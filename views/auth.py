#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from flask import redirect, url_for, request, flash, render_template, abort
from flask_login import current_user, login_user, logout_user, login_required
from eventit.forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from eventit.models import User, Connection
from app import app, db
from uuid import uuid4


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role.name not in roles:
                return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def allow_organizer(*roles):
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if not app.config['ALLOW_REGISTER']:
        abort(404)

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

        app.communication_manager.send_mail_from_template(
            template='mail/activate_account.txt',
            subject=app.config['MAIL_ACTIVATE_ACCOUNT_SUBJECT'],
            recipient=user.email,
            **{
                'user': user,
                'activate_link': url_for('activate', uuid=user.uuid, _external=True)
            })

        return redirect(url_for('login'))

    if form.errors:
        flash(form.errors, 'warning')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        db.session.add(Connection(user=existing_user, address=request.remote_addr))
        db.session.commit()
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/activate/<string:uuid>', methods=['GET'])
def activate(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    user.is_active = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ForgotPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        if '@' in username:
            existing_user = User.query.filter_by(email=username).first()
        else:
            existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            flash('The mail or username is not in our DataBase.', 'warning')
            return render_template('forgot_password.html', form=form)

        existing_user.reset_password_token = str(uuid4()).replace('-', '')
        db.session.commit()

        app.communication_manager.send_mail_from_template(
            template='mail/forgot_password.txt',
            subject=app.config['MAIL_ACTIVATE_ACCOUNT_SUBJECT'],
            recipient=existing_user.email,
            **{
                'user': existing_user,
                'reset_password_link': url_for(
                    'recover_password',
                    token=existing_user.reset_password_token,
                    _external=True
                )
            })
        return render_template('forgot_password_mail.html')

    return render_template('forgot_password.html', form=form)


@app.route('/recover_password/<string:token>', methods=['POST', 'GET'])
def recover_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(reset_password_token=token).first()
        if not user:
            flash('The mail or username is not in our DataBase.', 'warning')
            return render_template('forgot_password.html', form=form)
        user.password = form.password.data
        user.reset_password_token = None
        db.session.commit()
        # TODO: Send some message informing user about their password reset
        return redirect(url_for('login'))

    if request.method == 'GET':
        user = User.query.filter_by(reset_password_token=token).first()
        if not user:
            flash('The recover password token is invalid.', 'warning')
            return redirect(url_for('forgot_password'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('recover_password.html', form=form)
