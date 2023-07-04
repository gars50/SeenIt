from app.extensions import db

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    releaseDate = db.Column(db.DateTime)
    theMovieDbID = db.Column(db.Integer)
    theMovieDbURL = db.Column(db.String(100))
    ombiID = db.Column(db.Integer, unique=True)
    radarrID = db.Column(db.Integer, unique=True)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    picks = db.relationship('movie_pick', backref='movie', lazy='dynamic')

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.releaseDate.strftime("%Y")})'