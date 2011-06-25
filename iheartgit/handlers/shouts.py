# -*- coding: utf-8 -*-
from iheartgit.handlers import BaseHandler
from iheartgit.models.shout import Shout
from tornado.escape import xhtml_escape
from datetime import datetime
import config
import logging

class ShoutsHandler(BaseHandler):
    def shout_date(self, date=None):
        try:
            timedelta = datetime.now() - date
        except:
            return '?'
            
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
            
        if timedelta.seconds < 86400:
            hours_ago = int(round(timedelta.seconds / 3600.0))
            plural = ''
            if hours_ago > 1:
                plural = 's'
            return '%d hour%s ago' % (hours_ago, plural)
            
        return date.strftime('%a %d, %Y %H:%M')
            
    def get(self):
        try:
            offset = int(self.get_argument('offset', 0))
        except:
            offset = 0
        
        shouts = Shout.objects().order_by('-created_at')[offset:offset + 1]
                
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