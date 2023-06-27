from app.extensions import db

class TVShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    tvDbId = db.Column(db.Integer)
    ombiID = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    abandonnedDate = db.Column(db.DateTime)
    deleteDate = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'

    def changeOwner(self, newOwner):
        self.owner_id = newOwner.id

    def setExpiryDate(self, date):
        self.expiryDate = date