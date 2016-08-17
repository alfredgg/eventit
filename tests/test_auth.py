#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import EventitTestBase
from flask import url_for
from eventit.models import User, db


class AuthTest(EventitTestBase):
    def test_register_and_login(self):
        response = self.auth_register('test_user', '1234', 'Test', 'User', 'test_user@test.test')
        self.assertTrue(response.status_code == 302)  # TODO: It was a redirection to 'login', is that right?

        # FIXME: g.outbox does not work, neither mail.record_messages(), we shall check the mails
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
        response = self.auth_login('test_user', '1234')
        self.assertTrue(response.status_code == 302)

        self.client.get(url_for('logout'))

        # login with email
        response = self.auth_login('test_user@test.test', '1234')
        self.assertTrue(response.status_code == 302)

    def test_register_same_username(self):
        response = self.auth_register('test_user', '1234', 'Test', 'User', 'test_user@test.test')
        self.assertTrue(response.status_code == 302)  # TODO: It was a redirection to 'login', is that right?

        response = self.auth_register('test_user', '1234', 'Test', 'User', 'test_user2@test.test')
        self.assertTrue(response.status_code == 200)

    def test_register_same_mail(self):
        response = self.auth_register('test_user', '1234', 'Test', 'User', 'test_user@test.test')
        self.assertTrue(response.status_code == 302)  # TODO: It was a redirection to 'login', is that right?

        response = self.auth_register('test_user2', '1234', 'Test', 'User', 'test_user@test.test')
        self.assertTrue(response.status_code == 200)


    def test_change_password_username(self):
        user = User(
            username='test_user',
            password='1234',
            email='test_user@test.test',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()

        response = self.auth_forgot_password(user.username)
        self.assertTrue(response.status_code == 200)

        # FIXME: g.outbox does not work, neither mail.record_messages(), we shall check the mails
        """
        with self.app.communication_manager.mail.record_messages() as outbox:
            self.assertEqual(len(outbox), 1)
            sent_msg = outbox[0]
            print sent_msg
        """

        db.session.refresh(user)
        password_token = user.reset_password_token
        self.assertTrue(password_token is not None)

        response = self.client.post(url_for('recover_password', token=password_token), data={
            'password': '12345',
            'confirm': '12345'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)

        db.session.refresh(user)
        password_token = user.reset_password_token
        self.assertTrue(password_token is None)

    def test_change_password_mail(self):
        user = User(
            username='test_user',
            password='1234',
            email='test_user@test.test',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()

        response = self.auth_forgot_password(user.email)
        self.assertTrue(response.status_code == 200)

        # FIXME: g.outbox does not work, neither mail.record_messages(), we shall check the mails
        """
        with self.app.communication_manager.mail.record_messages() as outbox:
            self.assertEqual(len(outbox), 1)
            sent_msg = outbox[0]
            print sent_msg
        """

        db.session.refresh(user)
        password_token = user.reset_password_token
        self.assertTrue(password_token is not None)

        response = self.client.post(url_for('recover_password', token=password_token), data={
            'password': '12345',
            'confirm': '12345'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)

        db.session.refresh(user)
        password_token = user.reset_password_token
        self.assertTrue(password_token is None)