#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, login_manager
from models import User
import datetime
from flask_login import login_required
from flask import send_from_directory, abort
import views


login_manager.login_view = 'login'

JINJA2_GLOBALS = {
    'now': datetime.datetime.now
}
app.jinja_env.globals.update(**JINJA2_GLOBALS)


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))


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