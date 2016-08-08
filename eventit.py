#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import datetime
from flask_login import login_required
from flask import send_from_directory, abort

app = Flask(__name__)

if os.path.exists(os.path.join(os.path.dirname(__file__), 'app_config.py')):
    app.config.from_object('app_config')

app.config.from_envvar('EVENTIT_CONFIG_MODULE', silent=True)

if 'STATIC_FOLDER' in app.config.keys() and app.config['STATIC_FOLDER']:
    app.static_folder = app.config['STATIC_FOLDER']

base_path = ''
if 'TEMPLATES_PATH' in app.config.keys() and app.config['TEMPLATES_PATH']:
    app.template_folder = app.config['TEMPLATES_PATH']

db = SQLAlchemy(app)

# Configure flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(_id):
    from models import User
    return User.query.get(int(_id))


# Configure templates
JINJA2_GLOBALS = {
    'now': datetime.datetime.now
}
app.jinja_env.globals.update(**JINJA2_GLOBALS)


@app.before_request
def get_current_user():
    pass


@app.route('/page/<path:filename>')
def pages(filename):
    if app.config['PAGES_PATH']:
        return send_from_directory(app.config['PAGES_PATH'], filename)
    abort(404)


@app.route('/user_page/<path:filename>')
@login_required
def user_pages(filename):
    if app.config['USER_PAGES_PATH']:
        return send_from_directory(app.config['USER_PAGES_PATH'], filename)
    abort(404)

import views