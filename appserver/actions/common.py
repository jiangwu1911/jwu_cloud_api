import logging
from bottle import request
import model
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

    token = request.get_header('X-Auth-Token');
    result = db.query(model.Token).filter_by(id=token).first() 
    if result:
        if result.expires > datetime.datetime.now():
            return True 
    return False


def remove_expired_token(db):
    now = datetime.datetime.now()
    # Try to clean expired token every hour
    if now - gl.time_clean_expired_token > datetime.timedelta(seconds=3600):
        db.query(model.Token).filter(model.Token.expires < now).delete()
        gl.time_clean_expired_token = now

    
def check_permission(request, db):
    pass
