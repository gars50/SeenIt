from app.extensions import db

def default_TMDB_url(context):
    return "https://www.themoviedb.org/movie/"+str(context.get_current_parameters()['TMDB_id'])

def default_theTVDB_url(context):
    return "https://www.thetvdb.com/?id="+str(context.get_current_parameters()['theTVDB_id'])+"&tab=series"

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(100), nullable = False)

    ombi_id = db.Column(db.Integer, nullable = False)
    total_size = db.Column(db.BigInteger)
    poster_url = db.Column(db.String(100))

    abandoned_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    deletion_date = db.Column(db.DateTime)

    picks = db.relationship('Pick', back_populates='media', cascade='all, delete')

    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': type
    }

    def to_dict(self) :
        if self.type == "movie":
            media_db_url = self.TMDB_url
            full_title = self.title+" ("+str(self.year)+")"
        else:
            media_db_url = self.theTVDB_url
            full_title = self.title
        num_picks = len(self.picks)
        return {
                'title': full_title,
                'media_db_url': media_db_url,
                'poster_url': self.poster_url,
                'media_size': self.total_size,
                'abandoned_date': self.abandoned_date,
                'deletion_date': self.deletion_date,
                'num_picks': num_picks,
                'media_id': self.id,
                'media_type': self.type
            }

class Movie(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    TMDB_id = db.Column(db.Integer, nullable=False, unique=True)
    TMDB_url = db.Column(db.String(100), default=default_TMDB_url)
    radarr_id = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "movie",
    }

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.year})'


class TVShow(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    theTVDB_id = db.Column(db.Integer, nullable=False, unique=True)
    theTVDB_url = db.Column(db.String(100), default=default_theTVDB_url)
    sonarr_id = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "tv_show",
    }

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'