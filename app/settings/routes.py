from flask import render_template, flash, redirect, request, url_for, current_app
from app import db
from app.settings import bp
from app.scripts.media import modify_deletion_date
from app.models import User, AppSettings, Media
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
            current_app.logger.info("Deletion settings have been changed. Updating deletion date of abandonned medias.")
            abandonned_medias = Media.query.filter_by(picks=None)
            modify_deletion_date(abandonned_medias)
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
        try:
            last_admin = User.query.filter_by(admin=True).one()
        except Exception as err:
            current_app.logger.info("More than one admin or none : "+str(err))
            last_admin = None
        
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