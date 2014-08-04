# -*- coding: UTF-8 -*-

import logging
from model import Token
from model import User
from model import Dept
from model import UserRoleMembership
from model import Permission
import utils
import datetime
import global_variables as gl

from error import TokenNotFoundError
from error import TokenExpiredError
from error import PermissionDenyError


log = logging.getLogger("cloudapi")

def pre_check(func):
    def _deco(req, db):
        #1. 检查token是否正确
        verify_token(req, db);

        #2. 检查所属的role, 是否有进行这种操作的权限
        check_permission(req, db)

        ret = func(req, db)
        return ret
    return _deco


def verify_token(req, db):
    remove_expired_token(db)

    token = req.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first() 

    if result == None:
        raise TokenNotFoundError(token)

    if result.expires < datetime.datetime.now():
        raise TokenExpiredError(token)

    return True 


def remove_expired_token(db):
    now = datetime.datetime.now()
    # Try to clean expired token every hour
    if now - gl.time_clean_expired_token > datetime.timedelta(seconds=3600):
        db.query(Token).filter(Token.expires < now).delete()
        gl.time_clean_expired_token = now

    
def check_permission(req, db):
    user = get_user_by_token(req, db)
    membership = db.query(UserRoleMembership).filter(UserRoleMembership.user_id==user.id).first()
    if membership == None:
        return False

    permissions = db.query(Permission).filter_by(role_id=membership.role_id,
                                                 method=req.method)
    for p in permissions:
        import re
        p = re.compile(p.path)
        if p.match(req.path):
            return True
    
    raise PermissionDenyError()        
    

def get_user_by_token(req, db):
    token = req.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first()
    if result == None:
        raise TokenNotFoundError(token)

    result = db.query(User).filter(User.id==result.user_id).first()
    if result == None:
        raise UserNotFoundError(result.user_id)
        
    return result


def get_all_depts(db, user):
    depts = []
    depts.append(_get_dept(db, user.dept_id))
    for d in _get_sub_depts(db, user.dept_id):
        depts.append(d)
    return depts

def _get_dept(db, dept_id):
    return db.query(Dept).filter(Dept.id==dept_id).first()

def _get_sub_depts(db, dept_id):
    depts = []
    sub_depts = db.query(Dept).filter(Dept.parent_dept_id==dept_id)

    for d in sub_depts:
        depts.append(d)
    return depts
