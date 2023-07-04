from app.extensions import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    releaseDate = db.Column(db.DateTime)
    theMovieDbID = db.Column(db.Integer)
    theMovieDbURL = db.Column(db.String(100))
    ombiID = db.Column(db.Integer)
    radarrID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    picks = db.relationship('MoviePick', backref='movie', lazy='dynamic')

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.releaseDate.strftime("%Y")})'