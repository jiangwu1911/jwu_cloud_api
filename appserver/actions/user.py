# -*- coding: UTF-8 -*-

import logging
from sqlalchemy.exc import SQLAlchemyError

import model
import utils
import bottle
from common import pre_check
from common import get_input
from common import get_required_input
from common import is_dept_admin
from common import get_all_roles
from common import handle_db_error
from error import NotDeptAdminError
from error import UserNotFoundError
from error import UsernameAlreadyExistError
from error import EmailAlreadyExistError
from error import RolePermissionDenyError
from error import DatabaseError
from model import User
from model import Role
from model import UserRoleMembership
from utils import obj_array_to_json
from utils import obj_to_json
from actions.auth import delete_token
from actions.auth import generate_token

log = logging.getLogger("cloudapi")


@pre_check
def list_user(req, db, context):
    depts = []
    dept_id = get_input(req, 'dept_id')

    if dept_id and dept_id!="":
        dept_id = int(dept_id)
        if is_dept_admin(context, dept_id) == False:
            raise NotDeptAdminError(dept_id)
        depts.append(dept_id)
    else:
        depts = context['dept_ids']

    users = db.query(User).filter(User.dept_id.in_(depts))
    return obj_array_to_json(users, 'users')


@pre_check
def show_user(req, db, context, user_id):
    user = db.query(User).filter(User.dept_id.in_(context['dept_ids']),
                                 User.id==user_id).first()
    if user == None: 
        raise UserNotFoundError(user_id)
    return obj_to_json(user, 'user')


@pre_check
def add_user(req, db, context):
    name = get_required_input(req, 'username')
    password = get_required_input(req, 'password')
    email = get_input(req, 'email')
    dept_id = int(get_required_input(req, 'dept_id'))
    role_id = get_input(req, 'role_id')

    if db.query(User).filter(User.name==name, User.deleted==0).count() > 0:
        raise UsernameAlreadyExistError(name)

    if db.query(User).filter(User.email==email, User.deleted==0).count() > 0:
        raise EmailAlreadyExistError(email)

    if is_dept_admin(context, dept_id) == False:
        raise NotDeptAdminError(dept_id)

    if role_id == None:
        user_role = db.query(Role).filter(Role.name=='普通用户').first()
        role_id = user_role.id
    else:
        role_id = int(role_id)
        operator_role_id = int(context['membership'].role_id)
        if role_id < operator_role_id:
            raise RolePermissionDenyError(role_id)

    try:
        user = User(name=name, password=password, email=email, dept_id=dept_id)
        db.add(user)
        db.flush()
        membership = UserRoleMembership(user_id=user.id, role_id=role_id)
        db.add(membership)
        db.commit()
    except Exception, e:
        handle_db_error(db, e)
         
    return obj_to_json(user, 'user')


@pre_check
def update_user(req, db, context, user_id):
    user_id = int(user_id) 
    name = get_input(req, 'username')
    password = get_input(req, 'password')
    email = get_input(req, 'email')
    dept_id = get_input(req, 'dept_id')
    role_id = get_input(req, 'role_id')
    action = get_input(req, 'action')
    
    if action and action=='refresh_token':
        if context['user'].id == user_id:
            # 客户端请求更新token
            token = req.get_header('X-Auth-Token')
            delete_token(db, token)
            token = generate_token(db, user_id)
            return {'success': {'token': token.id}}

    result = db.query(User).filter(User.id==user_id, User.deleted==0)
    if result.count() == 0:
        raise UserNotFoundError(user_id)
    user = result.first()

    if name:
        if db.query(User).filter(User.name==name, User.deleted==0, User.id!=user_id).count() > 0:
            raise UsernameAlreadyExistError(name)
        user.name = name

    if password:
        user.password = password

    if email:
        if db.query(User).filter(User.email==email, User.deleted==0, User.id!=user_id).count() > 0:
            raise EmailAlreadyExistError(email)
        user.email = email

    if dept_id:
        dept_id = int(dept_id)
        if is_dept_admin(context, dept_id) == False:
            raise NotDeptAdminError(dept_id)
        user.dept_id = dept_id

    if role_id:
        role_id = int(role_id)
        operator_role_id = int(context['membership'].role_id)
        if role_id < operator_role_id:
            # 部门管理员不能授予用户系统管理员的权限
            raise RolePermissionDenyError(role_id)

    try:
        db.add(user)
        db.query(UserRoleMembership).filter(UserRoleMembership.user_id==user_id).delete()
        membership = UserRoleMembership(user_id=user_id, role_id=role_id)
        db.add(membership)
        db.commit()
    except Exception, e:
        handle_db_error(db, e)


@pre_check
def delete_user(req, db, context, user_id):
    user_id = int(user_id)
    user = db.query(User).filter(User.dept_id.in_(context['dept_ids']),
                                 User.id==user_id).first()
    if user == None:
        raise UserNotFoundError(user_id)
    
    user.deleted = 1
    db.add(user)
    db.commit()
