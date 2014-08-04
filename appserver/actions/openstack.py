# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient

import logging
from common import pre_check
from common import get_input
from common import get_required_input
from error import CannotConnectToOpenStackError
from error import FlavorNotFoundError
from error import ImageNotFoundError
from novaclient import exceptions
import settings as conf

log = logging.getLogger("cloudapi")


nova_client = nvclient.Client(auth_url = conf.openstack_keystone_url,
                              username = conf.openstack_user,
                              api_key = conf.openstack_password,
                              project_id = conf.openstack_tenant_name
                             )

def openstack_call(func):
    def _deco(*args):
        try:
            ret = func(*args)
        except (exceptions.ConnectionRefused, exceptions.Unauthorized) as e:
            log.error(e)
            raise CannotConnectToOpenStackError()
        return ret 
    return _deco


@pre_check
@openstack_call
def list_flavor(req, db, context):
    objs = nova_client.flavors.list()
    return {'flavors': [o.to_dict() for o in objs if o]}


@pre_check
@openstack_call
def list_image(req, db, context):
    objs = nova_client.images.list()
    return {'images': [o.to_dict() for o in objs if o]}


@pre_check
@openstack_call
def list_server(req, db, context):
    objs = nova_client.servers.list()
    return {'servers': [o.to_dict() for o in objs if o]}


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
    return {'server': instance.to_dict()}
