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
"""OAuth interface handlers."""

import tornado.web
import tornado.httpclient
import tornado.auth
from urllib import urlencode
from urlparse import parse_qs
import config
import json

from iheartgit.handlers import BaseHandler
from iheartgit.models.user import User

import logging

class GitHubLoginHandler(BaseHandler):
    """GitHub authorization redirect handler."""
    def get(self):
        """Redirects the UA to GitHub authorization page."""
        if self.current_user != None:
            self.redirect('/')
        else:
            self.redirect('https://github.com/login/oauth/authorize?client_id=%s&redirect_uri=%s' % (config.GITHUB_ID, config.GITHUB_CALLBACK))
        
class GitHubCallbackHandler(tornado.web.RequestHandler):
    """GitHub post-auth callback handler."""
    def on_profile_response(self, response):
        """Handles user profile request response."""
        if response.error:
            self.send_error()
            
        try:
            github_user = json.loads(response.body)
        except:
            logging.exception('Failed to decode response.')
            self.send_error()
        
        user_id = None
        current_user = User.objects(service='github', nick=github_user['login']).first()
        if current_user != None:
            user_id = unicode(current_user.id)
            logging.info('GitHub user "%s" already signed up.' % (github_user['login'], ))
        else:    
            user = User(service='github', nick=github_user['login'], url=github_user['html_url'], avatar_url=github_user['avatar_url'])
            
            logging.info('Saving GitHub user "%s".' % (github_user['login'], ))
            try:
                user.save()
            except:
                logging.exception('Failed to save user in DB.')
                self.send_error()
                
            user_id = unicode(user.id)
            
        self.set_secure_cookie('user_id', user_id, expires_days=365)
        self.redirect('/#publish')
        self.finish()
        
    def on_callback_response(self, response):
        """Handles access token request response."""
        if response.error:
            self.send_error()
            
        try:
            response_data = parse_qs(response.body)
        except:
            self.send_error()
            
        request = tornado.httpclient.HTTPRequest('https://api.github.com/user?access_token=' + response_data['access_token'][0], method='GET')
        httpclient = tornado.httpclient.AsyncHTTPClient()
        httpclient.fetch(request, self.on_profile_response)
    
    @tornado.web.asynchronous
    def get(self):
        """GitHub OAuth callback handler."""
        body = {
            'client_id': config.GITHUB_ID,
            'client_secret': config.GITHUB_SECRET,
            'code': self.get_argument('code'),
            'redirect_uri': config.GITHUB_CALLBACK
        }
        request = tornado.httpclient.HTTPRequest('https://github.com/login/oauth/access_token', method='POST')
        request.body = urlencode(body)
        request.headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        httpclient = tornado.httpclient.AsyncHTTPClient()
        httpclient.fetch(request, self.on_callback_response)
        
class TwitterHandler(BaseHandler, tornado.auth.TwitterMixin):
    """Twitter authorization handler."""
    def on_profile_response(self, twitter_user):
        """Handles user profile request response."""
        user_id = None
        current_user = User.objects(service='twitter', nick=twitter_user['username']).first()
        if current_user != None:
            user_id = unicode(current_user.id)
            logging.info('Twitter user "%s" already signed up.' % (twitter_user['username'], ))
            if len(current_user.auth) == 0 or current_user.auth['key'] != twitter_user['access_token']['key']:
                current_user.auth = twitter_user['access_token']
                
                try:
                    current_user.save()
                except:
                    logging.exception('Could not update Twitter user auth token.')
                    self.send_error
        else:
            user = User(service='twitter', nick=twitter_user['username'], url='http://twitter.com/' + twitter_user['username'], avatar_url=twitter_user['profile_image_url'])
            user.auth = twitter_user['access_token']
            
            logging.info('Saving Twitter user "%s".' % (twitter_user['username'], ))
            try:
                user.save()
            except:
                logging.exception('Failed to save user in DB.')
                self.send_error()
                
            user_id = unicode(user.id)
            
        self.set_secure_cookie('user_id', user_id, expires_days=365)
        self.redirect('/#publish')
        
    @tornado.web.asynchronous
    def get(self):
        """Redirects the UA to Twitter authorization page or acts as callback handler."""
        if self.current_user != None:
            self.redirect('/')
            self.finish()
        else:
            if self.get_argument('oauth_token', None):
                self.get_authenticated_user(self.async_callback(self.on_profile_response))
                return
                
            self.authenticate_redirect()