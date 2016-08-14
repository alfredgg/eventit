#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseAssetManager(object):
    pass


class BaseCommunicationManager(object):
    def send_mail(self):
        self._send_mail()

    def _send_mail(self):
        print 'Send mail from base'


class FlaskMailCommunicationManager(BaseCommunicationManager):
    def _send_mail(self):
        print 'Send mail from flask mail'
