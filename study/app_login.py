#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import logging.config
from bottle import Bottle, run
from paste import httpserver
from bottle import get, post, request


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("example") 

app = Bottle()


#@route('/login')
@app.get('/login')
def login_form():
    return '''<form method = "POST">
                <input name="name" type="text" />
                <input name="password" type="password" />
                <input type="submit" value="Login" />
                </form>'''


#@route('/login', method = 'POST')
@app.post('/login')
def login():
    name = request.forms.get('name')
    password = request.forms.get('password')
    if check_login(name, password):
        return '<p>Your login was correct</p>'
    else:
        logger.info("bad password, username is " + name)
        return '<p>Login failed</p>'


def check_login(name, password):
    return False


#run(app, host='0.0.0.0', port=8080)
httpserver.serve(app, host='0.0.0.0', port=8080)
