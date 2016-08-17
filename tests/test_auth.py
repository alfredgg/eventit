#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import EventitTestBase
from flask import url_for
from eventit.models import User, db


class AuthTest(EventitTestBase):
    def test_register_and_login(self):
        response = self.client.post(url_for('register'), data={
            'username': 'test_user',
            'password': '1234',
            'confirm': '1234',
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test_user@test.test'
        })
        self.assertTrue(response.status_code == 302)  # TODO: It was a redirection to 'login', is that right?

        # TODO: g.outbox does not work, neither mail.record_messages()
        """
        with self.app.communication_manager.mail.record_messages() as outbox:
            self.assertEqual(len(outbox), 1)
            sent_msg = outbox[0]
            print sent_msg
        """

        user = User.query.filter_by(email='test_user@test.test').first()
        token = user.uuid
        response = self.client.get(url_for('activate', uuid=user.uuid), follow_redirects=True)
        data = response.get_data(as_text=True)
        # self.assertTrue('You have confirmed your account' in data)

        db.session.refresh(user)
        self.assertTrue(user.is_active)

        # login with username
        response = self.client.post(url_for('login'), data={
            'username': 'test_user',
            'password': '1234'
        })
        self.assertTrue(response.status_code == 302)

        self.client.get(url_for('logout'))

        response = self.client.post(url_for('login'), data={
            'username': 'test_user@test.test',
            'password': '1234'
        })
        self.assertTrue(response.status_code == 302)


"""
# login with the new account
response = self.client.post(url_for('auth.login'), data={
'email': 'john@example.com',
'password': 'cat'
}, follow_redirects=True)
data = response.get_data(as_text=True)
self.assertTrue(re.search('Hello,\s+john!', data))
self.assertTrue('You have not confirmed your account yet' in data)
# send a confirmation token
user = User.query.filter_by(email='john@example.com').first()
token = user.generate_confirmation_token()
response = self.client.get(url_for('auth.confirm', token=token),
follow_redirects=True)
data = response.get_data(as_text=True)
self.assertTrue('You have confirmed your account' in data)
# log out
response = self.client.get(url_for('auth.logout'),
follow_redirects=True)
data = response.get_data(as_text=True)
self.assertTrue('You have been logged out' in data)
"""
