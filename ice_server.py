#!/usr/bin/python
# coding: utf-8

# realXiaoice - server.py
# 2019/8/11 17:13
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import os
from platform import uname
import json
import traceback
from concurrent.futures import ThreadPoolExecutor
from tornado import web, ioloop, httpserver, gen, options
from tornado.concurrent import run_on_executor

from xiaoice import chat

ALLOWED_IPS = []


class BaseHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass


class IndexHandler(BaseHandler):
    def get(self):
        text = '''
        GET: http://127.0.0.1:6789/chat?text=hello
        POST:http://127.0.0.1:6789/chat, form-urlencoded or json with {"text":"hello"}
        Response: HTTP 200: {"text":"hi there", "debug":""}
                  Other : {"text":"", "debug":"error"}
        '''
        self.write(text)


class ChatHandler(BaseHandler):
    executor = ThreadPoolExecutor(max_workers=20)

    def accessibility(self, ip):
        if ALLOWED_IPS and ip not in ALLOWED_IPS:
            logging.warning('Access denied for {}'.format(ip))
            self.set_status(403)
            return {"text": "", "debug": "Access denied."}

    @run_on_executor
    def run_request(self):
        user_ip = self.request.headers.get("X-Real-IP", "") or self.request.remote_ip
        denied = self.accessibility(user_ip)
        if denied:
            return denied

        if self.request.method == 'GET':
            user_input = self.get_query_argument('text', None)
        elif self.request.headers.get('Content-Type') == 'application/json' and self.request.body:
            user_input = json.loads(self.request.body).get('text')
        elif self.request.method == 'POST':
            user_input = self.get_argument('text', None)
        else:
            user_input = None

        if user_input:
            try:
                response = {"text": chat(user_input), "debug": ""}
            except Exception as e:
                logging.error(traceback.format_exc())
                self.set_status(500)
                response = {"text": "", "debug": str(e)}
        else:
            self.set_status(400)
            response = {"text": "", "debug": "param text is missing"}
        return response

    @gen.coroutine
    def get(self):
        res = yield self.run_request()
        self.write(res)

    @gen.coroutine
    def post(self):
        res = yield self.run_request()
        self.write(res)


class RunServer:
    root_path = os.path.dirname(__file__)
    page_path = os.path.join(root_path, 'pages')

    handlers = [(r'/', IndexHandler),
                (r'/chat', ChatHandler),
                ]
    settings = {
        "cookie_secret": "5Li05DtnQewDZq1mDVB3HAAhFqUu2vD2USnqezkeu+M=",
        "xsrf_cookies": False,
        "autoreload": True
    }

    application = web.Application(handlers, **settings)

    @staticmethod
    def run_server(port=9876, host='127.0.0.1', **kwargs):
        tornado_server = httpserver.HTTPServer(RunServer.application, **kwargs, xheaders=True)
        tornado_server.bind(port, host)

        if uname()[0] == 'Windows':
            tornado_server.start()
        else:
            tornado_server.start(None)

        try:
            print('Server is running on http://{host}:{port}'.format(host=host, port=port))
            ioloop.IOLoop.instance().current().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()
            print('"Ctrl+C" received, exiting.\n')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    options.define("p", default=6789, help="running port", type=int)
    options.define("h", default='127.0.0.1', help="listen address", type=str)
    options.define("a", default='', help="Allowed IPs to access this server,split by comma", type=str)
    options.parse_command_line()
    p = options.options.p
    h = options.options.h
    allow = options.options.a
    if allow:
        ALLOWED_IPS = allow.split(',')
    RunServer.run_server(port=p, host=h)
