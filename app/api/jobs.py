from app.api import bp
from app.extensions import scheduler
from flask import current_app
from flask_login import login_required
from datetime import datetime

@bp.route("/jobs/trigger_update_medias_and_requests_job", methods=['POST'])
@login_required
def trigger_update_medias_and_requests_job():
    current_app.logger.info("Forcing a trigger of the update medias and requests job")
    scheduler.modify_job("update_medias_and_requests-job", next_run_time=datetime.utcnow())
    return {
        'message' : "Job triggered"
    }

@bp.route("/jobs/trigger_delete_expired_medias_job", methods=['POST'])
@login_required
def trigger_delete_expired_medias_job():
    current_app.logger.info("Forcing a trigger of the delete of expired medias job")
    scheduler.modify_job("delete_expired_medias-job", next_run_time=datetime.utcnow())
    return {
        'message' : "Job triggered"
    }