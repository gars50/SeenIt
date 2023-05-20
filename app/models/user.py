from app.extensions import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app.models.movie import Movie
from app.models.tvshow import TVShow

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    plexid = db.Column(db.Integer, unique=True)
    alias = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)
    lastlogin = db.Column(db.DateTime)

    #Relations
    tvshows = db.relationship('TVShow', backref='owner', lazy='dynamic')
    movies = db.relationship('Movie', backref='owner', lazy='dynamic')

    def __repr__(self) -> str:
        return f'User: {self.email}'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_admin(self, admin):
        self.admin = bool(admin)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))