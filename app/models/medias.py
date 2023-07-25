from app.extensions import db

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(100), nullable = False)

    ombi_id = db.Column(db.Integer, nullable = False)
    total_size = db.Column(db.Integer)
    expiry_date = db.Column(db.DateTime)
    deletion_date = db.Column(db.DateTime)

    picks = db.relationship('Pick', back_populates='media', cascade='all, delete')

    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': type
    }

class Movie(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    release_date = db.Column(db.DateTime, nullable=False)
    TMDB_id = db.Column(db.Integer, nullable=False, unique=True)
    TMDB_url = db.Column(db.String(100))
    radarr_id = db.Column(db.Integer, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "movie",
    }

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.release_date.strftime("%Y")})'


class TVShow(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    theTVDB_id = db.Column(db.Integer, nullable=False, unique=True)
    theTVDB_url = db.Column(db.String(100))
    sonarr_id = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "tv_show",
    }

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'