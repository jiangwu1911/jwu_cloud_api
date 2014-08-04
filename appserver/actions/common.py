import logging
from model import Token
from model import UserRoleMembership
from model import Permission
import utils
import datetime
import global_variables as gl

from error import TokenNotFoundError
from error import TokenExpiredError

log = logging.getLogger("cloudapi")

def pre_check(func):
    def _deco(req, db):
        verify_token(req, db);

        if check_permission(req, db) == False:
            return {'error': "You don't have permission"}

        ret = func(req, db)
        return ret
    return _deco


def verify_token(req, db):
    remove_expired_token(db)

    token = req.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first() 

    if result == None:
        raise TokenNotFoundError(token)

    if result.expires < datetime.datetime.now():
        raise TokenExpiredError(token)

    return True 


def remove_expired_token(db):
    now = datetime.datetime.now()
    # Try to clean expired token every hour
    if now - gl.time_clean_expired_token > datetime.timedelta(seconds=3600):
        db.query(Token).filter(Token.expires < now).delete()
        gl.time_clean_expired_token = now

    
def check_permission(req, db):
    user_id = get_userid_by_token(req, db)
    membership = db.query(UserRoleMembership).filter(UserRoleMembership.user_id==user_id).first()
    if membership == None:
        return False

    permissions = db.query(Permission).filter_by(role_id=membership.role_id,
                                                 method=req.method)
    for p in permissions:
        import re
        p = re.compile(p.path)
        if p.match(req.path):
            return True
            
    return False
    

def get_userid_by_token(req, db):
    token = req.get_header('X-Auth-Token')
    result = db.query(Token).filter(Token.id==token).first()
    if result:
        return result.user_id
    return None 
