# -*- coding: utf-8 -*-
import tornado.web
import iheartgit.handlers.oauth

from iheartgit.models import Session
from iheartgit.models.user import User

class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_secure_cookie('user_id')
        if user_id != None:
            session = Session()
            user = User.objects(id=user_id).first()
            
        if user != None:
            self.write('Welcome back, %s!' % (user.nick, ))
        else:
            self.write('Hello, World!')
            