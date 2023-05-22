from app.extensions import db
from sqlalchemy import event

class RadarrConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    apiKey = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f'Radarr Connection: {self.host}:{self.port}'
    
class SonarrConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    apiKey = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f'Sonarr Connection: {self.host}:{self.port}'
    
class OmbiConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    apiKey = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f'Ombi Connection: {self.host}:{self.port}'