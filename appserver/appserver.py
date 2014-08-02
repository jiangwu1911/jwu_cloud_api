#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import logging.config

from bottle import Bottle, run
from bottle import get, post, request
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine
from paste import httpserver

import settings as conf
import model
import auth 


def init_log():
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("cloudapi")


def install_db_plugin(app):
    engine = create_engine('mysql://%s:%s@%s/%s?charset=%s' % 
                           (conf.db_config['user'],
                            conf.db_config['passwd'],
                            conf.db_config['host'],
                            conf.db_config['db'],
                            conf.db_config['charset']),
                            echo=True)

    plugin = SQLAlchemyPlugin(engine, 
                              model.Base.metadata, 
                              create=True,
                              commit=True)
    app.install(plugin)


init_log()
app = Bottle()
install_db_plugin(app)

#@route('/login', method = 'POST')
@app.post('/login')
def login(db):
    return auth.login(request, db)

httpserver.serve(app, host=conf.listen_ip, port=conf.listen_port)
