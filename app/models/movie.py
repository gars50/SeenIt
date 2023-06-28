from app.extensions import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    releaseDate = db.Column(db.DateTime)
    theMovieDbID = db.Column(db.Integer)
    theMovieDbURL = db.Column(db.String(100))
    ombiID = db.Column(db.Integer)
    radarrID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    abandonnedDate = db.Column(db.DateTime)
    deleteDate = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.releaseDate.strftime("%Y")})'
    
    def setExpiryDate(self, date):
        self.expiryDate = date