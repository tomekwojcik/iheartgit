# -*- coding: utf-8 -*-
import tornado.web

class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, World!')