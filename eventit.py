#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from flask import render_template
from models import Event
import os

if not os.path.exists('static/assets'):
    os.mkdir('static/assets')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', **{
        'events': Event
    })
