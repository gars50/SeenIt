from app.extensions import db

class TVShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    tvDbID = db.Column(db.Integer)
    tvDbURL = db.Column(db.String(100))
    ombiID = db.Column(db.Integer)
    sonarrID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    picks = db.relationship('TVShowPick', backref='tvShow', lazy='dynamic')

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'