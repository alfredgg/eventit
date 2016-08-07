#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Email


class RegistrationForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])
    firstname = StringField('Name', [InputRequired()])
    lastname = StringField('Last name')
    email = StringField('E-Mail', [Email()])


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


class CreateEventForm(Form):
    name = StringField('Event Name', [InputRequired()])
