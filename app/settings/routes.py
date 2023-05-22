from flask import render_template, flash, redirect, request, url_for
from app.settings import bp
from app.models import User
from app.models.connections import RadarrConnection, SonarrConnection, OmbiConnection
from app.settings.forms import EditUserForm, EditConnectionsForm
from flask_login import login_required
from app import db

@bp.route('/')
@login_required
def index():
    return render_template('settings/index.html')

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

@bp.route('/connections', methods=['GET', 'POST'])
@login_required
def connections():
    connectionRadarr = RadarrConnection.query.first()
    connectionSonarr = SonarrConnection.query.first()
    connectionOmbi = OmbiConnection.query.first()
    form = EditConnectionsForm()
    if form.validate_on_submit():
        connectionRadarr.host = form.hostRadarr.data
        connectionRadarr.port = form.portRadarr.data
        connectionRadarr.apiKey = form.apiKeyRadarr.data
        connectionSonarr.host = form.hostSonarr.data
        connectionSonarr.port = form.portSonarr.data
        connectionSonarr.apiKey = form.apiKeySonarr.data
        connectionOmbi.host = form.hostOmbi.data
        connectionOmbi.port = form.portOmbi.data
        connectionOmbi.apiKey = form.apiKeyOmbi.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('settings.connections'))
    elif request.method == 'GET':
        form.hostRadarr.data = connectionRadarr.host
        form.portRadarr.data = connectionRadarr.port
        form.apiKeyRadarr.data = connectionRadarr.apiKey
        form.hostSonarr.data = connectionSonarr.host
        form.portSonarr.data = connectionSonarr.port
        form.apiKeySonarr.data = connectionSonarr.apiKey
        form.hostOmbi.data = connectionOmbi.host
        form.portOmbi.data = connectionOmbi.port
        form.apiKeyOmbi.data = connectionOmbi.apiKey
    return render_template('settings/connections.html', form=form)