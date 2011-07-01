#!/usr/bin/env python
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
"""Application wrapper.

Use this script to run an instance of the app.
"""

import tornado.ioloop
from config import app_config
from optparse import OptionParser
from iheartgit.app import create_app

app = create_app(app_config)

if __name__ in ('main', '__main__'):
    parser = OptionParser()
    parser.add_option('-p', '--port', dest="port", help="port to bind to. Defaults to 8888.", action="store", type="int", default=8888)
    options, args = parser.parse_args()
    
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()