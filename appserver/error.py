from bottle import HTTPError


class TokenNotFoundError(HTTPError):
    def __init__(self, token_id):
        message = "Could not find token '%s'" % token_id
        super(TokenNotFoundError, self).__init__(404, message)


class TokenExpiredError(HTTPError):
    def __init__(self, token_id):
        message = "Token '%s' expired" % token_id
        super(TokenExpiredError, self).__init__(403, message)
