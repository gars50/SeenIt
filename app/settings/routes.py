from flask import render_template, flash, redirect, request, url_for
from app.settings import bp
from app.models import User, AppSettings
from app.settings.forms import EditUserForm, EditConnectionsForm, AddUserForm, EditAppSettings
from flask_login import login_required
from app import db

@bp.route('/application', methods=['GET', 'POST'])
@login_required
def application():
    app_settings = AppSettings.query.first()
    form = EditAppSettings()
    if not app_settings:
        app_settings = AppSettings()
        db.session.add(app_settings)
        db.session.commit()
    if form.validate_on_submit():
        app_settings.delayNumber = form.delayNumber.data
        app_settings.delayUnit = form.delayUnit.data
        app_settings.radarrHost = form.radarrHost.data
        app_settings.radarrPort = form.radarrPort.data
        app_settings.radarrApiKey = form.radarrApiKey.data
        app_settings.sonarrHost = form.sonarrHost.data
        app_settings.sonarrPort = form.sonarrPort.data
        app_settings.sonarrApiKey = form.sonarrApiKey.data
        app_settings.ombiHost = form.ombiHost.data
        app_settings.ombiPort = form.ombiPort.data
        app_settings.ombiApiKey = form.ombiApiKey.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('settings.application'))
    elif request.method == 'GET':
        form.delayNumber.data = app_settings.delayNumber
        form.delayUnit.data = app_settings.delayUnit
        form.radarrHost.data = app_settings.radarrHost
        form.radarrPort.data = app_settings.radarrPort
        form.radarrApiKey.data = app_settings.radarrApiKey
        form.sonarrHost.data = app_settings.sonarrHost
        form.sonarrPort.data = app_settings.sonarrPort
        form.sonarrApiKey.data = app_settings.sonarrApiKey
        form.ombiHost.data = app_settings.ombiHost
        form.ombiPort.data = app_settings.ombiPort
        form.ombiApiKey.data = app_settings.ombiApiKey
    return render_template('settings/application.html', form=form)

@bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('settings/users.html', users=users)

@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        user.alias = form.alias.data
        user.admin = form.admin.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('settings.users'))
    elif request.method == 'GET':
        form.email.data = user.email
        form.alias.data = user.alias
        form.admin.data = user.admin
    return render_template('settings/user.html', form=form)

@bp.route('/user/<int:user_id>/delete/')
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.admin:
        flash('Cannot delete an admin.')
        return redirect(url_for('settings.users'))
    #Need to reassign TVShows and Movies
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('settings.users'))

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, alias=form.alias.data, admin=form.admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been added.')
        return redirect(url_for('settings.users'))
    return render_template('settings/add_user.html', form=form)