#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app, copy_current_request_context, render_template
from flask_mail import Mail, Message
from threading import Thread


communication = None


def set_communication_manager(com_manager):
    global communication
    communication = com_manager


class BaseAssetManager(object):
    pass


class DiskAssetManager(object):
    pass


class BaseCommunicationManager(object):
    def send_message(self):
        pass

    def send_mail_from_template(self, template, subject, recipient, **context):
        self.send_mail(subject, render_template(template, **context), recipient)

    def send_mail(self, subject, message, recipient, html_message=None):
        self._send_mail(subject, message, recipient, html_message)

    def _send_mail(self, subject, message, recipient, html_message=None):
        raise NotImplementedError()


class FlaskMailCommunicationManager(BaseCommunicationManager):
    def __init__(self):
        self.mail = Mail(current_app)

    def _send_mail(self, subject, message, recipient, html_message=None):
        @copy_current_request_context
        def send_message(mail, the_message):
            mail.send(the_message)

        msg = Message(subject=subject, body=message, recipients=[recipient])
        sender = Thread(name='mail_sender', target=send_message, args=(self.mail, msg,))
        sender.start()
