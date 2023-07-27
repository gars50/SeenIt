from flask import render_template, flash, redirect, request, url_for, current_app
from datetime import datetime
from app import db, scheduler
from app.settings import bp
from app.models import User, AppSettings, Media, Movie, TVShow, Pick
from app.settings.forms import EditUserForm, AddUserForm, EditAppSettings
from flask_login import login_required, current_user

@bp.route('/application', methods=['GET', 'POST'])
@login_required
def application():
    if not current_user.admin:
        flash('You do not have access to this.', "error")
        return redirect(url_for('main.index'))
    app_settings = AppSettings.query.first()
    form = EditAppSettings()
    if form.validate_on_submit():
        app_settings.expiry_time_number = form.expiry_time_number.data
        app_settings.expiry_time_unit = form.expiry_time_unit.data
        app_settings.next_delete = form.next_delete.data
        app_settings.deletion_time_number = form.deletion_time_number.data
        app_settings.deletion_time_unit = form.deletion_time_unit.data
        app_settings.app_name = form.app_name.data
        app_settings.radarr_host = form.radarr_host.data
        app_settings.radarr_port = form.radarr_port.data
        app_settings.radarr_api_key = form.radarr_api_key.data
        app_settings.sonarr_host = form.sonarr_host.data
        app_settings.sonarr_port = form.sonarr_port.data
        app_settings.sonarr_api_key = form.sonarr_api_key.data
        app_settings.ombi_host = form.ombi_host.data
        app_settings.ombi_port = form.ombi_port.data
        app_settings.ombi_api_key = form.ombi_api_key.data
        app_settings.safe_mode = form.safe_mode.data
        db.session.commit()
        flash('Your changes have been saved.', "success")
        return redirect(url_for('settings.application'))
    elif request.method == 'GET':
        form.expiry_time_number.data = app_settings.expiry_time_number
        form.expiry_time_unit.data = app_settings.expiry_time_unit
        form.next_delete.data = app_settings.next_delete
        form.deletion_time_number.data = app_settings.deletion_time_number
        form.deletion_time_unit.data = app_settings.deletion_time_unit
        form.app_name.data = app_settings.app_name
        form.radarr_host.data = app_settings.radarr_host
        form.radarr_port.data = app_settings.radarr_port
        form.radarr_api_key.data = app_settings.radarr_api_key
        form.sonarr_host.data = app_settings.sonarr_host
        form.sonarr_port.data = app_settings.sonarr_port
        form.sonarr_api_key.data = app_settings.sonarr_api_key
        form.ombi_host.data = app_settings.ombi_host
        form.ombi_port.data = app_settings.ombi_port
        form.ombi_api_key.data = app_settings.ombi_api_key
        form.safe_mode.data = app_settings.safe_mode
    else :
        flash('Error saving settings. Check error messages', "error")
    return render_template('settings/application.html', form=form)

@bp.route('/users')
@login_required
def users():
    if not current_user.admin:
        flash('You do not have access to this.', "error")
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('settings/users.html', users=users)

@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        #If this user is the last admin and the user unchecks admin, we deny it.
        last_admin = db.one_or_404(db.select(User).filter_by(admin=True))
        if ((user == last_admin) and (not form.admin.data)):
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
    current_app.logger.info("Deleting user : "+str(user))
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

@bp.route('/trigger_update_medias_and_requests_job', methods=['POST'])
@login_required
def trigger_update_medias_and_requests_job():
    current_app.logger.info("Forcing a trigger of the update medias and requests job")
    scheduler.modify_job("update_medias_and_requests-job", next_run_time=datetime.utcnow())
    return {
        'message' : "Job triggered"
    }

@bp.route('/delete_all_medias', methods=['DELETE'])
@login_required
def delete_medias():
    current_app.logger.info("Deleting all medias")
    num_movies = Movie.query.delete()
    num_tv_shows = TVShow.query.delete()
    app_settings = AppSettings.query.first()
    Media.query.delete()
    app_settings.last_media_import = datetime.min
    db.session.commit()
    return {
        'message' : "Deleted "+str(num_movies)+" movies and "+str(num_tv_shows)+" TV shows"
    }

@bp.route('/delete_picks', methods=['DELETE'])
@login_required
def delete_picks():
    current_app.logger.info("Deleting all picks")
    numPicks = Pick.query.delete()
    db.session.commit()
    return {
        'message' : "Deleted "+str(numPicks)+" picks"
    }

@bp.route('/delete_users', methods=['DELETE'])
@login_required
def delete_users():
    current_app.logger.info("Deleting all non-admin users")
    numUsers = User.query.filter_by(admin=False).delete()
    db.session.commit()
    return {
        'message' : str(numUsers)+" non-admin users deleted"
    }