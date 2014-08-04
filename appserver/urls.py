from bottle import route, get, post, delete, request, response

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

    @app.post('/dept/:dept_id')
    def update_dept(db, dept_id):
        response.content_type = "application/json"
        return dept.update_dept(request, db, dept_id)

    @app.delete('/dept/:dept_id')
    def delete_dept(db, dept_id):
        response.content_type = "application/json"
        return dept.delete_dept(request, db, dept_id)

    #----- user related -----
    @app.get('/user')
    def list_user(db):
        response.content_type = "application/json"
        return user.list_user(request, db)

    @app.get('/user/:user_id')
    def show_user(db, user_id):
        response.content_type = "application/json"
        return user.show_user(request, db, user_id)

    @app.post('/user')
    def add_user(db):
        response.content_type = "application/json"
        return user.add_user(request, db)

    @app.post('/user/:user_id')
    def update_user(db, user_id):
        response.content_type = "application/json"
        return user.update_user(request, db, user_id)

    @app.delete('/user/:user_id')
    def delete_user(db, user_id):
        response.content_type = "application/json"
        return user.delete_user(request, db, user_id)
