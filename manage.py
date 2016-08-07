#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from eventit import app


CONFIG_TEMPLATE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

SQLALCHEMY_DATABASE_URI = '%(db_path)s'
SESSION_TYPE = 'filesystem'
SECRET_KEY = '%(secret_key)s'

SQLALCHEMY_TRACK_MODIFICATIONS = False
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
        'db_path': 'sqlite:///' + os.environ['HOME'] + '/newskid.db',
        'secret_key': generate_secret_key(),
    }
    values = CONFIG_TEMPLATE % data
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app_config.py'), 'w')
    f.write(values)
    f.close()


@manager.command
def setup_db():
    from models import db
    db.drop_all()
    db.create_all()


@manager.command
def generate_test_data():
    from tests.test_data import generate_data
    generate_data()


@manager.command
def prepare():
    setup_db()
    generate_test_data()


@manager.command
def runserver():
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )


if __name__ == '__main__':
    manager.run()
