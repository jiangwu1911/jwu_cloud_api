# -*- coding: UTF-8 -*-

import logging

from common import pre_check
from common import get_required_input
from common import can_modify_dept
from utils import sql_result_to_json
from utils import one_line_sql_result_to_json
from error import DeptNotFoundError
from error import DeptExistError
from error import ParentDeptNotFoundError
from error import CannotModifyDeptError
from model import Dept


log = logging.getLogger("cloudapi")


@pre_check
def list_dept(req, db, context):
    return sql_result_to_json(context['depts'], 'depts')


@pre_check
def show_dept(req, db, context, dept_id):
    for d in context['depts']:
        if int(dept_id) == d.id:
            return one_line_sql_result_to_json(d, 'dept')
    raise DeptNotFoundError(dept_id)


@pre_check
def delete_dept(req, db, context):
    pass 


@pre_check
def add_dept(req, db, context):
    name = get_required_input(req, 'name')
    desc = get_required_input(req, 'desc')
    parent_dept_id = int(get_required_input(req, 'parent_dept_id'))
    
    if db.query(Dept).filter(Dept.name==name).count() > 0:
        raise DeptExistError(name)

    if db.query(Dept).filter(Dept.id==parent_dept_id).count() == 0:
        raise ParentDeptNotFoundError(parent_dept_id)

    if can_modify_dept(context, parent_dept_id) == False:
        raise CannotModifyDeptError(parent_dept_id) 

    dept = Dept(name=name, desc=desc, parent_dept_id=parent_dept_id)
    db.add(dept)
    db.commit()
    return one_line_sql_result_to_json(dept, 'dept')
