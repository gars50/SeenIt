from flask import render_template, redirect, url_for, flash, session, abort, current_app, request
from app.auth import bp
from app.extensions import db
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateProfile
from app.scripts.email import send_password_reset_email
from app.models import User, AppSettings
import requests
import urllib.parse

@bp.route('/login_choice', methods=['GET'])
def login_choice():
    app_settings = AppSettings.query.first()
    return render_template('auth/login_choice.html', app_name=app_settings.app_name)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or user.system_user or not user.password_hash or not user.check_password(form.password.data):
            flash('Invalid username or password', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_choice'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #If there are no admin users, we create one
        if not User.query.filter_by(admin=True).first():
            user = User(email=form.email.data, admin=True)
            user.set_password(form.password.data)
            db.session.add(user)
            current_app.logger.info("User with email "+user.email+" was created as an admin as it is the first user to log in.")
        else:
            #We verify the user is allowed to register
            user = User.query.filter_by(email=form.email.data).first()
            if not user or user.system_user:
                flash("You are not allowed to register.", "error")
                return redirect(url_for('auth.login'))
            elif user.password_hash:
                flash("Account is already registered. Reset your password if it was forgotten.", "warning")
                return redirect(url_for('auth.login'))
            else:
                user.set_password(form.password.data)
        db.session.commit()
        flash("Congratulations, you are now a registered user!", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', "info")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.", "info")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = current_user
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.password.data:
            user.set_password(form.password.data)
        user.alias = form.alias.data
        db.session.commit()
        flash('Your settings has been changed.', "success")
        return redirect(url_for('auth.login'))
    elif request.method == 'GET':
        form.alias.data = user.alias
    return render_template('auth/update_profile.html', form=form)

@bp.route('/plex_login')
def plex_login():
    app_settings = AppSettings.query.first()
    
    #We ask Plex for an id and code to create the URL for authentication
    url = "https://plex.tv/api/v2/pins"
    headers = {
        "accept": "application/json"
    }
    data = {
        "X-Plex-Product": app_settings.app_name,
        "X-Plex-Client-Identifier": app_settings.plex_client_id,
        "strong": "true"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
    except requests.ConnectionError as err:
        abort(500)


    #Parse the response and ready the url to give to the user to authenticate
    id = response.json().get('id')
    code = response.json().get('code')
    call_back_url = url_for('auth.plex_callback', _external=True)
    session['plex_oauth_id'] = id
    session['plex_oauth_code'] = code
    params = {
        "clientID": app_settings.plex_client_id,
        "code": code,
        "forwardUrl": call_back_url,
        "context%5Bdevice%5D%5Bproduct%5D": app_settings.app_name
    }
    params_url = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    full_plex_url = "https://app.plex.tv/auth/#?"+params_url
    return redirect(full_plex_url)

@bp.route('/plex_callback')
def plex_callback():
    app_settings = AppSettings.query.first()

    if not session['plex_oauth_code'] or not session['plex_oauth_id']:
        flash('Error while logging in Plex', "error")
        return redirect(url_for('auth.login_choice'))
    
    #Verify if the PIN has been claimed
    verify_pin_url = "https://plex.tv/api/v2/pins/"+str(session['plex_oauth_id'])
    headers = {
        "accept": "application/json"
    }
    data = {
        "X-Plex-Client-Identifier": app_settings.plex_client_id,
        "X-Plex-Token": session['plex_oauth_code']
    }
    response = requests.get(verify_pin_url, headers=headers, data=data)
    plex_auth_token = response.json().get('authToken')
    if not plex_auth_token:
        flash('Login to Plex failed', "error")
        return redirect(url_for('auth.login_choice'))
    
    #If it was successfully claimed, we verify the user's email
    verify_user_url = "https://plex.tv/api/v2/user"
    headers = {
        "accept": "application/json"
    }
    data = {
        "X-Plex-Product": app_settings.app_name,
        "X-Plex-Client-Identifier": app_settings.plex_client_id,
        "X-Plex-Token": plex_auth_token
    }
    response = requests.get(verify_user_url, headers=headers, data=data)
    user_email = response.json().get('email')
    
    user = User.query.filter_by(email=user_email).first()
    current_app.logger.debug("User with email "+user_email+" is trying to login through Plex. Corresponding user: "+str(user))
    #If there are no admin users, we create one
    if not User.query.filter_by(admin=True).first():
        user = User(email=user_email, admin=True)  
        db.session.add(user)
        db.session.commit()
        current_app.logger.info("User with email "+user.email+" was created as an admin as it is the first user to log in.")
    #If the user is not in the list, we do not allow them to login
    if user is None or user.system_user:
            flash("You are not allowed to login.", "error")
            return redirect(url_for('auth.login'))
    login_user(user, remember=True)
    current_app.logger.info(str(user)+" logged in.")
    return redirect(url_for('main.index'))