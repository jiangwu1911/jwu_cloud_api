from bottle import route, get, post, request

from actions import auth
from actions import user
from actions import dept
import model
import json
import utils

def define_route(app):
    @app.post('/login')
    def login(db):
        return auth.login(request, db)

    @app.get('/user')
    def list_user(db):
        return user.list_user(request, db)

    @app.get('/dept')
    def list_dept(db):
        return dept.list_dept(request, db)

