import logging
from model import User
from model import Token
import datetime
import utils

import settings as conf
from error import UserNotFoundError
from error import WrongPasswordError

log = logging.getLogger("cloudapi")


def login(req, db):
    username = req.forms.get('username')
    password = req.forms.get('password')
    if check_login(db, username, password):
        token = generate_token(db, username)
        return {'success': {'token': token.id}}
    

def check_login(db, username='', password=''):
    user = db.query(User).filter(User.name==username).first()
    if user == None:
        raise UserNotFoundError(username)

    if user.password != password:
        raise WrongPasswordError()
    
    return True


def generate_token(db, username):
    token = Token()
    user = db.query(User).filter(User.name==username).first()
    token.id = _generate_uuid_token()
    token.expires = datetime.datetime.now() + datetime.timedelta(seconds=conf.token_expires)
    token.user_id = user.id
    db.add(token)
    return token


def _generate_uuid_token():
    return utils.get_uuid()
