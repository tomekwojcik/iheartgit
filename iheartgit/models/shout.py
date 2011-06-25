from mongoengine import *
from datetime import datetime

from iheartgit.models.user import User

class Shout(Document):
    user = ReferenceField(User)
    text = StringField(max_length=140)
    created_at = DateTimeField(default=datetime.now)