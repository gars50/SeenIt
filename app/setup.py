from app.models.application_settings import AppSettings
from datetime import datetime
from app import db
import os

def setup_app():
    app_settings = AppSettings.query.first()
    if not app_settings:
        plex_id = os.urandom(24).hex()
        app_settings = AppSettings(expiryTimeNumber=0, lastMediaImport = datetime.min, plexClientID = plex_id, appName = "SeenIt")
        db.session.add(app_settings)
        db.session.commit()