# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient
import datetime

import logging
from actions.common import get_input
from actions.common import get_required_input
from actions.common import handle_db_error
from actions.common import write_operation_log
from actions.common import is_sys_admin_or_dept_admin
from actions.common import pre_check
from actions.user import find_user
from utils import obj_array_to_json
from utils import obj_to_json
from model import Volume
from error import VolumeNotFoundError
from error import UnsupportedOperationError

from actions.openstack.common import *
from actions.openstack.server import find_server

log = logging.getLogger("cloudapi")


@pre_check
@openstack_call
def list_volume(req, db, context):
    if is_sys_admin_or_dept_admin(context):
        # 管理员可以看到部门下面所有云硬盘
        volumes = db.query(Volume).filter(Volume.dept.in_(context['dept_ids']),
                                          Volume.deleted==0).all()
    else:
        # 普通用户只能看到属于自己的云硬盘
        volumes = db.query(Volume).filter(Volume.owner==context['user'].id,
                                          Volume.deleted==0).all()
    return obj_array_to_json(volumes, 'volumes')


def find_volume(db, context, volume_id):
    if is_sys_admin_or_dept_admin(context):
        # 管理员可以看到部门下面所有机器
        volume = db.query(Volume).filter(Volume.dept.in_(context['dept_ids']),
                                         Volume.deleted==0,
                                         Volume.id==volume_id).first()
    else:
        # 普通用户只能看到属于自己的机器
        volume = db.query(Volume).filter(Volume.owner==context['user'].id,
                                         Volume.deleted==0,
                                         Volume.id==volume_id).first()
    if volume == None:
        raise VolumeNotFoundError(volume_id)

    return volume


@pre_check
@openstack_call
def show_volume(req, db, context, volume_id):
    volume = find_volume(db, context, volume_id);
    return obj_to_json(volume, 'volume')


@pre_check
@openstack_call
def create_volume(req, db, context):
    name = get_required_input(req, 'name')
    size = get_required_input(req, 'size')

    data = {'display_name': name}
    ret = cinder_client().volumes.create(size, **data)

    volume = Volume(creator = context['user'].id,
                    dept = context['user'].dept_id, # 部门设置成创建者所属的部门
                    name = name,
                    volume_id = ret.id,
                    status = ret.status,
                    size = size,
                    created_at = datetime.datetime.now())

    db.add(volume)
    db.commit()
    write_operation_log(db,
                        user_id = context['user'].id,
                        resource_type = 'volume',
                        resource_id = volume.id,
                        resource_uuid = volume.volume_id,
                        event = 'create_volume')
    db.commit()
    log.debug(volume)
    return obj_to_json(volume, 'volume')


@pre_check
@openstack_call
def delete_volume(req, db, context, id):
    volume = find_volume(db, context, id)
    volume.status = 'deleting'
    db.add(volume)
    db.commit()

    try:
        cinder_client().volumes.delete(volume.volume_id)
    except ci_ex.NotFound, e:
        # volume在openstack中已被删除
        volume.deleted = 1
        volume.deleted_at = datetime.datetime.now()
        db.add(volume)
        db.commit()

    write_operation_log(db,
                        user_id = context['user'].id,
                        resource_type = 'volume',
                        resource_id = volume.id,
                        resource_uuid = volume.volume_id,
                        event = 'delete volume')
    db.commit()


@pre_check
@openstack_call
def update_volume(req, db, context, id):
    volume = find_volume(db, context, id);

    name = get_input(req, 'name')
    if name:
        volume.name = name

    owner_id = get_input(req, 'owner')
    if owner_id:
        owner = find_user(db, context, owner_id)
        volume.owner = owner_id
        volume.dept = owner.dept_id

    db.add(volume)
    db.commit()

    action = get_input(req, 'action')
    if action:
        if action == 'attach':
            return attach(req, db, context, volume)
        elif action == 'detach':
            return detach(req, db, context, volume)
        else:
            raise UnsupportedOperationError(action)


def attach(req, db, context, volume):
    server_id = get_required_input(req, 'server_id')
    device = get_input(req, 'device')
    server = find_server(db, context, server_id)

    nova_client().volumes.create_server_volume(server.instance_id,
                                             volume.volume_id,
                                             device)
    volume.status = 'attaching'
    volume.owner = server.owner
    db.add(volume)
    db.commit()


def detach(req, db, context, volume):
    server = find_server(db, context, volume.attached_to)
    nova_client().volumes.delete_server_volume(server.instance_id,
                                             volume.volume_id)
    volume.status = 'detaching'
    db.add(volume)
    db.commit()
