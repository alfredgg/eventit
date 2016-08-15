#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user
from flask import abort, redirect, request, url_for


# TODO: Do not allow admin.index for all users
# Create customized model view class
class EventitAdminModelView(ModelView):
    form_base_class = SecureForm

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        if current_user.role and current_user.role.name == 'admin':
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('login', next=request.url))


class UserModelView(EventitAdminModelView):
    column_exclude_list = ['password', 'reset_password_token']