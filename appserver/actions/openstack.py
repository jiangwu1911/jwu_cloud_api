# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient

import logging
from common import pre_check
from common import get_input
from common import get_required_input
from error import CannotConnectToOpenStackError
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
        except Exception, e:
            log.error(e)
            raise CannotConnectToOpenStackError()
        return ret 
    return _deco


@pre_check
@openstack_call
def list_flavor(request, db, context):
    objs = nova_client.flavors.list()
    return {'flavors': [o.to_dict() for o in objs if o]}


@pre_check
@openstack_call
def list_image(request, db, context):
    objs = nova_client.images.list()
    return {'images': [o.to_dict() for o in objs if o]}


@pre_check
@openstack_call
def list_server(request, db, context):
    objs = nova_client.servers.list()
    return {'servers': [o.to_dict() for o in objs if o]}


@pre_check
@openstack_call
def start_server(request, db, context):
    flavor = get_required_input(req, 'flavor')
    image = get_required_input(req, 'image')
    

    
