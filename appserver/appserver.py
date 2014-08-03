# -*- coding: UTF-8 -*-

import logging
import logging.config
import sys

from bottle import Bottle, run
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine
from paste import httpserver

import settings as conf
import model
import urls
import data


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


def start_server():
    init_log()
    app = Bottle()
    install_db_plugin(app)
    urls.define_route(app)
    httpserver.serve(app, host=conf.listen_ip, port=conf.listen_port)


def init_db(testdata=False):
    answer = raw_input("Do you really want to destroy all data in database: (yes|no)? ")
    if answer == "yes":
        engine = create_db_engine()
        model.Base.metadata.drop_all(engine)
        model.Base.metadata.create_all(engine)
        data.insert_basic_data(engine)
        
        if testdata == True:
            data.insert_test_data(engine) 


def main():
    from optparse import OptionParser

    usage = "Usage: %prog [options]"
    parser = OptionParser(usage, version=VERSION)

    parser.add_option("-i", "--initdb", action="store_true", 
                      dest="initdb", 
                      default=False, 
                      help="initialize database, remove all data") 

    parser.add_option("--initdb_with_test_data", action="store_true", 
                      dest="testdata", 
                      default=False, 
                      help="initialize database and insert test data into database") 

    options, args = parser.parse_args()
    
    if options.initdb:
        init_db()
        sys.exit(0)

    if options.testdata:
        init_db(True)
        sys.exit(0) 
    
    start_server()


if __name__ == "__main__":
    main()
