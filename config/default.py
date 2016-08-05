#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ['HOME'] + '/eventit.db'
SESSION_TYPE = 'filesystem'
SECRET_KEY = '9a1c9869d834572bb4546ed65b39a9b4ce8883e940a64411'
