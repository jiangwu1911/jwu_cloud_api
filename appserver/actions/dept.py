# -*- coding: UTF-8 -*-

import logging

from common import pre_check
from common import get_input
from common import get_required_input
from common import is_dept_admin
from utils import obj_array_to_json
from utils import obj_to_json
from error import DeptNotFoundError
from error import DeptAlreadyExistError
from error import ParentDeptNotFoundError
from error import NotDeptAdminError
from error import DeptNotEmptyError
from error import ParentCannotBeSelfError
from model import Dept
from model import User

log = logging.getLogger("cloudapi")


@pre_check
def list_dept(req, db, context):
    return obj_array_to_json(context['depts'], 'depts')


@pre_check
def show_dept(req, db, context, dept_id):
    dept_id = int(dept_id)
    for d in context['depts']:
        if dept_id == d.id:
            return obj_to_json(d, 'dept')
    raise DeptNotFoundError(dept_id)


@pre_check
def add_dept(req, db, context):
    name = get_required_input(req, 'name')
    desc = get_required_input(req, 'desc')
    parent_id = int(get_required_input(req, 'parent_id'))
    
    if db.query(Dept).filter(Dept.name==name, Dept.deleted==0).count() > 0:
        raise DeptAlreadyExistError(name)

    if db.query(Dept).filter(Dept.id==parent_id, Dept.deleted==0).count() == 0:
        raise ParentDeptNotFoundError(parent_id)

    dept = Dept(name=name, desc=desc, parent_id=parent_id)
    db.add(dept)
    db.commit()
    log.debug(dept)
    return obj_to_json(dept, 'dept')


@pre_check
def update_dept(req, db, context, dept_id):
    dept_id = int(dept_id)
    name = get_input(req, 'name')
    desc = get_input(req, 'desc')
    parent_id = get_input(req, 'parent_id')
    
    result = db.query(Dept).filter(Dept.id==dept_id, Dept.deleted==0)
    if result.count() == 0:
        raise DeptNotFoundError(dept_id)
    dept = result.first()

    if is_dept_admin(context, dept_id) == False:
        raise NotDeptAdminError(dept_id)

    if name: 
        if db.query(Dept).filter(Dept.name==name, Dept.deleted==0, Dept.id!=dept_id).count() > 0:
            raise DeptAlreadyExistError(name) 
        dept.name = name

    dept.desc = desc
    if parent_id:
        if dept_id == int(parent_id):
            raise ParentCannotBeSelfError(dept_id)
        if db.query(Dept).filter(Dept.id==parent_id, Dept.deleted==0).count() == 0:
            raise ParentDeptNotFoundError(parent_id)
        dept.parent_id = parent_id

    db.add(dept)
    db.commit()
     

@pre_check
def delete_dept(req, db, context, dept_id):
    dept_id = int(dept_id)
    result = db.query(Dept).filter(Dept.id==dept_id, Dept.deleted==0)
    if result.count() == 0:
        raise DeptNotFoundError(dept_id)        
    dept = result.first()

    if is_dept_admin(context, dept_id) == False:
        raise NotDeptAdminError(dept_id)

    if db.query(User).filter(User.dept_id==dept_id).count() > 0:
        raise DeptNotEmptyError(dept_id)

    dept.deleted = 1
    db.add(dept)
    db.commit()
