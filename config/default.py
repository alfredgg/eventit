#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ['HOME'] + '/eventit.db'
N_EVENTS_PASSED = 5
N_EVENTS_UPCOMING = 5
