#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if os.path.exists(os.path.join(os.path.dirname(__file__), 'app_config.py')):
    app.config.from_object('app_config')

app.config.from_envvar('BACKEND_CONFIG_MODULE', silent=True)
db = SQLAlchemy(app)
