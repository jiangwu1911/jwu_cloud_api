# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient

import logging
from common import pre_check
from common import get_input
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
    flavor_objs = nova_client.flavors.list()
    return {'flavors': [f.to_dict() for f in flavor_objs if f]}
