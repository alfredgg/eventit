#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from flask_login import current_user
from forms import CreateEventForm
from flask import render_template
from models import Event


def render_frontpage():
    return render_template('index.html', **{
        'events': Event
    })


@app.route('/')
@app.route('/index.html')
def index():
    if current_user.is_authenticated:
        form = CreateEventForm()
        return render_template('user.html', **{
            'events': Event,
            'form': form
        })
    return render_frontpage()


@app.route('/frontpage')
def frontpage():
    return render_frontpage()