#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from flask import render_template
from data_model import Event


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', **{
        'events': Event
    })
