# -*- coding: UTF-8 -*-

import traceback
from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException

import logging
from error import MonitorServerError
import settings as conf


log = logging.getLogger("cloudapi")

def connect():
    return Elasticsearch(conf.monitor_server)


def monitor_call(func):
    def _deco(*args):
        try:
            return func(*args)

        except (ElasticsearchException) as e:
            log.error(e)
            raise MonitorServerError(e)
    return _deco
