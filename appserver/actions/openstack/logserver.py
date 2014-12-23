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
import settings as conf

log = logging.getLogger("cloudapi")


@pre_check
@openstack_call
def show_log_server_url(req, db, context):
    return conf.openstack_log_server['url']
