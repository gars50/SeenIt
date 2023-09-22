import os
from app.models import AppSettings, User
from datetime import datetime, timedelta
from app import db, scheduler
from app.scripts.jobs import update_medias_and_requests, delete_all_expired_medias

def first_run_setup():
    app_settings = AppSettings.query.first()
    if not app_settings:
        plex_id = os.urandom(24).hex()
        app_settings = AppSettings(expiry_time_number=2, expiry_time_unit="weeks", free_space=100, next_delete=datetime.utcnow() + timedelta(weeks=104), deletion_time_number=1, deletion_time_unit="months", last_media_import=datetime.min, plex_client_id=plex_id, app_name="SeenIt")
        db.session.add(app_settings)
        db.session.commit()

    if not scheduler.get_jobs():
        scheduler.add_job(id='update_medias_and_requests-job', func=update_medias_and_requests, next_run_time=datetime.utcnow() + timedelta(weeks=104), trigger='interval', minutes=10)
        scheduler.add_job(id='delete_expired_medias-job', func=delete_all_expired_medias, next_run_time=datetime.utcnow() + timedelta(weeks=104), trigger='interval', days=1)

    permanent_user = User.query.filter_by(email="Permanent").first()
    if not permanent_user:
        permanent_user = User(alias="Permanent Collection", email="Permanent", system_user=True)
        db.session.add(permanent_user)
        db.session.commit()