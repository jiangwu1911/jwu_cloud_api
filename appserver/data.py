# -*- coding: UTF-8 -*-

from sqlalchemy.orm import sessionmaker
from model import Dept
from model import User
from model import Role
from model import Permission
from model import UserRoleMembership
import utils


def insert_basic_data(engine):
    Session = sessionmaker(engine)
    session = Session()

    dept = Dept(name='总部', desc='公司总部')
    session.add(dept)

    admin = User(name='admin', password=utils.md5encode('admin'), dept_id=dept.id)
    session.add(admin)

    admin_role = Role('管理员', '管理员')
    user_role = Role('普通用户', '普通用户')
    session.add(admin_role)
    session.add(user_role)

    membership1 = UserRoleMembership(user_id=admin.id, 
                                     role_id=admin_role.id)
    session.add(membership1)

    session.commit()


def insert_test_data(engine):
    Session = sessionmaker(engine)
    session = Session()

    head_dept = session.query(Dept).filter(Dept.name=='总部').first()
    dept1 = Dept(name='研发部', desc='研发部', parent_dept_id=head_dept.id)
    dept1_1 = Dept(name='研发一部', desc='研发一部', parent_dept_id=dept1.id)
    dept1_2 = Dept(name='研发二部', desc='研发二部', parent_dept_id=dept1.id)
    dept2 = Dept(name='市场部', desc='市场部', parent_dept_id=head_dept.id) 
    dept2_1 = Dept(name='市场一部', desc='市场一部', parent_dept_id=dept2.id) 
    dept2_2 = Dept(name='市场二部', desc='市场二部', parent_dept_id=dept2.id) 
    session.add(dept1)
    session.add(dept1_1)
    session.add(dept1_2)
    session.add(dept2)
    session.add(dept2_1)
    session.add(dept2_2)

    user1 = User(name='熊大', password=utils.md5encode('abc123'), dept_id=dept1.id)
    user2 = User(name='熊二', password=utils.md5encode('abc123'), dept_id=dept2.id)
    user3 = User(name='张三', password=utils.md5encode('abc123'), dept_id=dept1_1.id)
    user4 = User(name='李四', password=utils.md5encode('abc123'), dept_id=dept1_2.id)
    user5 = User(name='王五', password=utils.md5encode('abc123'), dept_id=dept2_1.id)
    user6 = User(name='赵六', password=utils.md5encode('abc123'), dept_id=dept2_2.id)
    user7 = User(name='用户1', password=utils.md5encode('abc123'), dept_id=dept1_1.id)
    user8 = User(name='用户2', password=utils.md5encode('abc123'), dept_id=dept1_2.id)
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.add(user5)
    session.add(user6)
    session.add(user7)
    session.add(user8)

    admin_role = session.query(Role).filter(Role.name=='管理员').first()
    user_role = session.query(Role).filter(Role.name=='普通用户').first()

    session.add(UserRoleMembership(user1.id, admin_role.id))
    session.add(UserRoleMembership(user2.id, admin_role.id))
    session.add(UserRoleMembership(user3.id, admin_role.id))
    session.add(UserRoleMembership(user4.id, admin_role.id))
    session.add(UserRoleMembership(user5.id, admin_role.id))
    session.add(UserRoleMembership(user6.id, admin_role.id))
    session.add(UserRoleMembership(user7.id, user_role.id))
    session.add(UserRoleMembership(user8.id, user_role.id))

    session.add(Permission(path='^/dept$', role_id=admin_role.id, method='GET'))
    session.add(Permission(path='^/dept$', role_id=admin_role.id, method='PUT'))
    session.add(Permission(path='^/dept$', role_id=admin_role.id, method='POST'))
    session.add(Permission(path='^/dept$', role_id=admin_role.id, method='DELETE'))
    session.add(Permission(path='^/dept$', role_id=user_role.id, method='GET'))

    session.commit()
