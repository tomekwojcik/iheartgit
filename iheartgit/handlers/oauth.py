# -*- coding: utf-8 -*-
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
    def get(self):
        if self.current_user != None:
            self.redirect('/')
        else:
            self.redirect('https://github.com/login/oauth/authorize?client_id=%s&redirect_uri=%s' % (config.GITHUB_ID, config.GITHUB_CALLBACK))
        
class GitHubCallbackHandler(tornado.web.RequestHandler):
    def on_profile_response(self, response):
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
    def on_profile_response(self, twitter_user):
        user_id = None
        current_user = User.objects(service='twitter', nick=twitter_user['username']).first()
        if current_user != None:
            user_id = unicode(current_user.id)
            logging.info('Twitter user "%s" already signed up.' % (github_user['login'], ))
        else:
            user = User(service='twitter', nick=twitter_user['username'], url='http://twitter.com/' + twitter_user['username'], avatar_url=twitter_user['profile_image_url'])
            
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
        if self.current_user != None:
            self.redirect('/')
            self.finish()
        else:
            if self.get_argument('oauth_token', None):
                self.get_authenticated_user(self.async_callback(self.on_profile_response))
                return
                
            self.authenticate_redirect()