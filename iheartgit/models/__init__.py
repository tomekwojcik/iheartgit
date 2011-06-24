# -*- coding: utf-8 -*-
from mongoengine import connect
import config

class Session(object):
    def __init__(self):
        self._db = connect(config.MONGO_DB)