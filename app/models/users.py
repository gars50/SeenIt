import jwt
from flask import current_app
from app.extensions import db, login
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

def default_alias(context):
    return context.get_current_parameters()['email']

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    alias = db.Column(db.String(100), default=default_alias)
    admin = db.Column(db.Boolean, default=False)
    superuser = db.Column(db.Boolean, default=False)
    system_user = db.Column(db.Boolean, default=False)
    movie_storage_usage = db.Column(db.BigInteger, default=0)
    show_storage_usage = db.Column(db.BigInteger, default=0)

    picks = db.relationship('Pick', back_populates='user', cascade='all, delete')

    def __repr__(self) -> str:
        return f'User: {self.email}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_admin(self, admin):
        self.admin = bool(admin)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config["SECRET_KEY"], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    def reset_permissions(self):
        self.permissions = 0
    def has_permission(self, perm):
        return self.permissions & perm == perm

class Permission:
    ADMIN = 1
    SUPERUSER = 2