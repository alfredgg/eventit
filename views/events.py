#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_login import login_required, current_user
from eventit import app, db
from forms import CreateEventForm
from models import Event
import datetime
from flask import redirect, url_for, abort, render_template, request


@app.route('/event', methods=['POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        the_event = Event(
            name=form.name.data,
            description='',
            starting_at=datetime.date.today() + datetime.timedelta(days=1),
            owner_id=current_user.id
        )
        db.session.add(the_event)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/event/<string:event_uid>', methods=['GET', 'POST'])
def event(event_uid):
    the_event = Event.query.filter_by(slug=event_uid).first()
    if not the_event:
        abort(404)
    if request.method == 'GET':
        if the_event.owner == current_user:
            form = CreateEventForm(
                name=the_event.name
            )
            return render_template('event.html', **{
                'event': the_event,
                'form': form
            })
        else:
            return render_template('event.html', **{
                'event': the_event,
                'form': None
            })
    elif request.method == 'POST':
        if the_event.owner == current_user:
            form = CreateEventForm()
            if form.validate_on_submit():
                form.populate_obj(the_event)
                db.session.commit()
            return redirect(url_for('event', event_uid=the_event.slug))
        else:
            abort(403)
