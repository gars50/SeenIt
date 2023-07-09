from app.extensions import db

class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expiryTimeNumber = db.Column(db.Integer)
    expiryTimeUnit = db.Column(db.String(50))
    
    nextDelete = db.Column(db.DateTime)
    deletionInterval = db.Column(db.DateTime)
    deletionTimeNumber = db.Column(db.Integer)
    deletionTimeUnit = db.Column(db.String(50))

    lastMediaImport = db.Column(db.DateTime)
    importInterval = db.Column(db.DateTime)
    nextImportDate = db.Column(db.DateTime)

    radarrHost = db.Column(db.String(100))
    radarrPort = db.Column(db.Integer)
    radarrApiKey = db.Column(db.String(100))

    sonarrHost = db.Column(db.String(100))
    sonarrPort = db.Column(db.Integer)
    sonarrApiKey = db.Column(db.String(100))   

    ombiHost = db.Column(db.String(100))
    ombiPort = db.Column(db.Integer)
    ombiApiKey = db.Column(db.String(100))

    plexClientID = db.Column(db.String(100))
    appName = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f'''
        Expire timer: {self.expiryTimeNumber} {self.expiryTimeUnit}
        Radarr Connection: {self.radarrHost}:{self.radarrPort}
        Sonarr Connection: {self.sonarrHost}:{self.sonarrPort}
        Ombi Connection: {self.ombiHost}:{self.ombiPort}'''