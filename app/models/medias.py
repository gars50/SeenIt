from app.extensions import db

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(100), nullable = False)

    ombiID = db.Column(db.Integer, nullable = False)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    picks = db.relationship('Pick', back_populates='media', cascade='all, delete')

    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': type
    }

class Movie(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    releaseDate = db.Column(db.DateTime, nullable=False)
    theMovieDbID = db.Column(db.Integer, nullable=False, unique=True)
    theMovieDbURL = db.Column(db.String(100))
    radarrID = db.Column(db.Integer, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "movie",
    }

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.releaseDate.strftime("%Y")})'


class TVShow(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    tvDbID = db.Column(db.Integer, nullable=False, unique=True)
    tvDbURL = db.Column(db.String(100))
    sonarrID = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "tv_show",
    }

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'