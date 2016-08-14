#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
import os


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
login_manager = LoginManager()
admin = Admin(app)

