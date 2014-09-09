# -*- coding: UTF-8 -*-

import traceback
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
from model import Snapshot
from error import SnapshotNotFoundError
from error import UnsupportedOperationError
from actions.openstack.common import *

log = logging.getLogger("cloudapi")


@pre_check
@openstack_call
def list_snapshot(req, db, context):
    if is_sys_admin_or_dept_admin(context):
        # 管理员可以看到部门下面所有云硬盘
        snapshots = db.query(Snapshot).filter(Snapshot.dept.in_(context['dept_ids']),
                                          Snapshot.deleted==0).all()
    else:
        # 普通用户只能看到属于自己的云硬盘
        snapshots = db.query(Snapshot).filter(Snapshot.owner==context['user'].id,
                                          Snapshot.deleted==0).all()
    return obj_array_to_json(snapshots, 'snapshots')


def find_snapshot(db, context, snapshot_id):
    if is_sys_admin_or_dept_admin(context):
        # 管理员可以看到部门下面所有机器
        snapshot = db.query(Snapshot).filter(Snapshot.dept.in_(context['dept_ids']),
                                         Snapshot.deleted==0,
                                         Snapshot.id==snapshot_id).first()
    else:
        # 普通用户只能看到属于自己的机器
        snapshot = db.query(Snapshot).filter(Snapshot.owner==context['user'].id,
                                         Snapshot.deleted==0,
                                         Snapshot.id==snapshot_id).first()
    if snapshot == None:
        raise SnapshotNotFoundError(snapshot_id)

    return snapshot


@pre_check
@openstack_call
def show_snapshot(req, db, context, snapshot_id):
    snapshot = find_snapshot(db, context, snapshot_id);
    return obj_to_json(snapshot, 'snapshot')


@pre_check
@openstack_call
def delete_snapshot(req, db, context, id):
    snapshot = find_snapshot(db, context, id)
    snapshot.status = 'deleting'
    db.add(snapshot)
    db.commit()

    try:
        glance_client().images.delete(snapshot.snapshot_id)
    except gl_ex.NotFound: 
        snapshot.deleted = 1
        snapshot.deleted_at = datetime.datetime.now()
        db.add(snapshot)
        db.commit()

    write_operation_log(db,
                        user_id = context['user'].id,
                        resource_type = 'snapshot',
                        resource_id = snapshot.id,
                        resource_uuid = snapshot.snapshot_id,
                        event = 'delete snapshot')
    db.commit()


@pre_check
@openstack_call
def update_snapshot(req, db, context, id):
    snapshot = find_snapshot(db, context, id);

    name = get_input(req, 'name')
    if name:
        snapshot.name = name

    owner_id = get_input(req, 'owner')
    if owner_id:
        owner = find_user(db, context, owner_id)
        snapshot.owner = owner_id
        snapshot.dept = owner.dept_id

    db.add(snapshot)
    db.commit()
