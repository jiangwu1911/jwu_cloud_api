import logging
from bottle import get, post, request
import model

log = logging.getLogger("cloudapi")


def login(request, db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(db, username, password):
        return '<p>Your login was correct</p>'
    else:
        return '<p>Login failed</p>'


def check_login(db, username='', password=''):
    user = db.query(model.User).filter_by(name=username).first()
    if user == None:
        log.debug('Cannot find user %s.' % username)
        return False

    if user.password != password:
        log.debug('Wrong password. Username:%s, Password:%s'
                  % (username, password))
        return False
    
    return True
