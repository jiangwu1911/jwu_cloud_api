from bottle import route, get, post, request

import auth
import model
import json
import utils

def define_route(app):
    @app.post('/login')
    def login(db):
        return auth.login(request, db)

    @app.get('/user')
    def list_user(db):
        users = db.query(model.User)
        for user in users:
            return utils.JsonEncoder().encode(user)
