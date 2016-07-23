#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ['HOME'] + '/eventit.db'
TEMPLATES_FOLDER = 'templates'
