from flask import render_template, flash, redirect, request, url_for, Response, jsonify
from datetime import datetime
from app.settings import bp
from app.models import User, AppSettings, Movie, TVShow, MoviePick, TVShowPick
from app.settings.forms import EditUserForm, AddUserForm, EditAppSettings
from flask_login import login_required
from app.scripts.media import import_all_requests
from app import db

@bp.route('/application', methods=['GET', 'POST'])
@login_required
def application():
    app_settings = AppSettings.query.first()
    form = EditAppSettings()
    if form.validate_on_submit():
        app_settings.expiryTimeNumber = form.expiryTimeNumber.data
        app_settings.expiryTimeUnit = form.expiryTimeUnit.data
        app_settings.appName = form.appName.data
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
        flash('Your changes have been saved.', "success")
        return redirect(url_for('settings.application'))
    elif request.method == 'GET':
        form.expiryTimeNumber.data = app_settings.expiryTimeNumber
        form.expiryTimeUnit.data = app_settings.expiryTimeUnit
        form.appName.data = app_settings.appName
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
        #If this user is the last admin and the user unchecks admin, we deny it.
        lastAdmin = db.one_or_404(db.select(User).filter_by(admin=True))
        if ((user == lastAdmin) and (not form.admin.data)):
            flash('Cannot disable the last administrator', "error")
        else:
            user.alias = form.alias.data
            user.admin = form.admin.data
            db.session.commit()
            flash('Your changes have been saved.', "success")
        return redirect(url_for('settings.users'))
    elif request.method == 'GET':
        form.email.data = user.email
        form.alias.data = user.alias
        form.admin.data = user.admin
    return render_template('settings/user.html', form=form)

@bp.route('/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.admin:
        return {
            "error" : user.email+" is an admin and cannot be deleted"
        }, 400
    db.session.delete(user)
    db.session.commit()
    return {
        "message" : user.email+" has been deleted"
    }

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, alias=form.alias.data, admin=form.admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been added.', "success")
        return redirect(url_for('settings.users'))
    return render_template('settings/add_user.html', form=form)

@bp.route('/import_requests', methods=['POST'])
@login_required
def import_requests():
    try:
        scriptResult = import_all_requests()
    except Exception as err:
        return jsonify(error=str(err)), 500

    app_settings = AppSettings.query.first()
    app_settings.lastMediaImport = datetime.utcnow()
    db.session.commit()
    return {
        'message' : scriptResult
    }

@bp.route('/delete_medias', methods=['DELETE'])
@login_required
def delete_medias():
    numMovies = Movie.query.delete()
    numTVShows = TVShow.query.delete()
    db.session.commit()
    return {
        'message' : "Deleted "+str(numMovies)+" movies and "+str(numTVShows)+" TV shows"
    }

@bp.route('/delete_picks', methods=['DELETE'])
@login_required
def delete_picks():
    numMoviePicks = MoviePick.query.delete()
    numTVShowPicks = TVShowPick.query.delete()
    db.session.commit()
    return {
        'message' : "Deleted "+str(numMoviePicks)+" movie picks and "+str(numTVShowPicks)+" TV show picks"
    }

@bp.route('/delete_users', methods=['POST'])
@login_required
def delete_users():
    numUsers = User.query.filter_by(admin=False).delete()
    db.session.commit()
    return {
        'message' : str(numUsers)+" non-admins deleted"
    }