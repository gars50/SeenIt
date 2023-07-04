from app.extensions import db

class TVShow(db.Model):
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
    seasons = db.relationship('TVShowSeason', backref='tvShow', lazy='dynamic')

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'


class TVShowSeason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seasonNubmer = db.Column(db.Integer, nullable=False)

    ombiID = db.Column(db.Integer)
    sonarrID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    deletionDate = db.Column(db.DateTime)

    #Relations
    tvShow_id = db.Column(db.Integer, db.ForeignKey('tvShow.id'), nullable=False)

    picks = db.relationship('TVShowSeasonPick', backref='tvShowSeason', lazy='dynamic')

    def __repr__(self) -> str:
        return f'{self.tvShow.title}: Season {self.seasonNumber}'