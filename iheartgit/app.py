# -*- coding: utf-8 -*-
import tornado.web
import iheartgit.handlers
import logging

routes = [
    (r'/', iheartgit.handlers.HelloWorldHandler),
    (r'/oauth/github/login', iheartgit.handlers.oauth.GitHubLoginHandler),
    (r'/oauth/github/callback', iheartgit.handlers.oauth.GitHubCallbackHandler),
    (r'/oauth/twitter/login', iheartgit.handlers.oauth.TwitterHandler),
    (r'/oauth/twitter/callback', iheartgit.handlers.oauth.TwitterHandler),
]

def create_app(config=None):
    if config == None:
        raise RuntimeError('No configuration given.')
        
    if config.get('debug', False):
        logging.basicConfig(level=logging.DEBUG)
    
    app = tornado.web.Application(routes, **config)
    
    return app