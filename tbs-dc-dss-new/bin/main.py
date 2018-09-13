#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

from tornado import web
from tornado import ioloop

from tornado import httpserver
from tornado.options import options
from core.serverHandlers import AuthHandler, ServerHandler

options.define('port', 8005, help='run help', type=int)

application = web.Application(
    handlers=[
        (r'/operate', ServerHandler),
        (r'/auth', AuthHandler),
    ],
    autoreload=True,
)

if __name__ == '__main__':
    options.parse_command_line()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()