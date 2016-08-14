#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user
from eventit.forms import CreateEventForm, LoginForm
from eventit.models import Event
from app import app


def render_frontpage():
    login_form = LoginForm()
    return render_template('index.html', **{
        'events': Event,
        'login_form': login_form
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