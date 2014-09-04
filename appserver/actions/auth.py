import logging
import datetime

from model import User
from model import Token
from model import Role
from model import UserRoleMembership
import utils
import settings as conf
from error import UserNotFoundOrPasswordError
from error import RoleNotFoundError
from common import get_required_input


log = logging.getLogger("cloudapi")


def login(req, db):
    username = get_required_input(req, 'username')
    password = get_required_input(req, 'password')

    if check_login(db, username, password):
        user = db.query(User).filter(User.name==username).first()

        token = generate_token(db, user.id)

        user_role = db.query(UserRoleMembership).filter(UserRoleMembership.user_id==user.id).first()
        if user_role == None:
            raise RoleNotFoundError 
        role = db.query(Role).filter(Role.id==user_role.role_id).first()
        if role == None:
            raise RoleNotFoundError

        return {'success': {'token': token.id, 'role': utils.json_dumps(role)}}
    

def check_login(db, username='', password=''):
    user = db.query(User).filter(User.name==username).first()
    if user == None:
        raise UserNotFoundOrPasswordError(username)
    if user.password != password:
        raise UserNotFoundOrPasswordError(username)
    return True


def generate_token(db, user_id):
    token = Token()
    token.id = _generate_uuid_token()
    token.expires = datetime.datetime.now() + datetime.timedelta(seconds=conf.token_expires)
    token.user_id = user_id
    db.add(token)
    db.commit()
    return token


def _generate_uuid_token():
    return utils.get_uuid()


def delete_token(db, token):
    db.query(Token).filter(Token.id==token).delete()
    db.commit()

    
def logout(req, db):
    token = req.get_header('X-Auth-Token')
    delete_token(db, token)
    return {'success': 'token deleted.'}
