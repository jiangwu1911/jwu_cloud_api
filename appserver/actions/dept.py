# -*- coding: UTF-8 -*-

import logging
from sqlalchemy import or_

from model import Dept
from model import User
import utils
from common import pre_check
from common import get_userid_by_token
from utils import sql_results_to_json

log = logging.getLogger("cloudapi")


@pre_check
def list_dept(req, db):
    """Return all dept and sub depts"""
    user_id = get_userid_by_token(req, db)
    if user_id == None:
        return {'error': 'Invalid token'}
    
    user = db.query(User).filter(User.id==user_id).first()
    if user == None:
        return {'error': 'User not found'}

    depts = []
    depts.append(get_dept(db, user.dept_id))
    for d in get_sub_depts(db, user.dept_id):
        depts.append(d)

    return sql_results_to_json(depts, 'depts')


def get_dept(db, dept_id):
    return db.query(Dept).filter(Dept.id==dept_id).first()


def get_sub_depts(db, dept_id):
    depts = []

    sub_depts = db.query(Dept).filter(Dept.parent_dept_id==dept_id)

    for d in sub_depts:
        depts.append(d)

        sub1 = get_sub_depts(db, d.id)
        for d1 in sub1:
            depts.append(d1)
    
    return depts
