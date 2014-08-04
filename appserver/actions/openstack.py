# -*- coding: UTF-8 -*-

import logging
import model
import utils
import bottle
from common import pre_check
from common import get_input
from error import CannotConnectToOpenStackError
import novaclient.v1_1.client as nvclient
import settings as conf

log = logging.getLogger("cloudapi")


nova_client = nvclient.Client(auth_url = conf.openstack_keystone_url,
                           username = conf.openstack_user,
                           api_key = conf.openstack_password,
                           project_id = conf.openstack_tenant_name
                          )

@pre_check
def list_flavor(req, db, context):
    try:
        flavor_objs = nova_list_flavor()
        return {'flavors': [f.to_dict() for f in flavor_objs if f]}
    except Exception, e:
        raise CannotConnectToOpenStackError()


def nova_list_flavor():
    return nova_client.flavors.list()
