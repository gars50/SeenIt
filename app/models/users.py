import jwt
from flask import current_app
from app.extensions import db, login
from time import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

def default_alias(context):
    return context.get_current_parameters()['email']

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    alias = db.Column(db.String(100), default=default_alias)
    last_seen = db.Column(db.DateTime(), default=None)
    movie_storage_usage = db.Column(db.BigInteger, default=0)
    show_storage_usage = db.Column(db.BigInteger, default=0)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    picks = db.relationship('Pick', back_populates='user', cascade='all, delete')

    def __repr__(self) -> str:
        return f'User: {self.email}'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def is_super_user(self):
        return self.can(Permission.SUPERUSER)

    def is_system_user(self):
        return self.role.name == "System User"

    def set_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        self.role = role
        db.session.add(self)
        db.session.commit()

    def set_alias(self, alias):
        self.alias = alias
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config["SECRET_KEY"], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def admins_count():
        num_admins = 0
        for user in User.query.all():
            if (user.is_administrator()):
                num_admins += 1
        return num_admins

    @staticmethod
    def insert_system_users():
        users = {
            'Permanent',
        }
        for u in users:
            user = User.query.filter_by(email=u).first()
            if user is None:
                user = User(email=u)
                db.session.add(user)
                db.session.commit()
                user.set_role('System User')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
    def is_super_user(self):
        return False

login.anonymous_user = AnonymousUser

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

    @staticmethod
    def insert_roles():
        roles = {
            'User': [],
            'System User': [],
            'Power User': [Permission.SUPERUSER],
            'Administrator': [Permission.ADMIN, Permission.SUPERUSER],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class Permission:
    #Use binary
    ADMIN = 1
    SUPERUSER = 2