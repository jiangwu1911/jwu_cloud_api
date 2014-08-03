import logging
from bottle import request
import model
import datetime
import utils

import settings as conf

log = logging.getLogger("cloudapi")


def login(request, db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(db, username, password):
        token = generate_token(db, username)
        return {'success': {'token': token.id}}
    else:
        return {'error': 'Login failed.'}


def check_login(db, username='', password=''):
    user = db.query(model.User).filter_by(name=username).first()
    if user == None:
        log.debug('Cannot find user %s.' % username)
        return False

    if user.password != password:
        log.debug('Wrong password. Username:%s, Password:%s'
                  % (username, password))
        return False
    
    log.debug(user)
    return True


def generate_token(db, username):
    token = model.Token()
    user = db.query(model.User).filter_by(name=username).first()
    token.id = _generate_uuid_token()
    token.expires = datetime.datetime.now() + datetime.timedelta(seconds=conf.token_expires)
    token.user_id = user.id
    db.add(token)
    return token


def _generate_uuid_token():
    return utils.get_uuid()
