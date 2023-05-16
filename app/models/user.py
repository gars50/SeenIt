from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    plexid = db.Column(db.Integer, unique=True)
    alias = db.Column(db.String(100))
    admin = db.Column(db.Boolean())

    def __repr__(self) -> str:
        return f'User: {self.alias}'