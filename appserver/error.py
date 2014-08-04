from bottle import HTTPError


# ----- Basic -----
class EmptyVariableError(HTTPError):
    def __init__(self, varname):
        msg = "%s cannot be empty" % varname
        super(EmptyVariableError, self).__init__(400, msg)


# ----- Auth related -----
class UserNotFoundError(HTTPError):
    def __init__(self, username):
        msg = "User %s not found" % username
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


# ----- Dept related -----
class DeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "Dept %s not found or do not have permission" % dept_id
        super(DeptNotFoundError, self).__init__(404, msg)


class DeptAlreadyExistError(HTTPError):
    def __init__(self, dept_id):
        msg = "Dept %s already exist" % dept_id
        super(DeptAlreadyExistError, self).__init__(400, msg)


class ParentDeptNotFoundError(HTTPError):
    def __init__(self, dept_id):
        msg = "Parent dept %s not found" % dept_id
        super(ParentDeptNotFoundError, self).__init__(400, msg)


class CannotModifyDeptError(HTTPError):
    def __init__(self, dept_id):
        msg = "You don't have permission to modify %s" % dept_id
        super(CannotModifyDeptError, self).__init__(403, msg)


class DeptNotEmpty(HTTPError):
    def __init__(self, dept_id):
        msg = "Dept %s is not empty" % dept_id
        super(DeptNotEmpty, self).__init__(400, msg)
