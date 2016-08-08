#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, login_manager
from flask import render_template, flash, url_for, redirect, request, g, abort
from models import Event, User, db, Connection
from forms import RegistrationForm, LoginForm, CreateEventForm
from flask_login import login_user, login_required, logout_user, current_user
import datetime
import views


login_manager.login_view = 'login'

JINJA2_GLOBALS = {
    "get_current_date": "project.main.jinja_lib.get_current_date",
}


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))


@app.before_request
def get_current_user():
    pass

