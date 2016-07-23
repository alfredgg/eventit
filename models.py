#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app import db
from datetime import datetime
from slugify import slugify
import arrow


class Event (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    slug = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String())
    starting_at = db.Column(db.DateTime, nullable=False)
    ending_at = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Float)
    where = db.Column(db.String(255))
    where_link = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, starting_at):
        self.name = name
        self.slug = slugify(name)
        self.starting_at = starting_at

    @property
    def short_description(self):
        return "short_description"

    @staticmethod
    def get_upcoming():
        events = Event.query.filter(Event.starting_at > datetime.utcnow()).order_by(Event.starting_at).limit(5).all()
        for event in events:
            event.starting_at_hum = arrow.get(event.starting_at).humanize()
        return events

    @staticmethod
    def get_passed():
        events = Event.query.filter(Event.starting_at < datetime.utcnow()).order_by(Event.starting_at.desc()).limit(5).all()
        for event in events:
            event.starting_at_hum = arrow.get(event.starting_at).humanize()
        return events

    def __repr__(self):
        return '<Event %r>' % self.name
