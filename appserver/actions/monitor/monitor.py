# -*- coding: UTF-8 -*-

import traceback
import datetime

import logging
from actions.monitor.common import *
from actions.common import get_input
from actions.common import pre_check
from utils import obj_array_to_json
from utils import obj_to_json
from error import MonitorDataTypeNotSupportedError

log = logging.getLogger("cloudapi")
supported_datatype = ['cpu', 'memory', 'load']

@pre_check
@monitor_call
def get_data(req, db, context, data_type):
    if data_type not in supported_datatype:
        raise MonitorDataTypeNotSupportedError(data_type)     

    func_name = "get_%s_data" % data_type
    eval(func_name)


def get_cpu_data(req, db, context):
    pass


def get_memory_data(req, db, context):
    pass


def get_load_data(req, db, context):
    pass
