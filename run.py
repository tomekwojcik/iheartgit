# -*- coding: utf-8 -*-
import tornado.ioloop
from config import config
from iheartgit.app import create_app

app = create_app(config)
app.listen(5000)
tornado.ioloop.IOLoop.instance().start()