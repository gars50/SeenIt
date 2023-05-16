from flask import render_template
from app.settings import bp
from app.extensions import db
from app.models.user import User

@bp.route('/')
def index():
    return render_template('settings/index.html')

@bp.route('/users')
def users():
    users = User.query.all()
    return render_template('settings/users.html', users=users)

@bp.route('/connections')
def connections():
    return render_template('settings/connections.html')