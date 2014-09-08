from sqlalchemy import Column, Integer, Sequence, String, Text, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base
import utils
import datetime

Base = declarative_base()

class JsonObj():
    def to_dict(self):
        obj_dict = self.__dict__
        d = {}
        for key, val in obj_dict.items():
             if not key.startswith("_"):
                if isinstance(val, datetime.datetime):
                    d[key] = val.isoformat()
                else:
                    d[key] = val
        return d


class User(Base, JsonObj):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100))
    enabled = Column(Integer, default=1, nullable=False)
    dept_id = Column(Integer)
    deleted = Column(Integer, default=0, nullable=False)

    def __init__(self, name='', password='', email='', enabled=1, dept_id=0, deleted=0):
        self.name = name
        self.password = password
        self.email = email
        self.enabled = enabled
        self.dept_id = dept_id
        self.deleted = deleted

    def __repr__(self):
        return ("<User(%d, '%s', '%s', '%s', %d, %d, %d)>" 
                % (self.id, 
                   self.name, 
                   self.password,
                   self.email,
                   self.enabled,
                   self.dept_id,
                   self.deleted))


class Role(Base, JsonObj):
    __tablename__ = 'role'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(200))

    def __init__(self, name='', desc=''):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return("<Role(%d, '%s', '%s')>"
               % (self.id,
                  self.name,
                  self.desc))


class Dept(Base, JsonObj):
    __tablename__ = 'dept'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(200))
    parent_id = Column(Integer)
    deleted = Column(Integer, default=0, nullable=False)
    
    def __init__(self, name='', desc='', parent_id=0, deleted=0):
        self.name = name
        self.desc = desc
        self.parent_id = parent_id
        self.deleted = deleted
    
    def __repr__(self):
        return("<Dept(%d, '%s', '%s', %d, %d)>"
               % (self.id,
                  self.name,
                  self.desc,
                  self.parent_id,
                  self.deleted))


class UserRoleMembership(Base, JsonObj):
    __tablename__ = 'user_role_membership'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    user_id = Column(Integer)
    role_id = Column(Integer)
    
    def __init__(self, user_id=0, role_id=0):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return("<UserRoleMembership(%d, %d, %d)>"
               % (self.id,
                  self.user_id,
                  self.role_id))


class Permission(Base, JsonObj):
    __tablename__ = 'permission'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    role_id = Column(Integer)
    path = Column(String(500), nullable=False)
    method = Column(String(20), nullable=False)
    is_permit = Column(Integer, default=1, nullable=False)

    def __init__(self, path='', role_id=0, method='', is_permit=1):
        self.role_id = role_id
        self.path = path
        self.method = method
        self.is_permit = is_permit

    def __repr__(self):
        return("<Permission(%d, %d, '%s', '%s', %d)>"
               % (self.id,
                  self.role_id,
                  self.path,
                  self.method,
                  self.is_permit))


class Token(Base, JsonObj):
    __tablename__ = 'token'
    id = Column(String(100), primary_key=True)
    expires = Column(DateTime)
    user_id = Column(Integer)

    def __init__(self, expires=-1, user_id=0):
        self.id = utils.get_uuid()
        self.expires = expires
        self.user_id = user_id

    def __repr__(self):
        return("<Token('%s', '%s', %d)>"
               % (self.id,
                  self.expires,
                  self.user_id))


