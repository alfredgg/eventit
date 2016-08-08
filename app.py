#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

if os.path.exists(os.path.join(os.path.dirname(__file__), 'app_config.py')):
    app.config.from_object('app_config')

app.config.from_envvar('EVENTIT_CONFIG_MODULE', silent=True)

if app.config['STATIC_FOLDER']:
    app.static_folder = app.config['STATIC_FOLDER']

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
