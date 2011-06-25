# -*- coding: utf-8 -*-
import tornado.web
import logging

import config
from mongoengine import connect
from iheartgit.models.user import User

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self._db = connect(config.MONGO_DB)
        
    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        if user_id != None:
            user = User.objects(id=user_id).first()
            
            if user != None:
                self.set_secure_cookie('user_id', user_id, expires_days=365)
            else:
                self.clear_cookie('user_id')
            return user
        else:
            return None
            
import iheartgit.handlers.oauth
import iheartgit.handlers.shouts

class HelloWorldHandler(BaseHandler):
    def get(self):
        self.render('../templates/index.html')
            