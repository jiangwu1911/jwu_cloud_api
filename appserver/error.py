from bottle import HTTPError


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
