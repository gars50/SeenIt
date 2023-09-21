from app.extensions import db

class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expiry_time_number = db.Column(db.Integer)
    expiry_time_unit = db.Column(db.String(50))
    
    next_delete = db.Column(db.DateTime)
    deletion_time_number = db.Column(db.Integer)
    deletion_time_unit = db.Column(db.String(50))

    last_media_import = db.Column(db.DateTime)
    free_space = db.Column(db.BigInteger)

    radarr_host = db.Column(db.String(100))
    radarr_port = db.Column(db.Integer)
    radarr_api_key = db.Column(db.String(100))

    sonarr_host = db.Column(db.String(100))
    sonarr_port = db.Column(db.Integer)
    sonarr_api_key = db.Column(db.String(100))   

    ombi_host = db.Column(db.String(100))
    ombi_port = db.Column(db.Integer)
    ombi_api_key = db.Column(db.String(100))

    plex_client_id = db.Column(db.String(100))
    app_name = db.Column(db.String(100))
    safe_mode = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'''
        Expire timer: {self.expiry_time_number} {self.expiry_time_unit}
        Radarr Connection: {self.radarr_host}:{self.radarr_port}
        Sonarr Connection: {self.sonarr_host}:{self.sonarr_port}
        Ombi Connection: {self.ombi_host}:{self.ombi_port}'''