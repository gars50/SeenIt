from app.extensions import db
from sqlalchemy import event

class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick_method = db.Column(db.String(100))
    pick_date = db.Column(db.DateTime)
    media_type = db.Column(db.String(50))

    #Relations
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))

    user = db.relationship('User', back_populates='picks')
    media = db.relationship('Media', back_populates='picks')

    #Ensures that a new pick has all its information, and the correct media type is set
    def __init__(self, user, media, pick_date, pick_method):
        self.user = user
        self.media = media
        self.media_type = media.type
        self.pick_date = pick_date
        self.pick_method = pick_method

    def __repr__(self) -> str:
        return f'{self.media} requested by {self.user} on {self.pick_date} through {self.pick_method}'