#import pandas
#! /usr/bin/python
import VCToolTest
from Install import *
import os
from inspect import getsourcefile

i = Install()
i.installPackages()

import flask

DEBUG = True
CODE_ROOT = os.path.dirname(os.path.abspath(getsourcefile(lambda:0)))
HTML_ROOT = os.path.abspath(os.path.join(CODE_ROOT, "./html/build"))
print("Code Root: " + CODE_ROOT)
print("HTML Root: " + HTML_ROOT)


server = flask.Flask("server", static_url_path='', static_folder=HTML_ROOT)

SETTINGS = {"host": "127.0.0.1", "port": 8888}


@server.route('/')
def html_root():
    return server.send_static_file('index.html')

@server.route('/status')
def status():
    return 'OK'

@server.route('/v1/test')
def testRun():
    result = VCToolTest.doit(*VCToolTest.manualOverride())
    return flask.jsonify(result)

def createServer(host="127.0.0.1", port=8888):
    server.run(debug=DEBUG, use_reloader=False, host=host, port=port, threaded=True)


def run():
    createServer()



if __name__ == '__main__':
    run()