# -*- coding: UTF-8 -*-

import logging
import logging.config
import sys

from bottle import Bottle, run
from bottle import get, post, request
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine
from paste import httpserver

import settings as conf
import model
import auth 


VERSION ="0.1"


def init_log():
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("cloudapi")


def create_db_engine():
    return create_engine('mysql://%s:%s@%s/%s?charset=%s' %
                         (conf.db_config['user'],
                          conf.db_config['passwd'],
                          conf.db_config['host'],
                          conf.db_config['db'],
                          conf.db_config['charset']),
                          echo=True)

def install_db_plugin(app):
    engine = create_db_engine()
    plugin = SQLAlchemyPlugin(engine, 
                              model.Base.metadata, 
                              create=True,
                              commit=True)
    app.install(plugin)


def define_route(app):
    @app.post('/login')
    def login(db):
        return auth.login(request, db)


def start_server():
    init_log()
    app = Bottle()
    install_db_plugin(app)
    define_route(app)
    httpserver.serve(app, host=conf.listen_ip, port=conf.listen_port)


def init_db():
    answer = raw_input("Do you really want to destroy all data in database: (yes|no)?")
    if answer == "yes":
        engine = create_db_engine()
        model.Base.metadata.drop_all(engine)
        model.Base.metadata.create_all(engine)
        model.init_db(engine)


def main():
    from optparse import OptionParser

    usage = "Usage: %prog [options]"
    parser = OptionParser(usage, version=VERSION)
    parser.add_option("-i", "--initdb", action="store_true", 
                      dest="initdb", 
                      default=False, 
                      help="initialize database") 
    options, args = parser.parse_args()
    
    if options.initdb:
        init_db()
        sys.exit(0)
    
    start_server()


if __name__ == "__main__":
    main()
