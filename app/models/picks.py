from app.extensions import db

class MoviePick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick_method = db.Column(db.String(100))
    pick_date = db.Column(db.DateTime)

    #Relations
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

class TVShowSeasonPick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick_method = db.Column(db.String(100))
    pick_date = db.Column(db.DateTime)

    #Relations
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tvShowSeason_id = db.Column(db.Integer, db.ForeignKey('tvShowSeason.id'), nullable=False)