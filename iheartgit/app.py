# -*- coding: utf-8 -*-
import tornado.web
import iheartgit.handlers

routes = [
    (r'/', iheartgit.handlers.HelloWorldHandler),
    (r'/oauth/github/login', iheartgit.handlers.oauth.GitHubLoginHandler),
    (r'/oauth/github/callback', iheartgit.handlers.oauth.GitHubCallbackHandler),
]

def create_app(config=None):
    if config == None:
        raise RuntimeError('No configuration given.')
    
    app = tornado.web.Application(routes, **config)
    
    return app