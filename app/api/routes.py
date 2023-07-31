from app.api import bp
from app import db, scheduler
from flask import json, request, current_app, render_template
from flask_login import login_required, current_user
from app.models import *
from datetime import datetime
from app.scripts.media import check_user_creation, check_movie_creation, check_tv_show_creation, check_pick_creation, delete_media_everywhere, check_if_abandonned

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

@bp.route("picks/<int:media_id>/add", methods=['POST'])
@login_required
def add_pick(media_id):
    media = Media.query.get(media_id)
    check_pick_creation(media, current_user, datetime.utcnow(), "Picked up")
    return{
        "message" : "Picked up "+str(media)
    }

@bp.route("/picks/add_watching", methods=['POST'])
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

@bp.route('/medias/delete_all', methods=['DELETE'])
@login_required
def delete_medias():
    current_app.logger.info("Deleting all medias")
    num_movies = Movie.query.delete()
    num_tv_shows = TVShow.query.delete()
    app_settings = AppSettings.query.first()
    Media.query.delete()
    app_settings.last_media_import = datetime.min
    db.session.commit()
    return {
        'message' : "Deleted "+str(num_movies)+" movies and "+str(num_tv_shows)+" TV shows"
    }

@bp.route('/picks/delete_all', methods=['DELETE'])
@login_required
def delete_picks():
    current_app.logger.info("Deleting all picks")
    numPicks = Pick.query.delete()
    db.session.commit()
    return {
        'message' : "Deleted "+str(numPicks)+" picks"
    }

@bp.route('users/delete_all', methods=['DELETE'])
@login_required
def delete_users():
    current_app.logger.info("Deleting all non-admin users")
    numUsers = User.query.filter_by(admin=False).delete()
    db.session.commit()
    return {
        'message' : str(numUsers)+" non-admin users deleted"
    }