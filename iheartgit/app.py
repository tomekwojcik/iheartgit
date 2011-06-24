# -*- coding: utf-8 -*-
import tornado.web
import iheartgit.handlers

routes = [
    (r'/', iheartgit.handlers.HelloWorldHandler)
]

def create_app(config=None):
    if config == None:
        raise RuntimeError('No configuration given.')
    
    app = tornado.web.Application(routes, **config)
    
    return app