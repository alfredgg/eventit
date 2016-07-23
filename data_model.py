#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app import db
from datetime import datetime
from slugify import slugify


class Event (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    slug = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)
