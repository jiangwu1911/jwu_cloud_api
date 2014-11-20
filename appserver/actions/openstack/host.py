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
def list_host(req, db, context):
    hosts = {}

    results = admin_nova_client().services.list()
    results1 = admin_cinder_client().services.list()

    for r in (results + results1):
        host = r.host
        if hosts.has_key(host):
            hosts[host]['service'] += ', %s' % r.binary
        else:
            hosts[host] = {}
            hosts[host]['id'] = r.id
            hosts[host]['hostname'] = r.host
            hosts[host]['state'] = r.state
            hosts[host]['service'] = r.binary

    return {'hosts': hosts.values()}
