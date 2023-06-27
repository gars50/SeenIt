from app.extensions import db

class TVShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    tvdbid = db.Column(db.Integer)
    totalSize = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'

    def changeOwner(self, newOwner):
        self.owner_id = newOwner.id