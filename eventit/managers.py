#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask_mail import Mail, Message


class BaseAssetManager(object):
    pass


class DiskAssetManager(object):
    pass


class BaseCommunicationManager(object):
    def send_message(self):
        pass

    def send_mail(self, message, recipient, html_message=None):
        self._send_mail(message, recipient, html_message)

    def _send_mail(self, message, recipient, html_message=None):
        raise NotImplementedError()


class FlaskMailCommunicationManager(BaseCommunicationManager):
    def __init__(self):
        self.mail = Mail(current_app)

    def _send_mail(self, message, recipient, html_message=None):
        msg = Message(message, recipients=[recipient])
        self.mail.send(msg)
