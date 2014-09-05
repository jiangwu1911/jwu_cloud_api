# -*- coding: UTF-8 -*-

import logging
import datetime
from bottle import response

from model import Token
from model import User
from model import Dept
from model import Role
from model import UserRoleMembership
from model import Permission
from model import OperationLog
import utils
import global_variables as gl
from error import TokenNotProvidedError
from error import TokenNotFoundError
from error import TokenExpiredError
from error import PermissionDenyError
from error import EmptyVariableError
from error import DatabaseError


log = logging.getLogger("cloudapi")

def pre_check(func):
    def _deco(req, db, *args):
        # context里保存一些比如token, permission, 允许操作的部门等信息
        context = {}

        # 检查token是否正确
        verify_token(req, db, context);

        # 检查所属的role, 是否有进行这种操作的权限
        check_permission(req, db, context)

        # 获取用户所能操作的部门（包括子部门）
        get_all_depts(req, db, context)

        # 调用实际的处理函数
        ret = func(req, db, context, *args)

        response.content_type = "application/json"
        return ret
    return _deco


def verify_token(req, db, context=None):
    remove_expired_token(db)

    token = req.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first() 

    if not token:
        raise TokenNotProvidedError

    if result == None:
        raise TokenNotFoundError(token)

    if result.expires < datetime.datetime.now():
        raise TokenExpiredError(token)

    context['token'] = result
    return True 


def remove_expired_token(db):
    now = datetime.datetime.now()
    # Try to clean expired token every hour
    if now - gl.time_clean_expired_token > datetime.timedelta(seconds=3600):
        db.query(Token).filter(Token.expires < now).delete()
        gl.time_clean_expired_token = now

    
def check_permission(req, db, context):
    user = get_user_by_token(req, db)
    context['user'] = user

    membership = db.query(UserRoleMembership).filter(UserRoleMembership.user_id==user.id).first()
    if membership == None:
        raise PermissionDenyError()
    context['membership'] = membership

    permissions = db.query(Permission).filter_by(role_id=membership.role_id, method=req.method)
    context['permissions'] = []
    for p in permissions:
        context['permissions'].append(p)
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


def get_all_depts(req, db, context):
    depts = []
    depts.append(_get_dept(db, context['user'].dept_id))
    depts.extend(_get_sub_depts(db, context['user'].dept_id))
    context['depts'] = depts

    context['dept_ids'] = []
    for d in context['depts']:
        context['dept_ids'].append(d.id)

def _get_dept(db, dept_id):
    return db.query(Dept).filter(Dept.id==dept_id, Dept.deleted==0).first()

def _get_sub_depts(db, dept_id):
    depts = []
    sub_depts = db.query(Dept).filter(Dept.parent_id==dept_id, Dept.deleted==0)
    for d in sub_depts:
        depts.append(d)
        depts.extend(_get_sub_depts(db, d.id))
    return depts


def get_dept_tree(db, dept_id):
    obj = _get_dept(db, dept_id)
    dept = {}
    dept['id'] = obj.id
    dept['name'] = obj.name
    dept['children'] = []

    sub_depts = db.query(Dept).filter(Dept.parent_id==dept_id, Dept.deleted==0)
    for d in sub_depts:
        dept['children'].append(get_dept_tree(db, d.id))

    return dept


def is_dept_admin(context, dept_id):
    if context['membership'].role_id > 2:   # Not sys_admin and dept_admin
        return False

    for d in context['depts']:
        if d.id == dept_id:
            return True
    return False


def get_input(req, varname):
    value = req.forms.get(varname)
    return value 


def get_required_input(req, varname):
    value = req.forms.get(varname)
    if value==None or value=='':
        raise EmptyVariableError(varname)
    return value


def get_all_roles(db):
    roles = db.query(Role)
    return roles


def handle_db_error(db, e):
    log.error(e)
    db.rollback()
    raise DatabaseError(e)


def write_operation_log(db, user_id='', resource_type='', resource_id=0,
                        resource_uuid='', event=''):
    optlog = OperationLog(user_id = user_id,
                          resource_type = resource_type,
                          resource_id = resource_id,
                          resource_uuid = resource_uuid,
                          event = event,
                          occurred_at = datetime.datetime.now())
    db.add(optlog)
