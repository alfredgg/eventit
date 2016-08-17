#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2 as unittest
import tempfile
from flask import url_for
import os

# FIXME: Flask-Mail needs to set the TESTING = True variable before is initialized, if not it'll send mails :(
os.environ['EVENTIT_CONFIG_MODULE'] = 'tests/app_config_test.py'
from eventit.eventit import app
from tests.data import generate_data
from manage import setup_db


class EventitTestBase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'testing'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SEND_BACKGROUND_MAIL'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies=True)
        setup_db()
        generate_data()

    def tearDown(self):
        os.remove(self.test_db_file)

    def auth_register(self, username, password, firstname, lastname, email, repeat_password=True):
        return self.client.post(url_for('register'), data={
            'username': username,
            'password': password,
            'confirm': password if repeat_password else password + '_different',
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })

    def auth_login(self, username, password):
        return self.client.post(url_for('login'), data={
            'username': username,
            'password': password
        })

    def auth_forgot_password(self, username):
        return self.client.post(url_for('forgot_password'), data={
            'username': username
        })
