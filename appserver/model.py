from sqlalchemy import Column, Integer, Sequence, String, Text, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import utils

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(String(100), primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100))
    enabled = Column(Integer, default=1, nullable=False)
    dept_id = Column(String(100), nullable=False)

    def __init__(self, name='', password='', email='', enabled=1, dept_id=''):
        self.id = utils.get_uuid()
        self.name = name
        self.password = password
        self.email = email
        self.enabled = enabled
        self.dept_id = dept_id

    def __repr__(self):
        return ("<User('%s', '%s', '%s', '%s', %d, '%s')>" 
                % (self.id, 
                   self.name, 
                   self.password,
                   self.email,
                   self.enabled,
                   self.dept_id))


class Role(Base):
    __tablename__ = 'role'
    id = Column(String(100), primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(200))

    def __init__(self, name='', desc=''):
        self.id = utils.get_uuid()
        self.name = name
        self.desc = desc

    def __repr__(self):
        return("<Role('%s', '%s', '%s')>"
               % (self.id,
                  self.name,
                  self.desc))


class Dept(Base):
    __tablename__ = 'dept'
    id = Column(String(100), primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(200))
    parent_dept_id = Column(String(100))
    
    def __init__(self, name='', desc='', parent_dept_id=''):
        self.id = utils.get_uuid()
        self.name = name
        self.desc = desc
        self.parent_dept_id = parent_dept_id
    
    def __repr__(self):
        return("<Dept('%s', '%s', '%s', '%s')>"
               % (self.id,
                  self.name,
                  self.desc,
                  self.parent_dept_id))


class UserRoleMembership(Base):
    __tablename__ = 'user_role_membership'
    id = Column(Integer, Sequence('membership_id_seq'), primary_key=True)
    user_id = Column(String(100), nullable=False)
    role_id = Column(String(100), nullable=False)
    
    def __init__(self, user_id='', role_id=''):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return("<UserRoleMembership('%s', '%s')>"
               % (self.user_id,
                  self.role_id))


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(String(100), primary_key=True)
    role_id = Column(String(100), nullable=False)
    path = Column(String(500), nullable=False)
    method = Column(String(20), nullable=False)
    is_permit = Column(Integer, default=1, nullable=False)

    def __init__(self, path='', role_id='', method='', is_permit=1):
        self.id = utils.get_uuid()
        self.role_id = role_id
        self.path = path
        self.method = method
        self.is_permit = is_permit

    def __repr__(self):
        return("<Permission('%s', '%s', '%s', '%s', %d)>"
               % (self.id,
                  self.role_id,
                  self.path,
                  self.method,
                  self.is_permit))


class Token(Base):
    __tablename__ = 'token'
    id = Column(String(100), primary_key=True)
    expires = Column('expires', DateTime)
    user_id = Column(String(100))

    def __init__(self, expires=-1, user_id=0):
        self.id = utils.get_uuid()
        self.expires = expires
        self.user_id = user_id

    def __repr__(self):
        return("<Token('%s', '%s', '%s')>"
               % (self.id,
                  self.expires,
                  self.user_id))
