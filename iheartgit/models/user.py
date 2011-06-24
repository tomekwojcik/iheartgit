from mongoengine import *
from datetime import datetime

class User(Document):
    service = StringField()
    nick = StringField(unique_with='service')
    created_at = DateTimeField(default=datetime.now)
    url = StringField()
    avatar_url = StringField()