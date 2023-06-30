from flask import render_template, redirect, url_for, flash
from app.auth import bp
from app.extensions import db
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.scripts.email import send_password_reset_email
from app.models.user import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.password_hash or not user.check_password(form.password.data):
            flash('Invalid username or password', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #If there are no users, we create an admin
        if not User.query.first():
            user = User(email=form.email.data)
            user.set_password(form.password.data)    
            user.set_admin('true')
            db.session.add(user)
        else:
            #We verify the user is allowed to register
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
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
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been changed.', "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/update_profile.html', form=form)

@bp.route('/login_choice', methods=['GET'])
def login_choice():
    return render_template('auth/login_choice.html')

@bp.route('/get_plex_auth', methods=['GET'])
def get_plex_auth():
    return True