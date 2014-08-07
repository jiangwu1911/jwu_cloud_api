import logging
from model import User
from model import Token
import datetime
import utils

import settings as conf
from error import UserNotFoundError
from error import WrongPasswordError
from common import get_required_input


log = logging.getLogger("cloudapi")


def login(req, db):
    username = get_required_input(req, 'username')
    password = get_required_input(req, 'password')
    if check_login(db, username, password):
        token = generate_token(db, username)
        return {'success': {'token': token.id}}
    

def check_login(db, username='', password=''):
    user = db.query(User).filter(User.name==username).first()
    if user == None:
        raise UserNotFoundError(username)
    if user.password != password:
        raise UserNotFoundError(username)
    return True


def generate_token(db, username):
    token = Token()
    user = db.query(User).filter(User.name==username).first()
    token.id = _generate_uuid_token()
    token.expires = datetime.datetime.now() + datetime.timedelta(seconds=conf.token_expires)
    token.user_id = user.id
    db.add(token)
    db.commit()
    return token


def _generate_uuid_token():
    return utils.get_uuid()


def logout(req, db):
    token = req.get_header('X-Auth-Token')
    db.query(Token).filter(Token.id==token).delete()
    db.commit()
    return {'success': 'token deleted.'}
