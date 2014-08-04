# -*- coding: UTF-8 -*-

import logging

from common import pre_check
from utils import sql_result_to_json
from utils import one_line_sql_result_to_json
from error import DeptNotFoundError


log = logging.getLogger("cloudapi")


@pre_check
def list_dept(req, db, context):
    return sql_result_to_json(context['depts'], 'depts')


@pre_check
def show_dept_detail(req, db, context, dept_id):
    for d in context['depts']:
        if int(dept_id) == d.id:
            return one_line_sql_result_to_json(d, 'dept')
    raise DeptNotFoundError(dept_id)
