# -*- coding: UTF-8 -*-

from bottle import route, get, post, delete, request, response

from actions import auth
from actions import user
from actions import dept
from actions import openstack
import model
import utils

def define_route(app):
    @app.route('/:path', method='OPTIONS')
    def options(path):
        # 允许跨域访问
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
                        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
 
    @app.post('/login')
    def login(db):
        response.content_type = "application/json"
        return auth.login(request, db)

    @app.post('/logout')
    def logout(db):
        response.content_type = "application/json"
        return auth.logout(request, db)

    #----- dept related -----
    @app.get('/depts')
    def list_dept(db):
        return dept.list_dept(request, db)

    @app.get('/depts/:dept_id')
    def show_dept(db, dept_id):
        return dept.show_dept(request, db, dept_id)

    @app.post('/depts')
    def add_dept(db):
        return dept.add_dept(request, db)

    @app.post('/depts/:dept_id')
    def update_dept(db, dept_id):
        return dept.update_dept(request, db, dept_id)

    @app.delete('/depts/:dept_id')
    def delete_dept(db, dept_id):
        return dept.delete_dept(request, db, dept_id)

    #----- user related -----
    @app.get('/users')
    def list_user(db):
        return user.list_user(request, db)

    @app.get('/users/:user_id')
    def show_user(db, user_id):
        return user.show_user(request, db, user_id)

    @app.post('/users')
    def add_user(db):
        return user.add_user(request, db)

    @app.post('/users/:user_id')
    def update_user(db, user_id):
        return user.update_user(request, db, user_id)

    @app.delete('/users/:user_id')
    def delete_user(db, user_id):
        return user.delete_user(request, db, user_id)

    #------ OpenStack related -----
    @app.get('/flavors')
    def list_flavor(db):
        return openstack.list_flavor(request, db)
 
    @app.get('/images')
    def list_image(db):
        return openstack.list_image(request, db)
 
    @app.get('/servers')
    def list_server(db):
        return openstack.list_server(request, db)

    @app.get('/servers/:server_id')
    def show_server(db, server_id):
        return openstack.show_server(request, db, server_id)

    @app.post('/servers')
    def list_server(db):
        return openstack.create_server(request, db)

    @app.post('/servers/:server_id')
    def update_server(db, server_id):
        return openstack.update_server(request, db, server_id)

    @app.delete('/servers/:server_id')
    def delete_server(db, server_id):
        return openstack.delete_server(request, db, server_id)

