#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
from exceptions import Warning
warnings.simplefilter('ignore', Warning)

from flask_script import Manager
from app import app


CONFIG_TEMPLATE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

SQLALCHEMY_DATABASE_URI = '%(db_path)s'
SESSION_TYPE = 'filesystem'
SECRET_KEY = '%(secret_key)s'

SERVER_NAME = None

STATIC_FOLDER = None
PAGES_PATH = None
USER_PAGES_PATH = None
TEMPLATES_PATH = None

SQLALCHEMY_TRACK_MODIFICATIONS = False
ALLOW_REGISTER = True
DB_TABLE_PREFIX = ''

USERS_CAN_ORGANIZE = False

COMMUNICATION_MANAGER = 'eventit.managers.FlaskMailCommunicationManager'

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
# MAIL_DEBUG = app.debug
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = None

MAIL_ACTIVATE_ACCOUNT_SUBJECT = 'Eventit account activation'
MAIL_FORGOTTEN_PASSWORD_SUBJECT = 'You forgot the Eventit password'
"""

manager = Manager(app)


def generate_secret_key():
    import os
    return os.urandom(24).encode('hex')


@manager.command
def write_config():
    'Writes app_config file.'
    import os
    data = {
        'db_path': 'sqlite:///' + os.environ['HOME'] + '/eventit.db',
        'secret_key': generate_secret_key(),
    }
    values = CONFIG_TEMPLATE % data
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app_config.py'), 'w')
    f.write(values)
    f.close()


@manager.command
def setup_db():
    from eventit.models import db, Role
    db.drop_all()   # TODO: Add a script for migrating the DB and not dropping it
    db.create_all()
    role_admin = Role(name='admin')
    role_organizer = Role(name='organizer')
    db.session.add(role_admin)
    db.session.add(role_organizer)
    db.session.commit()


@manager.command
def generate_test_data():
    from tests.data import generate_data
    generate_data()


@manager.command
def prepare_dev():
    setup_db()
    generate_test_data()


@manager.option('-n', '--username', dest='username', default='admin')
def create_admin(username):
    from eventit.eventit import db
    from eventit.models import User, Role
    import getpass
    from sys import stdout

    password = None
    password2 = None
    while not password or password != password2:
        password = getpass.getpass()
        password2 = getpass.getpass('Please, repeat your password: ')
        if not password or password != password2:
            stdout.write('Passwords do not match')

    user = User(username=username, email='', is_active=True, password=password)
    role_admin = Role.get_role_obj('admin')
    user.role = role_admin

    db.session.add(user)
    db.session.commit()


@manager.command
def test(coverage=False):
    import unittest2
    import os
    import coverage as _coverage
    cov = None
    if coverage:
        cov = _coverage.coverage(branch=True, include='./*')
        cov.start()
    tests = unittest2.TestLoader().discover('tests')
    unittest2.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()


# TODO: Implement options
@manager.command
def runserver():
    from eventit.eventit import app
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )

# TODO: Create admin user

if __name__ == '__main__':
    manager.run()
