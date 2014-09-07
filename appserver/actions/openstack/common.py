# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient
import datetime
from sqlalchemy.sql import or_

import logging
from actions.common import get_input
from actions.common import get_required_input
from actions.common import handle_db_error
from actions.common import write_operation_log
from actions.common import is_sys_admin_or_dept_admin
from actions.user import find_user
from error import CannotConnectToOpenStackError
from error import OpenStackError
from utils import obj_array_to_json
from utils import obj_to_json
from novaclient import exceptions
import settings as conf

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
