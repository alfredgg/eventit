#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.data import generate_data
import unittest2 as unittest
import tempfile
from app import app
from manage import setup_db
import os


class EventitTestBase(unittest.TestCase):
    def setUp(self):
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        app.config['TESTING'] = True
        self.app = app.test_client()
        setup_db()
        generate_data()

    def tearDown(self):
        os.remove(self.test_db_file)