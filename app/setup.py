import os
from app.models.application_settings import AppSettings
from datetime import datetime
from app import db, scheduler
from app.scripts.jobs import test_job
from flask import current_app

def first_run_setup():
    app_settings = AppSettings.query.first()
    if not app_settings:
        plex_id = os.urandom(24).hex()
        app_settings = AppSettings(expiryTimeNumber=0, lastMediaImport = datetime.min, plexClientID = plex_id, appName = "SeenIt")
        db.session.add(app_settings)
        db.session.commit()
    
    if not scheduler.get_jobs():
        scheduler.add_job(id='test-job', func=test_job, trigger='interval', minutes=5)