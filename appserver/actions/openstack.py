# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient
import datetime
from sqlalchemy.sql import or_

import logging
from common import pre_check
from common import get_input
from common import get_required_input
from common import handle_db_error
from common import write_operation_log
from common import is_sys_admin_or_dept_admin
from user import find_user
from error import CannotConnectToOpenStackError
from error import FlavorNotFoundError
from error import ImageNotFoundError
from error import ServerNotFoundError
from error import DatabaseError
from error import UnsupportedOperationError
from error import FlavorAlreadyExistError
from error import OpenStackError
from utils import obj_array_to_json
from utils import obj_to_json
from novaclient import exceptions
import settings as conf
from model import Server

log = logging.getLogger("cloudapi")


nova_client = nvclient.Client(auth_url = conf.openstack_api['keystone_url'],
                              username = conf.openstack_api['user'],
                              api_key = conf.openstack_api['password'],
                              project_id = conf.openstack_api['tenant_name']
                             )

# 某些操作, 比如创建flavor, 只能用admin身份做
admin_nova_client =  nvclient.Client(auth_url = conf.openstack_api['keystone_url'],
                              username = conf.openstack_api['admin_user'],
                              api_key = conf.openstack_api['admin_password'],
                              project_id = conf.openstack_api['admin_tenant_name']
                             )


def openstack_call(func):
    def _deco(*args):
        try:
            return func(*args)

        except (exceptions.ConnectionRefused, exceptions.Unauthorized) as e:
            log.error(e)
            raise CannotConnectToOpenStackError()

        except (exceptions.ClientException, exceptions.CommandError) as e:
            raise OpenStackError(e)

    return _deco


# ---------------------- Flavor related ---------------------------

@pre_check
@openstack_call
def list_flavor(req, db, context):
    objs = nova_client.flavors.list()

    flavors = []
    for o in objs:
        d = o.to_dict()
        d['ephemeral'] = d['OS-FLV-EXT-DATA:ephemeral']
        if d['swap'] == '':
            d['swap'] = 0
        flavors.append(d)
        
    return {'flavors': flavors}


@pre_check
@openstack_call
def create_flavor(req, db, context):
    name = get_required_input(req, 'name')
    vcpus = get_required_input(req, 'vcpus')
    ram = get_required_input(req, 'ram')
    disk = get_required_input(req, 'disk')
    ephemeral = get_input(req, 'ephemeral') 
    swap = get_input(req, 'swap')

    flavor = admin_nova_client.flavors.create(name, ram, vcpus, disk,
                                              flavorid='auto', 
                                              ephemeral=ephemeral,
                                              swap=swap,
                                              is_public=True)
    return {'flavor': flavor.to_dict()}


@pre_check
@openstack_call
def delete_flavor(req, db, context, flavor_id):
    admin_nova_client.flavors.delete(flavor_id)


@pre_check
@openstack_call
def update_flavor(req, db, context, flavor_id):
    name = get_input(req, 'name')
    vcpus = get_input(req, 'vcpus')
    ram = get_input(req, 'ram')
    disk = get_input(req, 'disk')
    ephemeral = get_input(req, 'ephemeral')
    swap = get_input(req, 'swap')

    if name==None or name=='':
        name = f.name
    if vcpus==None or name=='':
        vcpus = f.vcpus
    if ram==None or ram=='':
        ram = f.ram
    if disk==None or disk=='':
        disk = f.disk
    if ephemeral==None or ephemeral=='':
        ephemeral = f.ephemeral
    if swap==None or swap=='':
        swap = f.swap

    admin_nova_client.flavors.delete(flavor_id)
        
    flavor = admin_nova_client.flavors.create(name, int(ram), int(vcpus), int(disk),
                                              flavorid=flavor_id,
                                              ephemeral=int(ephemeral),
                                              swap=int(swap),
                                              is_public=True)
    return {'flavor': flavor.to_dict()}


# ---------------------- Image related ---------------------------

@pre_check
@openstack_call
def list_image(req, db, context):
    objs = nova_client.images.list()
    return {'images': [o.to_dict() for o in objs if o]}


# ---------------------- Server related ---------------------------

@pre_check
@openstack_call
def list_server(req, db, context):
    if is_sys_admin_or_dept_admin(context):
        # 管理员可以看到部门下面所有机器
        servers = db.query(Server).filter(Server.dept.in_(context['dept_ids']),
                                          Server.deleted==0).all()
    else:
        # 普通用户只能看到属于自己的机器
        servers = db.query(Server).filter(Server.owner==context['user'].id,
                                          Server.deleted==0).all()
    return obj_array_to_json(servers, 'servers')


