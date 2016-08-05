#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, session, flash, url_for, redirect, request
from models import Event, User, db, Connection
from forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', **{
        'events': Event
    })


@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: And current user is not anonymous
    if session.get('username'):
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

        session['username'] = existing_user.username
        db.session.add(Connection(user=existing_user))
        db.session.commit()
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = None
    return redirect(url_for('index'))
