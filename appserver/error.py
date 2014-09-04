# -*- coding: UTF-8 -*-

from bottle import HTTPError

# ----- Basic -----
class EmptyVariableError(HTTPError):
    def __init__(self, varname):
        msg = "'%s'字段不能为空。" % varname
        super(EmptyVariableError, self).__init__(400, msg)


class DatabaseError(HTTPError):
    def __init__(self, msg):
        msg = "数据库错误: %s。" % msg
        super(DatabaseError, self).__init__(500, msg)


# ----- Auth related -----
class UserNotFoundOrPasswordError(HTTPError):
    def __init__(self, username):
        msg = "用户'%s'不存在，或密码错误。" % username
        super(UserNotFoundOrPasswordError, self).__init__(403, msg)


class TokenNotFoundError(HTTPError):
    def __init__(self, token_id):
        msg = "Token '%s'不存在。" % token_id
        super(TokenNotFoundError, self).__init__(401, msg)


class TokenExpiredError(HTTPError):
    def __init__(self, token_id):
        msg = "Token '%s'已过期。" % token_id
        super(TokenExpiredError, self).__init__(401, msg)


class PermissionDenyError(HTTPError):
    def __init__(self):
        msg = "没有访问权限。"
        super(PermissionDenyError, self).__init__(403, msg)


class RoleNotFoundError(HTTPError):
    def __init__(self):
        msg = "权限定义不存在。"
        super(RoleNotFoundError, self).__init__(404, msg)


#----- Dept related -----
class DeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "部门'%s'不存在，或无权访问该部门。" % dept_id
        super(DeptNotFoundError, self).__init__(404, msg)


class DeptAlreadyExistError(HTTPError):
    def __init__(self, dept_name):
        msg = "部门'%s'已存在。" % dept_name
        super(DeptAlreadyExistError, self).__init__(400, msg)


class ParentDeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "上级部门'%s'不存在。" % dept_id
        super(ParentDeptNotFoundError, self).__init__(404, msg)


class NotDeptAdminError(HTTPError):
    def __init__(self, dept_id):
        msg = "无权操作部门'%s'。" % dept_id
        super(NotDeptAdminError, self).__init__(403, msg)


class DeptNotEmpty(HTTPError):
    def __init__(self, dept_id):
        msg = "部门'%s'内部还有用户，无法删除。" % dept_id
        super(DeptNotEmpty, self).__init__(400, msg)


#----- User related -----
class UserNotFoundError(HTTPError):
    def __init__(self, user_id):
        msg = "用户'%s'不存在。" % user_id
        super(UserNotFoundError, self).__init__(404, msg)


class UsernameAlreadyExistError(HTTPError):
    def __init__(self, username):
        msg = "用户名'%s'已存在。" % username
        super(UsernameAlreadyExistError, self).__init__(400, msg)


class EmailAlreadyExistError(HTTPError):
    def __init__(self, email):
        msg = "Email '%s'已存在。" % email
        super(EmailAlreadyExistError, self).__init__(400, msg)


class RolePermissionDenyError(HTTPError):
    def __init__(self, role_id):
        msg = "无权把角色'%s'授权给用户。" % (role_id)
        super(RolePermissionDenyError, self).__init__(403, msg)


#----- OpenStack related -----
class CannotConnectToOpenStackError(HTTPError):
    def __init__(self):
        msg = "无法连接到OpenStack。"
        super(CannotConnectToOpenStackError, self).__init__(500, msg)


class FlavorNotFoundError(HTTPError):
    def __init__(self, flavor):
        msg = "虚拟机类型'%s'不存在。" % flavor
        super(FlavorNotFoundError, self).__init__(403, msg)


class ImageNotFoundError(HTTPError):
    def __init__(self, image):
        msg = "镜像'%s'不存在。" % image
        super(ImageNotFoundError, self).__init__(403, msg)


class ServerNotFoundError(HTTPError):
    def __init__(self, server):
        msg = "虚拟机'%s'不存在。" % server
        super(ServerNotFoundError, self).__init__(403, msg)


class UnsupportedOperationError(HTTPError):
    def __init__(self, operation):
        msg = "'%s'操作不支持。" % operation
        super(UnsupportedOperationError, self).__init__(400, msg)
