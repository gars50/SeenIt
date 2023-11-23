from flask import render_template, flash, redirect, request, url_for, current_app
from app import db
from app.decorators import admin_required, super_user_required
from app.settings import bp
from app.models import User, AppSettings, Media, Pick, Movie, TVShow
from app.settings.forms import EditUserForm, AddUserForm, EditAppSettings
from flask_login import login_required

@bp.route('/application', methods=['GET', 'POST'])
@login_required
@admin_required
def application():
    num_picks = Pick.query.count()
    num_movies = Movie.query.count()
    num_shows = TVShow.query.count()
    app_settings = AppSettings.query.first()
    form = EditAppSettings()
    if form.validate_on_submit():
        deletion_settings_changed = (
            app_settings.expiry_time_number != form.expiry_time_number.data or
            app_settings.expiry_time_unit != form.expiry_time_unit.data or
            app_settings.next_delete != form.next_delete.data or
            app_settings.deletion_time_number != form.deletion_time_number.data or
            app_settings.deletion_time_unit != form.deletion_time_unit.data
        )
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
        if deletion_settings_changed:
            current_app.logger.info("Deletion settings have been changed. Updating deletion date of abandoned medias.")
            Media.update_all_deletion_details()
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
    return render_template('settings/application.html', form=form, num_picks=num_picks, num_movies=num_movies, num_shows=num_shows)

@bp.route('/users')
@login_required
@super_user_required
def users():
    users = User.query.all()
    return render_template('settings/users.html', users=users)

@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        #If this user is the last admin and admin is removed, we deny it.
        if (user.is_administrator() and (User.admins_count() <= 1)) and (form.role.data != "Administrator"):
            flash('Cannot disable the last administrator', "error")
        elif (user.is_system_user()):
            flash('Cannot change a system user', "error")
        else:
            user.set_role(form.role.data)
            user.set_alias(form.alias.data)
            flash('Your changes have been saved.', "success")
        return redirect(url_for('settings.users'))
    elif request.method == 'GET':
        form.email.data = user.email
        form.alias.data = user.alias
        form.role.data = user.role.name
        return render_template('settings/user.html', form=form)

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, alias=form.alias.data)
        db.session.add(user)
        db.session.commit()
        user.set_role(form.role.data)
        flash('User has been added.', "success")
        return redirect(url_for('settings.users'))
    return render_template('settings/add_user.html', form=form)

@bp.route('/logs')
@login_required
@admin_required
def logs():
    return render_template('settings/logs.html')