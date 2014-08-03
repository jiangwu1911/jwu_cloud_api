import logging
from bottle import request
import model
import utils

log = logging.getLogger("cloudapi")

def pre_check(func):
    def _deco(request, db):

        if verify_token(request, db) == False:
            return {'error': 'Invalid token.'}

        check_permission(request, db)

        ret = func(request, db)
        return ret
    return _deco


def verify_token(request, db):
    token = request.get_header('X-Auth-Token');
    result = db.query(model.Token).filter_by(id=token).first() 
    print result
    if result:
        return True 
    return False


def check_permission(request, db):
    pass
