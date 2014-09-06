# -*- coding: UTF-8 -*-

from bottle import route, get, post, delete, request, response, hook

from actions import auth
from actions import user
from actions import dept
from actions import openstack
import model
import utils


def define_route(app):
    @app.hook('after_request')
    def enable_cors():
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
        response.headers['Access-Control-Allow-Headers'] = \
                    'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, X-Auth-Token'

    @app.route('/:path', method=['OPTIONS'])
    def options(path):
        # 允许跨域访问
        pass
        
    @app.route('/:path/:id', method=['OPTIONS'])
    def options(path, id):
        # 允许跨域访问
        pass
        

    #---------- auth related ----------
    @app.post('/login')
    def login(db):
        response.content_type = "application/json"
        return auth.login(request, db)

    @app.post('/logout')
    def logout(db):
        response.content_type = "application/json"
        return auth.logout(request, db)

    @app.get('/roles')
    def list_role(db):
        return auth.list_role(request, db)


    #---------- dept related ----------
    @app.get('/depts')
    def list_dept(db):
        return dept.list_dept(request, db)

    @app.get('/depts/:dept_id')
    def show_dept(db, dept_id):
        return dept.show_dept(request, db, dept_id)

    @app.post('/depts')
    def create_dept(db):
        return dept.create_dept(request, db)

    @app.post('/depts/:dept_id')
    def update_dept(db, dept_id):
        return dept.update_dept(request, db, dept_id)

    @app.delete('/depts/:dept_id')
    def delete_dept(db, dept_id):
        return dept.delete_dept(request, db, dept_id)


    #---------- user related ----------
    @app.get('/users')
    def list_user(db):
        return user.list_user(request, db)

    @app.get('/users/:user_id')
    def show_user(db, user_id):
        return user.show_user(request, db, user_id)

    @app.post('/users')
    def create_user(db):
        return user.create_user(request, db)

    @app.post('/users/:user_id')
    def update_user(db, user_id):
        return user.update_user(request, db, user_id)

    @app.delete('/users/:user_id')
    def delete_user(db, user_id):
        return user.delete_user(request, db, user_id)


    #----------- OpenStack flavor related ----------
    @app.get('/flavors')
    def list_flavor(db):
        return openstack.list_flavor(request, db)
 
    @app.post('/flavors')
    def create_flavor(db):
        return openstack.create_flavor(request, db)
 
    @app.post('/flavors/:flavor_id')
    def update_flavor(db, flavor_id):
        return openstack.update_flavor(request, db, flavor_id)
 
    @app.delete('/flavors/:flavor_id')
    def create_flavor(db, flavor_id):
        return openstack.delete_flavor(request, db, flavor_id)


    #----------- OpenStack image related ----------
    @app.get('/images')
    def list_image(db):
        return openstack.list_image(request, db)
 

    #----------- OpenStack server related ----------
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
