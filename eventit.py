#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, login_manager
from flask import render_template, flash, url_for, redirect, request, g, abort
from models import Event, User, db, Connection
from forms import RegistrationForm, LoginForm, CreateEventForm
from flask_login import login_user, login_required, logout_user, current_user
import datetime


login_manager.login_view = 'login'


def render_frontpage():
    return render_template('index.html', **{
        'events': Event
    })


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))


@app.before_request
def get_current_user():
    g.user = current_user


@app.route('/')
@app.route('/index.html')
def index():
    if current_user.is_authenticated:
        form = CreateEventForm()
        return render_template('user.html', **{
            'events': Event,
            'form': form
        })
    return render_frontpage()


@app.route('/frontpage')
def frontpage():
    return render_frontpage()


@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: And current user is not anonymous
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        error = None
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            error = 'This username has been already taken. Try another one.'
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            error = 'This email has been already registered.'
        if error:
            flash(error, 'warning')
            return render_template('register.html', form=form)

        user = User(
            username=form.username.data,
            password=form.password.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    if form.errors:
        flash(form.errors, 'warning')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        if '@' in username:
            existing_user = User.query.filter_by(email=username).first()
        else:
            existing_user = User.query.filter_by(username=username).first()

        if not (existing_user and existing_user.check_password(form.password.data)):
            flash('Invalid username or password. Please try again.', 'warning')
            return render_template('login.html', form=form)

        login_user(existing_user)
        db.session.add(Connection(user=existing_user))
        db.session.commit()
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)


@login_required
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/event', methods=['POST'])
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
        abort(404, message='')
    if the_event.owner == current_user:
        pass
    else:
        pass