class Server(Base, JsonObj):
    """VM in OpenStack"""
    __tablename__ = 'server'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    image = Column(String(200))
    flavor = Column(String(200))
    creator = Column(Integer)   # Who created this server
    owner = Column(Integer)     # Currently who own this server
    dept = Column(Integer)
    name = Column(String(100), nullable=False)
    instance_id = Column(String(100), nullable=False)
    state = Column(String(100))
    task_state = Column(String(100))
    ram = Column(Integer)
    disk = Column(Integer)
    ephemeral = Column(Integer)
    swap = Column(Integer)
    vcpus = Column(Integer)
    ip = Column(String(100))
    fault = Column(String(500))
    console_url = Column(String(200))
    deleted = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    
    def __init__(self, image='', flavor='', creator=0, owner=0, dept=0, 
                 name='', instance_id='', state='', task_state='',
                 ram=0, disk=0, ephemeral=0, swap=0, vcpus=0, ip='', 
                 console_url='', fault='', deleted=0,
                 created_at='0000-00-00 00:00:00', 
                 updated_at='0000-00-00 00:00:00', 
                 deleted_at='0000-00-00 00:00:00'):
        self.image = image
        self.flavor = flavor
        self.creator = creator
        self.owner = owner
        self.dept = dept
        self.name = name
        self.instance_id = instance_id
        self.state = state
        self.task_state = task_state
        self.ram = ram
        self.disk = disk
        self.ephemeral = ephemeral
        self.swap = swap
        self.vcpus = vcpus
        self.ip = ip
        self.console_url = console_url
        self.falut = fault
        self.deleted = deleted
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self): 
        return("<Server(%d, %d, %d, %d, '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, \
                #%d, '%s', '%s', '%s', %d, '%s', '%s', '%s')>"
              % (self.id,
                 self.creator,
                 self.owner,
                 self.dept,
                 self.image,
                 self.flavor,
                 self.name,
                 self.instance_id,
                 self.state,
                 self.task_state,
                 self.ram, 
                 self.disk,
                 self.ephemeral,
                 self.swap,
                 self.vcpus,
                 self.ip,
                 self.console_url,
                 self.fault,
                 self.deleted,
                 self.created_at,
                 self.updated_at,
                 self.deleted_at
                ))


class Volume(Base, JsonObj):
    """Volume in OpenStack"""
    __tablename__ = 'volume'
    id =  Column(Integer, Sequence('seq_pk'), primary_key=True)
    creator = Column(Integer)   # Who created this volume
    owner = Column(Integer)     # Currently who own this volume
    dept = Column(Integer)
    name = Column(String(100), nullable=False)
    volume_id = Column(String(100), nullable=False)
    status = Column(String(100))
    size = Column(Integer)
    attached_to = Column(String(100))
    fault = Column(String(500))
    deleted = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def __init__(self, creator='', owner=0, dept=0, name='', volume_id='',
                 status='', size=0, attached_to='', fault='', deleted=0,
                 created_at='0000-00-00 00:00:00', 
                 updated_at='0000-00-00 00:00:00',
                 deleted_at='0000-00-00 00:00:00'):
        self.creator = creator
        self.owner = owner
        self.dept = dept
        self.name = name
        self.volume_id = volume_id
        self.status = status
        self.size = size
        self.attached_to = attached_to
        self.fault = fault
        self.deleted = deleted
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return("<Volume(%d, %d, %d, '%s', '%s', '%s', %d, '%s', %d, '%s', '%s', '%s', '%s')>"
             % (self.creator,
                self.owner,
                self.dept,
                self.name,
                self.volume_id,
                self.status,
                self.size,
                self.attached_to,
                self.fault,
                self.deleted,
                self.created_at,
                self.updated_at,
                self.deleted_at))


class OperationLog(Base, JsonObj):
    __tablename__ = 'operation_log'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    user_id = Column(Integer)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    resource_uuid = Column(String(100))
    event = Column(String(2000))
    occurred_at = Column(DateTime)

    def __init__(self, user_id=0, resource_type='', resource_id=0, resource_uuid='', 
                 event='', occurred_at='0000-00-00 00:00:00'):
        self.user_id = user_id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.resource_uuid = resource_uuid
        self.event = event
        self.occurred_at = occurred_at

    def __repr__(self):
        return("<OperationLog(%d, '%s', %d, '%s', '%s', %d)>"
             % (self.user_id,
                self.resource_type,
                self.resource_id,
                self.resource_uuid,
                self.event,
                self.occurred_at))


