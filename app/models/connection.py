from app.extensions import db

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    apiKey = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f'Connection: {self.name}'