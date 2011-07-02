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
"""Common handler-specific things."""

import tornado.web
import logging

import config
from mongoengine import connect
from iheartgit.models.user import User
from iheartgit.models.shout import Shout

class BaseHandler(tornado.web.RequestHandler):
    """RequestHandler subclass that provides base for app's handlers."""
    def prepare(self):
        """Pre-handler callback. Sets up MongoDB connection for this request."""
        self._db = connect(config.MONGO_DB)
        
    def get_current_user(self):
        """Loads user data from the DB if there's a user_id cookie defined.
        
        Resets the cookie if user is successfully loaded to prevent its expiration."""
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

class IndexHandler(BaseHandler):
    """Handler for app's main page."""
    def get(self):
        shouts_count = Shout.objects().count()
        self.render('../templates/index.html', shouts_count=shouts_count, ga_id=config.GOOGLE_ANALYTICS_ID)
            