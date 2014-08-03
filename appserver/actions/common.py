import logging
from bottle import request
from model import Token
import utils
import datetime
import global_variables as gl

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
    remove_expired_token(db)

    token = request.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first() 
    if result:
        if result.expires > datetime.datetime.now():
            return True 
    return False


def remove_expired_token(db):
    now = datetime.datetime.now()
    # Try to clean expired token every hour
    if now - gl.time_clean_expired_token > datetime.timedelta(seconds=3600):
        db.query(Token).filter(Token.expires < now).delete()
        gl.time_clean_expired_token = now

    
def check_permission(request, db):
    pass


def get_userid_by_token(db):
    token = request.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first()
    if result:
        return result.user_id
    return None 
