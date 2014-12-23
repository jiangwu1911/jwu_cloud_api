# -*- coding: UTF-8 -*-

from bottle import route, get, post, delete, request, response, hook, static_file, redirect

from actions import auth
from actions import user
from actions import dept
from actions.openstack import server
from actions.openstack import volume
from actions.openstack import snapshot
from actions.openstack import host
from actions.openstack import image
from actions.openstack import logserver
import model
import utils
import settings as conf


def define_route(app):
    @app.route('/')
    def server_index():
        redirect('/cloudapp/index.html')

    @app.route('/cloudapp/:path#.+#')
    def server_static(path):
        return static_file(path, root=conf.static_files_path)

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
        return server.list_flavor(request, db)
 
    @app.post('/flavors')
    def create_flavor(db):
        return server.create_flavor(request, db)
 
    @app.post('/flavors/:flavor_id')
    def update_flavor(db, flavor_id):
        return server.update_flavor(request, db, flavor_id)
 
    @app.delete('/flavors/:flavor_id')
    def create_flavor(db, flavor_id):
        return server.delete_flavor(request, db, flavor_id)


    #----------- OpenStack image related ----------
    @app.get('/images')
    def list_image(db):
        return image.list_image(request, db)

    @app.get('/images/:image_id')
    def show_image(db, image_id):
        return image.show_image(request, db, image_id)

    @app.post('/images')
    def create_image(db):
        return image.create_image(request, db)

    @app.post('/images/:image_id')
    def update_image(db, image_id):
        return image.update_image(request, db, image_id)

    @app.delete('/images/:image_id')
    def delete_image(db, image_id):
        return image.delete_image(request, db, image_id)
 

    #----------- OpenStack server related ----------
    @app.get('/servers')
    def list_server(db):
        return server.list_server(request, db)

    @app.get('/servers/:server_id')
    def show_server(db, server_id):
        return server.show_server(request, db, server_id)

    @app.post('/servers')
    def create_server(db):
        return server.create_server(request, db)

    @app.post('/servers/:server_id')
    def update_server(db, server_id):
        return server.update_server(request, db, server_id)

    @app.delete('/servers/:server_id')
    def delete_server(db, server_id):
        return server.delete_server(request, db, server_id)


    #---------- OpenStack Volume related ----------
    @app.get('/volumes')
    def list_volume(db):
        return volume.list_volume(request, db)

    @app.get('/volumes/:volume_id')
    def show_volume(db, volume_id):
        return volume.show_volume(request, db, volume_id)

    @app.post('/volumes')
    def list_volume(db):
        return volume.create_volume(request, db)

    @app.post('/volumes/:volume_id')
    def update_volume(db, volume_id):
        return volume.update_volume(request, db, volume_id)

    @app.delete('/volumes/:volume_id')
    def delete_volume(db, volume_id):
        return volume.delete_volume(request, db, volume_id)


    #---------- OpenStack Snapshot related ----------
    @app.get('/snapshots')
    def list_snapshot(db):
        return snapshot.list_snapshot(request, db)

    @app.get('/snapshots/:snapshot_id')
    def show_snapshot(db, snapshot_id):
        return snapshot.show_snapshot(request, db, snapshot_id)

    @app.post('/snapshots/:snapshot_id')
    def update_snapshot(db, snapshot_id):
        return snapshot.update_snapshot(request, db, snapshot_id)

    @app.delete('/snapshots/:snapshot_id')
    def delete_snapshot(db, snapshot_id):
        return snapshot.delete_snapshot(request, db, snapshot_id)


    #----------- OpenStack hypervisor related ----------
    @app.get('/hosts')
    def list_hypervisor(db):
        return host.list_hypervisor(request, db)

    #----------- View OpenStack logs ----------
    @app.get('/logs')
    def show_log_server_url(db):
        return logserver.show_log_server_url(request, db)
