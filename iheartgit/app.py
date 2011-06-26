# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 by Tomasz Wójcik <labs@tomekwojcik.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Application factory."""

import tornado.web
import iheartgit.handlers
import logging
import os

# Routing table.
routes = [
    (r'/', iheartgit.handlers.IndexHandler),
    (r'/oauth/github/login', iheartgit.handlers.oauth.GitHubLoginHandler),
    (r'/oauth/github/callback', iheartgit.handlers.oauth.GitHubCallbackHandler),
    (r'/oauth/twitter/login', iheartgit.handlers.oauth.TwitterHandler),
    (r'/oauth/twitter/callback', iheartgit.handlers.oauth.TwitterHandler),
    (r'/shouts', iheartgit.handlers.shouts.ShoutsHandler),
]

def create_app(config=None):
    """Instantiates and initializes the app according to config dict."""
    if config == None:
        raise RuntimeError('No configuration given.')
        
    config['static_path'] = os.path.join(os.path.dirname(__file__), 'static')
        
    if config.get('debug', False):
        logging.basicConfig(level=logging.DEBUG)
    
    app = tornado.web.Application(routes, **config)
    
    return app