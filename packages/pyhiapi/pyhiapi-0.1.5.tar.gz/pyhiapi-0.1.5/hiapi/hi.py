#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import flask

RESPONSE_CODE = 200
RESPONSE_MESSAGE = 'Hi!\n'

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def hello(path):
    global RESPONSE_CODE
    if RESPONSE_CODE == 200:
        return RESPONSE_MESSAGE
    else:
        flask.abort(RESPONSE_CODE)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind-address',
                        help='Address to bind the server to',
                        dest='bind', default='127.0.0.1')
    parser.add_argument('-c', '--config', default=None,
                        help='A file containing a custom response message')
    parser.add_argument('-p', '--port', dest='port', default=4000, type=int,
                        help='The port to listen on')
    parser.add_argument('-r', '--response_code', dest='code', default=200, type=int,
                        help='The response code to send back to requests')
    return parser.parse_args()

def main():
    global RESPONSE_CODE
    global RESPONSE_MESSAGE
    opts = parse_args()
    RESPONSE_CODE = opts.code

    if opts.config:
        try:
            with open(opts.config, 'r') as fh:
                RESPONSE_MESSAGE = fh.read()
        except IOError:
            print('Error: Could not read config file {}'.format(opts.config))

    app.run(host=opts.bind, port=opts.port)

if __name__ == "__main__":
    main()
