# -*- coding: utf-8 -*-
from paver.easy import *
from paver.setuputils import setup
import os

setup(
    name='iheartgit',
    version='1.0b1',
    description='Web application that powers http://iheartgit.com/',
    author='Tomek Wójcik',
    author_email='labs@tomekwojcik.pl',
    url='http://www.bthlabs.pl/',
    packages=[ 'iheartgit', 'iheartgit.handlers', 'iheartgit.models' ],
    package_data={
        'iheartgit': [ 'static/ajax-loader.gif', 'static/iheartgit.js', 'static/jquery-1.6.1.min.js', 'static/style.css', 'templates/index.html' ]
    }
)


def compile_coffeescripts():
    exit_status = os.system('coffee -c -o %s %s' % (path('iheartgit') / 'static', path('iheartgit') / 'static' / 'iheartgit.coffee'))
        
    if exit_status != 0:
        raise RuntimeError('Failed to compile CoffeeScripts.')

@task
def build():
    compile_coffeescripts()
    
    call_task("setuptools.command.build")