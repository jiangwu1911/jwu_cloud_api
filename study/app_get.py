#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bottle import Bottle, run
import time

app = Bottle()

@app.route('/hello/:name')
def hello(name = 'World'):
    return 'Hello {0}!'.format(name) 

run(app, host='0.0.0.0', port=8080)
