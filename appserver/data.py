# -*- coding: UTF-8 -*-

from sqlalchemy.orm import sessionmaker
from model import Dept
from model import User
import utils


def insert_basic_data(engine):
    Session = sessionmaker(engine)
    session = Session()

    dept = Dept(name='总部', desc='公司总部')
    session.add(dept)
    user = User(name='admin', password=utils.md5encode('admin'), dept_id=dept.id)
    session.add(user)

    session.commit()


def insert_test_data(engine):
    Session = sessionmaker(engine)
    session = Session()

    head_dept = session.query(Dept).filter_by(name='总部').first()
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

    session.add(User(name='熊大', password=utils.md5encode('abc123'), dept_id=dept1.id))
    session.add(User(name='熊二', password=utils.md5encode('abc123'), dept_id=dept2.id))
    session.add(User(name='张三', password=utils.md5encode('abc123'), dept_id=dept1_1.id))
    session.add(User(name='李四', password=utils.md5encode('abc123'), dept_id=dept1_2.id))
    session.add(User(name='王五', password=utils.md5encode('abc123'), dept_id=dept2_1.id))
    session.add(User(name='赵六', password=utils.md5encode('abc123'), dept_id=dept2_2.id))

    session.commit()
