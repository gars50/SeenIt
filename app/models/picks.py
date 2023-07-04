from app.extensions import db

class MoviePick(db.Model):
    __tablename__ = 'movie_pick'
    id = db.Column(db.Integer, primary_key=True)
    pick_method = db.Column(db.String(100))
    pick_date = db.Column(db.DateTime)

    #Relations
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

class TVShowSeasonPick(db.Model):
    __tablename__ = 'tv_show_season_pick'
    id = db.Column(db.Integer, primary_key=True)
    pick_method = db.Column(db.String(100))
    pick_date = db.Column(db.DateTime)

    #Relations
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tvShowSeason_id = db.Column(db.Integer, db.ForeignKey('tv_show_season.id'), nullable=False)