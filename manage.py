#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
from exceptions import Warning
warnings.simplefilter('ignore', Warning)

from flask_script import Manager
from eventit import app


CONFIG_TEMPLATE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

SQLALCHEMY_DATABASE_URI = '%(db_path)s'
SESSION_TYPE = 'filesystem'
SECRET_KEY = '%(secret_key)s'

STATIC_FOLDER = None
PAGES_PATH = None
USER_PAGES_PATH = None
TEMPLATES_PATH = None

SQLALCHEMY_TRACK_MODIFICATIONS = False
ALLOW_REGISTER = True
DB_TABLE_PREFIX = ''

USERS_CAN_ORGANIZE = False
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
    from models import db, Role
    db.drop_all()
    db.create_all()
    role_admin = Role(name='admin')
    role_organizer = Role(name='organizer')
    db.session.add(role_admin)
    db.session.add(role_organizer)
    db.session.commit()


@manager.command
def generate_test_data():
    from tests.test_data import generate_data
    generate_data()


@manager.command
def prepare_dev():
    setup_db()
    generate_test_data()


# TODO: Implement options
@manager.command
def runserver():
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )

# TODO: Create admin user

if __name__ == '__main__':
    manager.run()
