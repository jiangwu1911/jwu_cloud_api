# -*- coding: UTF-8 -*-

import logging
import logging.config
import sys

import bottle
from bottle import Bottle, run, response
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from paste import httpserver

import settings as conf
import model
import urls
import data
from notification import NovaNotifyListener
from notification import CinderNotifyListener
from notification import GlanceNotifyListener

VERSION ="0.1"

reload(sys)
sys.setdefaultencoding('utf-8')


bottle.ERROR_PAGE_TEMPLATE = """{"error": {"message": "{{e.body}}", "code": "{{e._status_code}}"}}"""


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
                          echo=False)

def install_db_plugin(app):
    engine = create_db_engine()
    create_session = sessionmaker(bind=engine)
    plugin = SQLAlchemyPlugin(engine, 
                              model.Base.metadata, 
                              create=True,
                              commit=False,
                              create_session=create_session)
    app.install(plugin)


def start_server():
    init_log()
    app = Bottle()
    install_db_plugin(app)
    urls.define_route(app)
    httpserver.serve(app, host=conf.listen_ip, port=conf.listen_port)


def start_notify_listener():
    engine = create_db_engine()

    nova_listener = NovaNotifyListener(engine)
    nova_listener.start()

    cinder_listener = CinderNotifyListener(engine)
    cinder_listener.start()

    glance_listener = GlanceNotifyListener(engine)
    glance_listener.start()


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

    start_notify_listener()
    start_server()


if __name__ == "__main__":
    main()
