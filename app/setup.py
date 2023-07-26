import os
from app.models.application_settings import AppSettings
from datetime import datetime, timedelta
from app import db, scheduler
from app.scripts.jobs import update_medias_and_requests

def first_run_setup():
    app_settings = AppSettings.query.first()
    if not app_settings:
        plex_id = os.urandom(24).hex()
        app_settings = AppSettings(expiry_time_number=0, last_media_import = datetime.min, plex_client_id = plex_id, app_name = "SeenIt")
        db.session.add(app_settings)
        db.session.commit()

    if not scheduler.get_jobs():
        scheduler.add_job(id='update_medias_and_requests-job', func=update_medias_and_requests, next_run_time=datetime.utcnow() + timedelta(weeks=104), trigger='interval', minutes=10)