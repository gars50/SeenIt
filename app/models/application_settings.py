from app.extensions import db

class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delayNumber = db.Column(db.Integer)
    delayUnit = db.Column(db.String(50))
    radarrHost = db.Column(db.String(100))
    radarrPort = db.Column(db.Integer)
    radarrApiKey = db.Column(db.String(100))
    sonarrHost = db.Column(db.String(100))
    sonarrPort = db.Column(db.Integer)
    sonarrApiKey = db.Column(db.String(100))    
    ombiHost = db.Column(db.String(100))
    ombiPort = db.Column(db.Integer)
    ombiApiKey = db.Column(db.String(100))
    lastMediaImport = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f'''
        Delay timer: {self.delayNumber} {self.delayUnit}
        Radarr Connection: {self.radarrHost}:{self.radarrPort}
        Sonarr Connection: {self.sonarrHost}:{self.sonarrPort}
        Ombi Connection: {self.ombiHost}:{self.ombiPort}'''