def find_server(db, context, server_id):
    if is_sys_admin_or_dept_admin(context):
        # 管理员可以看到部门下面所有机器
        server = db.query(Server).filter(Server.dept.in_(context['dept_ids']),
                                         Server.deleted==0,
                                         Server.id==server_id).first()
    else:
        # 普通用户只能看到属于自己的机器
        server = db.query(Server).filter(Server.owner==context['user'].id,
                                         Server.deleted==0,
                                         Server.id==server_id).first()
    if server == None:
        raise ServerNotFoundError(server_id)
    return server


@pre_check
@openstack_call
def show_server(req, db, context, server_id):
    server = find_server(db, context, server_id);
    return obj_to_json(server, 'server')


@pre_check
@openstack_call
def create_server(req, db, context):
    flavor_name = get_required_input(req, 'flavor_name')
    image_name = get_required_input(req, 'image_name')
    server_name = get_required_input(req, 'server_name')
    
    try:
        flavor = nova_client.flavors.find(name=flavor_name)
    except exceptions.NotFound, e:
        raise FlavorNotFoundError(flavor_name)

    try:
        image = nova_client.images.find(name=image_name)
    except exceptions.NotFound, e:
        raise ImageNotFoundError(image_name)

    instance = nova_client.servers.create(name=server_name,
                                          image=image,
                                          flavor=flavor)
    
    flavor = flavor.to_dict()
    instance = nova_client.servers.get(instance).to_dict()
    server = Server(creator = context['user'].id,
                    owner = None,  
                    dept = context['user'].dept_id, # 部门设置成创建者所属的部门
                    name = server_name,
                    image = image_name,
                    flavor = flavor_name,
                    instance_id = instance.get('id', None),
                    state = instance.get('OS-EXT-STS:vm_state', None),
                    task_state = instance.get('OS-EXT-STS:task_state', None),
                    ram = flavor.get('ram', 0),
                    disk = flavor.get('disk', 0),
                    ephemeral = flavor.get('OS-FLV-EXT-DATA:ephemeral', 0),
                    swap = 0,
                    vcpus = flavor.get('vcpus', 0),
                    ip = '',
                    created_by = context['user'].id,
                    created_at = datetime.datetime.now())

    try:
        db.add(server)
        db.commit()
        write_operation_log(db,
                            user_id = context['user'].id,
                            resource_type = 'server', 
                            resource_id = server.id,
                            resource_uuid = instance['id'],
                            event = 'create server')
        db.commit()
    except Exception, e:
        handle_db_error(db, e)

    return obj_to_json(server, 'server')


@pre_check
@openstack_call
def delete_server(req, db, context, server_id):
    server = find_server(db, context, server_id);
    try:
        nova_client.servers.delete(server.instance_id)
    except exceptions.NotFound, e:
        # server在openstack中已被删除
        server.deleted = 1
        server.deleted_at = datetime.datetime.now()
        db.add(server)
        db.commit()

    try:
        write_operation_log(db,
                            user_id = context['user'].id,
                            resource_type = 'server',
                            resource_id = server_id,
                            resource_uuid = server.instance_id,
                            event = 'delete server')
        db.commit() 
    except Exception, e:
        handle_db_error(db, e)


@pre_check
@openstack_call
def update_server(req, db, context, server_id):
    server = find_server(db, context, server_id);

    name = get_input(req, 'name')
    if name:
        server.name = name
    
    owner_id = get_input(req, 'owner')
    if owner_id:
        owner = find_user(db, context, owner_id)
        server.owner = owner_id
        server.dept = owner.dept_id

    db.add(server)
    db.commit()

    action = get_input(req, 'action') 
    if action:
        if action == 'start':
            return start_server(server)
        elif action == 'stop':
            return stop_server(server)
        elif action == 'suspend':
            return suspend_server(server)
        elif action == 'resume':
            return resume_server(server)
        elif action == 'get_console':
            return get_console(req, db, server)
        else:
            raise UnsupportedOperationError(action)


def start_server(server):
    nova_client.servers.start(server.instance_id) 


def stop_server(server):
    nova_client.servers.stop(server.instance_id)


def suspend_server(server):
    nova_client.servers.suspend(server.instance_id) 


def resume_server(server):
    nova_client.servers.resume(server.instance_id)


def get_console(req, db, server):
    console_type = get_input(req, 'console_type');
    if console_type==None or console_type=='':
        console_type = 'novnc'

    ret = nova_client.servers.get_vnc_console(server.instance_id,
                                              console_type)
    server.console_url = ret['console']['url']
    db.add(server)
    db.commit()
    return ret
