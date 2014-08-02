#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bottle import Bottle, run
from paste import httpserver

import time

app = Bottle()

@app.route('/hello')
def hello():
    time.sleep(1)
    return "Hello World!"

#run(app, host='0.0.0.0', port=8080)
httpserver.serve(app, host='0.0.0.0', port=8080)
