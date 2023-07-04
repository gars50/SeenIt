from app.extensions import db

class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    pick_method = db.Column(db.String(100))
    pick_date = db.Column(db.DateTime)

    #Relations
    picker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
    }

class MoviePick(Pick):
    id = db.Column(db.Integer, db.ForeignKey('pick.id'), primary_key=True)

    #Relations
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    __mapper_args__ = {
        "polymorphic_identity": "moviePick",
    }

    def __repr__(self) -> str:
        return f'{self.movie} requested by {self.picker} on {self.pick_date} through {self.pick_method}'


class TVShowPick(Pick):
    id = db.Column(db.Integer, db.ForeignKey('pick.id'), primary_key=True)

    #Relations
    tvShow_id = db.Column(db.Integer, db.ForeignKey('tv_show.id'))

    __mapper_args__ = {
        "polymorphic_identity": "tvShowPick",
    }

    def __repr__(self) -> str:
        return f'{self.tvShow} requested by {self.picker} on {self.pick_date} through {self.pick_method}'