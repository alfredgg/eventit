#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import EventitTestBase
from eventit.models import User, db, check_password_hash


class UserModelsTest(EventitTestBase):
    def test_change_password(self):
        u = User(
            username='test_user',
            password='1233',
            email='test@test.test'
        )
        db.session.add(u)
        db.session.commit()
        u.password = '1234'
        db.session.commit()
        self.assertTrue(check_password_hash(u.password, '1234'))

