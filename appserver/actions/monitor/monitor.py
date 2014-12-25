# -*- coding: UTF-8 -*-

import traceback
import datetime

import logging
from actions.monitor.common import *
from actions.common import get_required_input
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

    host = get_required_input(req, 'host')

    from_time = get_input(req, "from_time")
    if from_time==None or from_time=='':
        from_time = "now-30m"

    to_time = get_input(req, "to_time")
    if to_time==None or to_time=='':
        to_time = "now"

    interval = get_input(req, "interval")
    if interval==None or interval=='':
        interval = "1m"

    if data_type == "cpu":
        return get_cpu_data(host, from_time, to_time, interval)
    elif data_type == "memory":
        return get_memory_data(host, from_time, to_time, interval)
    elif data_type == "load":
        return get_load_data(host, from_time, to_time, interval)


def get_cpu_data(host, from_time, to_time, interval):
    es = connect_to_elasticsearch()
    querys = []
    cpu_ids = _get_cpu_ids(es, host)
    for cpu_id in cpu_ids:
        for type in ('idle', 'user', 'system'):
            q = _build_es_search_body_for_cpu(host, cpu_id, type, from_time, to_time, interval)
            querys.append({})       # Append a empty header
            querys.append(q)

    results = es.msearch(body=querys)
    print results


def _get_cpu_ids(es, host):
    result = es.search(body={
                        "query": { "query_string": { "query": "type:collectd AND host:%s AND plugin:cpu" % host }, },
                        "facets": { "cpu_id": { "terms": {"field": "plugin_instance" }} },
                        "size": 0
                    })
    cpu_ids = []
    for r in result['facets']['cpu_id']['terms']:
        cpu_ids.append(r['term'])
    return cpu_ids


def _build_es_search_body_for_cpu(host, cpu_id, type, from_time, to_time, interval):
    facet_name = "facet_%s_%s" % (cpu_id, type)
    query_string = "plugin:cpu AND plugin_instance:%s AND type_instance:%s" % (cpu_id, type)
    return _build_es_search_body(facet_name, query_string, host, from_time, to_time, interval)


def _build_es_search_body(facet_name, query_string, host, from_time, to_time, interval):
    return {
        "facets": {
            facet_name: {
                "date_histogram": {
                    "key_field": "@timestamp",
                    "value_field": "value",
                    "interval": interval
                },
                "global": "true",
                "facet_filter": {
                    "fquery": {
                        "query": {
                            "filtered": {
                                "query": {
                                    "query_string": {
                                        "query": query_string
                                    }
                                },
                                "filter": {
                                    "bool": {
                                        "must": [
                                            {
                                                "range": {
                                                    "@timestamp": {
                                                        "from": from_time,
                                                        "to": to_time
                                                    }
                                                }
                                            },
                                            {
                                                "fquery": {
                                                    "query": {
                                                        "query_string": {
                                                            "query": "type:collectd AND host:\"%s\"" % host
                                                        }
                                                    },
                                                    "_cache": "true"
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "size": 0
    }


def get_memory_data(req, db, context):
    pass


def get_load_data(req, db, context):
    pass
