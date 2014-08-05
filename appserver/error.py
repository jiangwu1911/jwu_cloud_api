from bottle import HTTPError


# ----- Basic -----
class EmptyVariableError(HTTPError):
    def __init__(self, varname):
        msg = "'%s' cannot be empty" % varname
        super(EmptyVariableError, self).__init__(400, msg)


# ----- Auth related -----
class UserNotFoundError(HTTPError):
    def __init__(self, username):
        msg = "User '%s' not found" % username
        super(UserNotFoundError, self).__init__(403, msg)


class WrongPasswordError(HTTPError):
    def __init__(self):
        msg = "Error password"
        super(WrongPasswordError, self).__init__(403, msg)


class TokenNotFoundError(HTTPError):
    def __init__(self, token_id):
        msg = "Could not find token '%s'" % token_id
        super(TokenNotFoundError, self).__init__(401, msg)


class TokenExpiredError(HTTPError):
    def __init__(self, token_id):
        msg = "Token '%s' expired" % token_id
        super(TokenExpiredError, self).__init__(401, msg)


class PermissionDenyError(HTTPError):
    def __init__(self):
        msg = "You don't have permission"
        super(PermissionDenyError, self).__init__(403, msg)


#----- Dept related -----
class DeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "Dept '%s' not found or do not have permission" % dept_id
        super(DeptNotFoundError, self).__init__(404, msg)


class DeptAlreadyExistError(HTTPError):
    def __init__(self, dept_name):
        msg = "Dept '%s' already exist" % dept_name
        super(DeptAlreadyExistError, self).__init__(400, msg)


class ParentDeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "Parent dept '%s' not found" % dept_id
        super(ParentDeptNotFoundError, self).__init__(404, msg)


class NotDeptAdminError(HTTPError):
    def __init__(self, dept_id):
        msg = "You don't have permission to operate dept '%s'" % dept_id
        super(NotDeptAdminError, self).__init__(403, msg)


class DeptNotEmpty(HTTPError):
    def __init__(self, dept_id):
        msg = "Dept '%s' is not empty" % dept_id
        super(DeptNotEmpty, self).__init__(400, msg)


#----- User related -----
class UserNotFoundError(HTTPError):
    def __init__(self, user_id):
        msg = "User '%s' not found or do not have permission" % user_id
        super(UserNotFoundError, self).__init__(404, msg)


class UsernameAlreadyExistError(HTTPError):
    def __init__(self, username):
        msg = "Username '%s' already exist" % username
        super(UsernameAlreadyExistError, self).__init__(400, msg)


class EmailAlreadyExistError(HTTPError):
    def __init__(self, email):
        msg = "Email '%s' already exist" % email
        super(EmailAlreadyExistError, self).__init__(400, msg)


class RolePermissionDenyError(HTTPError):
    def __init__(self, role_id):
        msg = "You don't have permission to assign role '%s' to user" % (role_id)
        super(RolePermissionDenyError, self).__init__(403, msg)


#----- OpenStack related -----
class CannotConnectToOpenStackError(HTTPError):
    def __init__(self):
        msg = "Cannot connect to OpenStack server"
        super(CannotConnectToOpenStackError, self).__init__(500, msg)


class FlavorNotFoundError(HTTPError):
    def __init__(self, flavor):
        msg = "Cannot find flavor '%s'" % flavor
        super(FlavorNotFoundError, self).__init__(403, msg)


class ImageNotFoundError(HTTPError):
    def __init__(self, image):
        msg = "Cannot find image '%s'" % image
        super(ImageNotFoundError, self).__init__(403, msg)


class ServerNotFoundError(HTTPError):
    def __init__(self, server):
        msg = "Cannot find server '%s'" % server
        super(ServerNotFoundError, self).__init__(403, msg)
