#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.default')
app.config.from_envvar('BACKEND_CONFIG_MODULE', silent=True)
db = SQLAlchemy(app)
