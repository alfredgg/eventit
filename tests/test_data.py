#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
import factory.fuzzy
from factory import compat
import models
import datetime


class EventFactory(factory.Factory):
    class Meta:
        model = models.Event
    name = factory.Sequence(lambda n: 'Event {0}'.format(n))
    starting_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(datetime.datetime.now().year, 1, 1, tzinfo=compat.UTC),
        datetime.datetime(datetime.datetime.now().year, 12, 31, tzinfo=compat.UTC)
    )

if __name__ == '__main__':
    NUMBER_OF_EVENTS = 100

    for _ in xrange(NUMBER_OF_EVENTS):
        event = EventFactory.build()
        models.db.session.add(event)
    models.db.session.commit()
