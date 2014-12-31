# -*- coding: UTF-8 -*-

import traceback
import datetime
from time import *

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

    host = get_required_input(req, 'hostname')

    from_time = get_input(req, "from_time")
    if from_time==None or from_time=='':
        from_time = (get_current_time() - 600) * 1000      # 缺省查询10分钟的数据
    else: 
        from_time = int(from_time)

    to_time = get_input(req, "to_time")
    if to_time==None or to_time=='':
        to_time = get_current_time() * 1000              
    else: 
        to_time = int(to_time)

    interval = get_input(req, "interval")
    if interval==None or interval=='':
        interval = 60 * 1000                                # 缺省间隔1分钟
    else:
        interval = int(interval)

    if data_type == "cpu":
        return get_cpu_data(host, from_time, to_time, interval)
    elif data_type == "memory":
        return get_memory_data(host, from_time, to_time, interval)
    elif data_type == "load":
        return get_load_data(host, from_time, to_time, interval)


def get_current_time():
    return time()


# 发现ES中,如果输入的时间没按interval对齐,查询出的数据不准确
# adjust_time将时间按interval对其
# 输入输出参数单位都是秒,注意在ES中,需要将其乘以1000使用
def adjust_time(t, interval):
    return int(t / interval) * interval


def get_cpu_data(host, from_time, to_time, interval):
    from_time = adjust_time(from_time, interval)
    to_time = adjust_time(to_time, interval)
    es = connect_to_elasticsearch()
    querys = []

    cpu_ids = _get_cpu_ids(es, host)
    for cpu_id in cpu_ids:
        for type in ('idle', 'user', 'system'):
            q = _build_es_search_body_for_cpu(host, cpu_id, type, from_time, to_time, interval)
            querys.append({})       # Append a empty header
            querys.append(q)

    results = es.msearch(body=querys)
    return {'cpustats': _parse_cpu_search_result(results)}


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


def _results_to_graph_data(results):
    graph_data = {}
    for r in results['responses']:
        for k in r['facets'].keys():
            graph = []
            for item in r['facets'][k]['entries']:
                graph.append({'date': item['time'],
                              'value': item['mean']})
            # 排序
            graph.sort(lambda x,y : cmp(x['date'], y['date']))

            # 求差值
            new_graph = []
            last_point = None
            for point in graph:
                if last_point != None:
                    p = {}
                    p['date'] = strftime("%Y-%m-%d %H:%M:%S", localtime(point['date']/1000))
                    p['value'] = (point['value'] - last_point['value']) * 1000 / \
                                 (point['date'] - last_point['date'])
                    new_graph.append(p)
                last_point = point
            graph_data[k] = new_graph
    return graph_data


def _parse_cpu_search_result(results):
    graph_data = _results_to_graph_data(results)
    # 目前为方便起见，把所有数据合成一个图，横坐标是时间，纵坐标是所有cpu的system+user/system+user+idle
    chart_data = {}
    for k in graph_data.keys():
        for g in graph_data[k]:
            t = g['date']
            if not chart_data.has_key(t):
                chart_data[t] = {}
                chart_data[t]['date'] = t
                chart_data[t]['used'] = 0
                chart_data[t]['total'] = 0

            if k.find('system')>0 or k.find('user')>0:
                chart_data[t]['used'] += g['value']
            chart_data[t]['total'] += g['value'] 

    return_data = []
    for c in chart_data.values():
        point = {}
        point['date'] = c['date']
        point['value'] = c['used'] * 100 / c['total']
        return_data.append(point)
    
    return_data.sort(lambda x,y : cmp(x['date'], y['date']))
    return return_data


def get_memory_data(host, from_time, to_time, interval):
    from_time = adjust_time(from_time, interval)
    to_time = adjust_time(to_time, interval)
    es = connect_to_elasticsearch()
    querys = []

    for type in ('cached', 'used', 'buffered', 'free'):
        q = _build_es_search_body_for_memory(host, type, from_time, to_time, interval)
        querys.append({})
        querys.append(q)

    results = es.msearch(body=querys)
    print results


def _build_es_search_body_for_memory(host, type, from_time, to_time, interval):
    facet_name = "facet_%s" % (type)
    query_string = "plugin:memory AND type_instance:%s" % (type)
    return _build_es_search_body(facet_name, query_string, host, from_time, to_time, interval)


def _parse_memory_search_result(results):
    pass


def get_load_data(req, db, context):
    pass
