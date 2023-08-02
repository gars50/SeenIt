from app.api import bp
from app.extensions import db, scheduler
from flask import json, request, current_app, render_template
from flask_login import login_required, current_user
from app.models import *
from datetime import datetime
from app.scripts.media import check_user_creation, check_movie_creation, check_tv_show_creation, check_pick_creation, delete_media_everywhere, check_if_abandonned, test_ombi, test_radarr, test_sonarr

@bp.route("/medias/<int:media_id>/picks_modal", methods=['GET'])
@login_required
def picks_modal(media_id):
    media = Media.query.get_or_404(media_id)
    picks = Pick.query.filter_by(media=media)
    content = render_template("media/picks_modal.html", picks=picks)
    return content

@bp.route("/medias/<int:media_id>/delete", methods=['DELETE'])
@login_required
def delete_media(media_id):
    if not current_user.admin:
        return {
            "error" : "Not allowed!"
        }, 405
    media = Media.query.get_or_404(media_id)
    current_app.logger.debug(str(current_user)+" is trying to delete "+str(media))
    script_result = delete_media_everywhere(media)
    return {
        "message" : script_result
    }

@bp.route("picks/<int:media_id>/add_current_user", methods=['PUT'])
@login_required
def add_pick(media_id):
    media = Media.query.get(media_id)
    check_pick_creation(media, current_user, datetime.utcnow(), "Picked up")
    return{
        "message" : "Picked up "+str(media)
    }

@bp.route("picks/<int:media_id>/add_permanent", methods=['PUT'])
@login_required
def add_pick_permanent_collection(media_id):
    media = Media.query.get(media_id)
    user = User.query.filter_by(email="permanent").first()
    check_pick_creation(media, user, datetime.utcnow(), "Picked up")
    return{
        "message" : str(media)+" added to the permanent collection"
    }

@bp.route("/picks/add_watching", methods=['PUT'])
def add_pick_watching():
    data = json.loads((request.data.decode("utf-8")))
    user, added_user = check_user_creation(data["email"], data["alias"])

    if data["type"] == "movie":
        #Only process if this is an actual movie
        if data["themoviedb_id"]:
            current_app.logger.info(str(user)+" started watching movie: "+data["title"])
            movie, added_movie = check_movie_creation(TMDB_id=data["themoviedb_id"])
            check_pick_creation(movie, user, datetime.utcnow(), "Watched")

    elif data["type"] == "tv_show":
        #Only process if this is an actual show
        if data["thetvdb_id"]:
            current_app.logger.info(str(user)+" started watching tv show: "+data["show_title"])
            tv_show, added_to_db = check_tv_show_creation(theTVDB_id=data["thetvdb_id"])
            check_pick_creation(tv_show, user, datetime.utcnow(), "Watched")
    return {}, 204

@bp.route("/picks/<int:pick_id>/delete", methods=['DELETE'])
@login_required
def delete_pick(pick_id):
    pick = Pick.query.get_or_404(pick_id)
    current_app.logger.debug("User "+current_user.alias+" is trying to delete pick "+str(pick))
    if (not current_user.admin) and (not current_user==pick.user):
        return {
            "error" : "Not allowed!"
        }, 405
    media = pick.media
    if pick.pick_method == "Ombi Request":
        #Should we delete the ombi request at this point and avoid double data in the db?
        current_app.logger.debug("Deleting Ombi Request for "+str(pick.media))
    db.session.delete(pick)
    db.session.commit()
    current_app.logger.info("User "+current_user.alias+" deleted "+str(pick))
    abandonned = check_if_abandonned(media)
    if abandonned:
        return{
            "message" : str(media)+" was let go. It has been abandonned as this was its last pick."
        }
    else:
        return{
            "message" : str(media)+" was let go. Others have picked this media, and it has not been abandonned yet."
        }

@bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_app.logger.info("Deleting user : "+str(user))
    if user.admin:
        return {
            "error" : user.email+" is an admin and cannot be deleted"
        }, 400
    db.session.delete(user)
    db.session.commit()
    return {
        "message" : user.email+" has been deleted"
    }

@bp.route('/jobs/trigger_update_medias_and_requests_job', methods=['POST'])
@login_required
def trigger_update_medias_and_requests_job():
    current_app.logger.info("Forcing a trigger of the update medias and requests job")
    scheduler.modify_job("update_medias_and_requests-job", next_run_time=datetime.utcnow())
    return {
        'message' : "Job triggered"
    }

@bp.route('/settings/test_ombi_from_server', methods=['POST'])
def test_ombi_from_server():
    ombi_host = request.json['ombi_host']
    ombi_port = request.json['ombi_port']
    ombi_api_key = request.json['ombi_api_key']
    return test_ombi(ombi_host, ombi_port, ombi_api_key)
    

@bp.route('/settings/test_radarr_from_server', methods=['POST'])
def test_radarr_from_server():
    radarr_host = request.json['radarr_host']
    radarr_port = request.json['radarr_port']
    radarr_api_key = request.json['radarr_api_key']
    return test_radarr(radarr_host, radarr_port, radarr_api_key)

@bp.route('/settings/test_sonarr_from_server', methods=['POST'])
def test_sonarr_from_server():
    sonarr_host = request.json['sonarr_host']
    sonarr_port = request.json['sonarr_port']
    sonarr_api_key = request.json['sonarr_api_key']
    return test_sonarr(sonarr_host, sonarr_port, sonarr_api_key)