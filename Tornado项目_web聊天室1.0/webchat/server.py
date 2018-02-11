#coding:utf-8

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop

from tornado.options import define, options

import config
from urls import url

define('port',default=8000,type=int,help='')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            url,**config.appsettings
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()