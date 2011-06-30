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
"""Shouts handler."""

from iheartgit.handlers import BaseHandler
from iheartgit.models.shout import Shout
from tornado.escape import xhtml_escape
from datetime import datetime
import config
import logging

class ShoutsHandler(BaseHandler):
    """Shouts handler."""
    def shout_date(self, date=None):
        """Reads shout date and return time delta string."""
        try:
            timedelta = datetime.now() - date
        except:
            return '?'
        
        if timedelta.days > 0:
            return date.strftime('%a %d, %Y %H:%M')
        
        if timedelta.seconds < 5:
            return 'Just now'
            
        if timedelta.seconds < 59:
            plural = ''
            if timedelta.seconds > 1:
                plural = 's'
            return '%d second%s ago' % (timedelta.seconds, plural)
            
        if timedelta.seconds < 3600:
            minutes_ago = int(round(timedelta.seconds / 60.0))
            plural = ''
            if minutes_ago > 1:
                plural = 's'
            return '%d minute%s ago' % (minutes_ago, plural)
            
        hours_ago = int(round(timedelta.seconds / 3600.0))
        plural = ''
        if hours_ago > 1:
            plural = 's'
        return '%d hour%s ago' % (hours_ago, plural)
            
    def get(self):
        """Fetches 10 shouts and returns them as JSON.
        
        Use *offset* query string parameter for pagination."""
        try:
            offset = int(self.get_argument('offset', 0))
        except:
            offset = 0
        
        shouts = Shout.objects().order_by('-created_at')[offset:offset + 10]
                
        response = []
        for shout in shouts:
            response.append({
                'id': unicode(shout.id),
                'text': shout.text,
                'created_at': self.shout_date(shout.created_at),
                'user': {
                    'nick': shout.user.nick,
                    'avatar_url': shout.user.avatar_url,
                    'url': shout.user.url
                }
            })
            
        self.write({ 'shouts': response })
        
    def post(self):
        """Saves a shout by a current user."""
        if self.current_user == None:
            self.send_error(403)
        else:
            current_shout = Shout.objects(user=self.current_user).first()
            
            if current_shout != None:
                self.send_error(409)
            else:
                shout = Shout(user=self.current_user, text=xhtml_escape(self.get_argument('text')))
                
                try:
                    shout.save()
                except:
                    logging.exception('Failed to save shout in DB.')
                    self.send_error()
                else:
                    self.write({ 'status': 'ok' })