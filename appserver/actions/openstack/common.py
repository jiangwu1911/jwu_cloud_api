# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient
import cinderclient.v1.client as ciclient
import threading

import logging
from error import CannotConnectToOpenStackError
from error import OpenStackError
import novaclient.exceptions as nv_ex
import cinderclient.exceptions as ci_ex
import settings as conf


log = logging.getLogger("cloudapi")
localdata = threading.local()

def nova_client():
    var = getattr(localdata, 'nova_client', None)
    if var is None:
        var = nvclient.Client(auth_url = conf.openstack_api['keystone_url'],
                              username = conf.openstack_api['user'],
                              api_key = conf.openstack_api['password'],
                              project_id = conf.openstack_api['tenant_name'])
        setattr(localdata, 'nova_client', var)
    return var


def admin_nova_client():
    var = getattr(localdata, 'admin_nova_client', None)
    if var is None:
        var = nvclient.Client(auth_url = conf.openstack_api['keystone_url'],
                              username = conf.openstack_api['admin_user'],
                              api_key = conf.openstack_api['admin_password'],
                              project_id = conf.openstack_api['admin_tenant_name'])
        setattr(localdata, 'admin_nova_client', var)
    return var


def cinder_client():
    var = getattr(localdata, 'cinder_client', None)
    if var is None:
        var = ciclient.Client(auth_url = conf.openstack_api['keystone_url'],
                              username = conf.openstack_api['user'],
                              api_key = conf.openstack_api['password'],
                              project_id = conf.openstack_api['tenant_name'])
        setattr(localdata, 'cinder_client', var)
    return var


def openstack_call(func):
    def _deco(*args):
        try:
            return func(*args)

        except (nv_ex.ConnectionRefused, nv_ex.Unauthorized, 
                ci_ex.ConnectionError, ci_ex.Unauthorized) as e:
            log.error(e)
            raise CannotConnectToOpenStackError()

        except (nv_ex.ClientException, nv_ex.CommandError, nv_ex.BadRequest,
                ci_ex.ClientException, ci_ex.CommandError, ci_ex.BadRequest) as e:
            raise OpenStackError(e)

    return _deco
