from app.extensions import db

class TVShow(db.Model):
    __tablename__ = 'tv_show'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    tvDbID = db.Column(db.Integer)
    tvDbURL = db.Column(db.String(100))
    ombiID = db.Column(db.Integer)
    sonarrID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    seasons = db.relationship('tv_show_season', backref='tvShow', lazy='dynamic')

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'


class TVShowSeason(db.Model):
    __tablename__ = 'tv_show_season'
    id = db.Column(db.Integer, primary_key=True)
    seasonNubmer = db.Column(db.Integer, nullable=False)

    ombiID = db.Column(db.Integer)
    sonarrID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    tvShow_id = db.Column(db.Integer, db.ForeignKey('tv_show.id'), nullable=False)

    picks = db.relationship('tv_show_season_pick', backref='tvShowSeason', lazy='dynamic')

    def __repr__(self) -> str:
        return f'{self.tvShow.title}: Season {self.seasonNumber}'