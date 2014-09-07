# -*- coding: UTF-8 -*-

import traceback
import novaclient.v1_1.client as nvclient
import datetime

import logging
from actions.openstack.common import *
from actions.common import get_input
from actions.common import pre_check
from utils import obj_array_to_json
from utils import obj_to_json

log = logging.getLogger("cloudapi")


@pre_check
@openstack_call
def list_hypervisor(req, db, context):
    action = get_input(req, 'action')

    print action

    if action == 'stats':
        return hopervisor_stats(db, context)

    else:
        results = admin_nova_client.hypervisors.list()
        return obj_array_to_json(results, 'hypervisors')


def hopervisor_stats(db, context):
    # 可以返回的信息
    # disk: local_gb, local_gb_used, disk_available_least, free_disk_gb
    # ram:  free_disk_gb, free_disk_gb, free_disk_gb
    # vcpus: vcpus, vcpus_used
    results = admin_nova_client.hypervisors.statistics()
    return obj_to_json(results, 'hypervisors')