class NovaNotification(Base, JsonObj):
    __tablename__ = 'nova_notification'
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    message_id = Column(String(100), unique=True)
    event_type = Column(String(100))
    instance_id = Column(String(100))
    state = Column(String(100))
    old_state = Column(String(100))
    new_task_state = Column(String(100))
    old_task_state = Column(String(100))
    occurred_at = Column(DateTime)

    def __init__(self, message_id='', event_type='', instance_id='', 
                 state='', old_state='', new_task_state='', old_task_state='',
                 occurred_at='0000-00-00 00:00:00'):
        self.message_id = message_id
        self.event_type = event_type
        self.instance_id = instance_id,
        self.state = state,
        self.old_state = old_state,
        self.new_task_state = new_task_state,
        self.old_task_state = old_task_state,
        self.occurred_at = occurred_at

    def __repr__(self):
        return("<NovaNotification(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>"
             % (self.id,
                self.message_id,
                self.event_type, 
                self.instance_id,
                self.state,
                self.old_state,
                self.new_task_state,
                self.old_task_state,
                self.occurred_at))


class CinderNotification(Base, JsonObj):
    __tablename__ = 'cinder_notification'
    id =  Column(Integer, Sequence('seq_pk'), primary_key=True)
    message_id = Column(String(100), unique=True)
    event_type = Column(String(100))
    volume_id = Column(String(100))
    status = Column(String(100))
    occurred_at = Column(DateTime)

    def __init__(self, message_id='', event_type='', volume_id='', status='',
                 occurred_at='0000-00-00 00:00:00'):
        self.message_id = message_id
        self.event_type = event_type
        self.volume_id = volume_id
        self.status = status
        self.occurred_at = occurred_at

    def __repr__(self):
        return("<CinderNotification(%d, '%s', '%s', '%s', '%s', '%s')>"
             % (self.id, 
                self.message_id,
                self.event_type,
                self.volume_id,
                self.status,
                self.occurred_at))


class GlanceNotification(Base, JsonObj):
    __tablename__ = 'glance_notification'
    id =  Column(Integer, Sequence('seq_pk'), primary_key=True)
    message_id = Column(String(100), unique=True)
    event_type = Column(String(100))
    snapshot_id = Column(String(100))
    status = Column(String(100))
    occurred_at = Column(DateTime)

    def __init__(self, message_id='', event_type='', snapshot_id='', status='',
                 occurred_at='0000-00-00 00:00:00'):
        self.message_id = message_id
        self.event_type = event_type
        self.snapshot_id = snapshot_id
        self.status = status
        self.occurred_at = occurred_at

    def __repr__(self):
        return("<GlanceNotification(%d, '%s', '%s', '%s', '%s', '%s')>"
             % (self.id,
                self.message_id,
                self.event_type,
                self.snapshot_id,
                self.status,
                self.occurred_at))


class Snapshot(Base, JsonObj):
    """Snapshot in OpenStack"""
    __tablename__ = 'snapshot'
    id =  Column(Integer, Sequence('seq_pk'), primary_key=True)
    creator = Column(Integer)   # Who created this volume
    owner = Column(Integer)     # Currently who own this volume
    dept = Column(Integer)
    name = Column(String(100), nullable=False)
    snapshot_id = Column(String(100), nullable=False)
    server_id = Column(Integer)
    status = Column(String(100))
    size = Column(Integer)
    fault = Column(String(500))
    deleted = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def __init__(self, creator=0, owner=0, dept=0, name='', snapshot_id='', server_id=0, status='',
                 size=0, fault='', deleted=0, 
                 created_at='0000-00-00 00:00:00',
                 updated_at='0000-00-00 00:00:00',
                 deleted_at='0000-00-00 00:00:00'):
        self.creator = creator
        self.owner = owner
        self.dept = dept
        self.name = name
        self.snapshot_id = snapshot_id
        self.server_id = server_id
        self.status = status
        self.size = size
        self.fault = fault
        self.deleted = deleted
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return("<Snapshot(%d, %d, %d, %d, '%s', '%s', %d, '%s', %d, '%s', %d, '%s', '%s', '%s')>" 
             % (self.id,
                self.creator,
                self.owner,
                self.dept,
                self.name,
                self.snapshot_id,
                self.server_id,
                self.status,
                self.size,
                self.fault,
                self.deleted,
                self.created_at,
                self.updated_at,
                self.deleted_at))
