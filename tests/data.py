#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import factory
import factory.fuzzy
from factory import compat
from eventit import models


class UserFactory(factory.Factory):
    class Meta:
        model = models.User
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    password = '1234'
    email = factory.LazyAttribute(lambda obj: '%s@eventit.test' % obj.username)
    firstname = factory.LazyAttribute(lambda obj: obj.username)
    lastname = 'Last Name'


class EventFactory(factory.Factory):
    class Meta:
        model = models.Event
    name = factory.Sequence(lambda n: 'Event {0}'.format(n))
    starting_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(datetime.datetime.now().year, 1, 1, tzinfo=compat.UTC),
        datetime.datetime(datetime.datetime.now().year, 12, 31, tzinfo=compat.UTC)
    )
    owner_id = 0


def generate_data(n_users=25, n_events=100):
    users = UserFactory.create_batch(size=n_users)
    models.db.session.bulk_save_objects(users)

    EventFactory.owner_id = factory.fuzzy.FuzzyInteger(1, n_users)  # FIXME: Use a sub-factory or something
    events = EventFactory.create_batch(size=n_events)
    models.db.session.bulk_save_objects(events)

    models.db.session.commit()
