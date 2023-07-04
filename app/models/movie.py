from app.extensions import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    releaseDate = db.Column(db.DateTime, nullable = False)
    theMovieDbID = db.Column(db.Integer, nullable = False, unique=True)
    theMovieDbURL = db.Column(db.String(100))
    ombiID = db.Column(db.Integer, nullable = False, unique=True)
    radarrID = db.Column(db.Integer, unique=True)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    picks = db.relationship('MoviePick', backref='movie', lazy='dynamic')

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.releaseDate.strftime("%Y")})'