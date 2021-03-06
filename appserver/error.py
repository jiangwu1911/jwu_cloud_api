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


class UploadFolderNotSetError(HTTPError):
    def __init__(self, msg):
        msg = "服务器没有设置上传目录" 
        super(UploadFolderNotSetError, self).__init__(500, msg)


# ----- Auth related -----
class UserNotFoundOrPasswordError(HTTPError):
    def __init__(self, username):
        msg = "用户名不存在，或密码错误。"
        super(UserNotFoundOrPasswordError, self).__init__(403, msg)


class TokenNotFoundError(HTTPError):
    def __init__(self, token_id):
        msg = "Token不存在。"
        super(TokenNotFoundError, self).__init__(401, msg)


class TokenNotProvidedError(HTTPError):
    def __init__(self):
        msg = "请求中没有包含Token。"
        super(TokenNotProvidedError, self).__init__(401, msg)


class TokenExpiredError(HTTPError):
    def __init__(self, token_id):
        msg = "Token已过期。"
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
        msg = "部门不存在，或无权访问该部门。"
        super(DeptNotFoundError, self).__init__(404, msg)


class DeptAlreadyExistError(HTTPError):
    def __init__(self, dept_name):
        msg = "部门名称已存在。"
        super(DeptAlreadyExistError, self).__init__(400, msg)


class ParentDeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "上级部门不存在。"
        super(ParentDeptNotFoundError, self).__init__(404, msg)


class NotDeptAdminError(HTTPError):
    def __init__(self, dept_id):
        msg = "无权操作部门。"
        super(NotDeptAdminError, self).__init__(403, msg)


class DeptNotEmptyError(HTTPError):
    def __init__(self, dept_id):
        msg = "部门内部还有用户，无法删除。"
        super(DeptNotEmptyError, self).__init__(400, msg)


class ParentCannotBeSelfError(HTTPError):
    def __init__(self, dept_id):
        msg = "部门的上级部门不能是自己。"
        super(ParentCannotBeSelfError, self).__init__(400, msg)


class DeptHasChildrenError(HTTPError):
    def __init__(self, dept_id):
        msg = "部门下面有子部门，无法删除。"
        super(DeptHasChildrenError, self).__init__(400, msg)


class CannotDeleteHeadDeptError(HTTPError):
    def __init__(self, dept_id):
        msg = "不允许删除总部。"
        super(CannotDeleteHeadDeptError, self).__init__(400, msg)


#----- User related -----
class UserNotFoundError(HTTPError):
    def __init__(self, user_id):
        msg = "用户不存在。"
        super(UserNotFoundError, self).__init__(404, msg)


class UsernameAlreadyExistError(HTTPError):
    def __init__(self, username):
        msg = "用户名已存在。"
        super(UsernameAlreadyExistError, self).__init__(400, msg)


class EmailAlreadyExistError(HTTPError):
    def __init__(self, email):
        msg = "Email已存在。"
        super(EmailAlreadyExistError, self).__init__(400, msg)


class RolePermissionDenyError(HTTPError):
    def __init__(self, role_id):
        msg = "无权把角色授权给用户。"
        super(RolePermissionDenyError, self).__init__(403, msg)


class CannotModifyAdminError(HTTPError):
    def __init__(self):
        msg = "不允许修改缺省系统管理员admin的部门和权限。"
        super(CannotModifyAdminError, self).__init__(403, msg)


class CannotDeleteSelfError(HTTPError):
    def __init__(self):
        msg = "用户不能删除自己。"
        super(CannotDeleteSelfError, self).__init__(400, msg)


class CannotDeleteUserWhoHasResourceError(HTTPError):
    def __init__(self):
        msg = "用户名下有云主机等资源，请先将资源转移给其它员工。"
        super(CannotDeleteUserWhoHasResourceError, self).__init__(400, msg)


#----- OpenStack server related -----
class CannotConnectToOpenStackError(HTTPError):
    def __init__(self):
        msg = "无法连接到OpenStack。"
        super(CannotConnectToOpenStackError, self).__init__(500, msg)


class OpenStackError(HTTPError):
    def __init__(self, error):
        msg = "OpenStack错误: %s" % error
        super(OpenStackError, self).__init__(500, msg)


class FlavorNotFoundError(HTTPError):
    def __init__(self, flavor):
        msg = "云主机类型'%s'不存在。" % flavor
        super(FlavorNotFoundError, self).__init__(404, msg)


class FlavorAlreadyExistError(HTTPError):
    def __init__(self, flavor):
        msg = "云主机类型'%s'已存在。" % flavor
        super(FlavorAlreadyExistError, self).__init__(400, msg)


class ImageNotFoundError(HTTPError):
    def __init__(self, image):
        msg = "镜像'%s'不存在。" % image
        super(ImageNotFoundError, self).__init__(404, msg)


class ServerNotFoundError(HTTPError):
    def __init__(self):
        msg = "云主机不存在。" 
        super(ServerNotFoundError, self).__init__(404, msg)


class UnsupportedOperationError(HTTPError):
    def __init__(self, operation):
        msg = "'%s'操作不支持。" % operation
        super(UnsupportedOperationError, self).__init__(400, msg)


#----- OpenStack volume related -----
class VolumeNotFoundError(HTTPError):
    def __init__(self, volume):
        msg = "云硬盘不存在。"
        super(VolumeNotFoundError, self).__init__(404, msg)


#----- OpenStack snapshot related -----
class SnapshotNotFoundError(HTTPError):
    def __init__(self, snapshot):
        msg = "快照不存在。"
        super(SnapshotNotFoundError, self).__init__(404, msg)


#----- OpenStack image related -----
class ImageUploadError(HTTPError):
    def __init__(self, error):
        msg = "上传文件错误: %s" % error
        super(ImageUploadError, self).__init__(400, msg)


#----- Monitor server (ElasticSearch) error -----
class MonitorServerError(HTTPError):
    def __init__(self, error):
        msg = "监控服务器错误: %s" % error
        super(MonitorServerError, self).__init__(500, msg)

class MonitorDataTypeNotSupportedError(HTTPError):
    def __init__(self, data_type):
        msg = "监控数据类型 %s 不支持" % data_type
        super(MonitorDataTypeNotSupportedError, self).__init__(400, msg)

class MonitorDataNotFoundError(HTTPError):
    def __init__(self):
        msg = "未找到监控数据"
        super(MonitorDataNotFoundError, self).__init__(400, msg)
