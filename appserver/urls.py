from bottle import route, get, post, request, response

from actions import auth
from actions import user
from actions import dept
import model
import json
import utils

def define_route(app):
    @app.post('/login')
    def login(db):
        response.content_type = "application/json"
        return auth.login(request, db)

    @app.get('/user')
    def list_user(db):
        response.content_type = "application/json"
        return user.list_user(request, db)

    #----- dept related -----
    @app.get('/dept')
    def list_dept(db):
        response.content_type = "application/json"
        return dept.list_dept(request, db)

    @app.get('/dept/:dept_id')
    def show_dept(db, dept_id):
        response.content_type = "application/json"
        return dept.show_dept(request, db, dept_id)

    @app.post('/dept')
    def add_dept(db):
        response.content_type = "application/json"
        return dept.add_dept(request, db)
