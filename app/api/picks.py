from app.api import bp
from app.extensions import db
from flask import json, request, current_app
from flask_login import login_required, current_user
from app.models import Media, User, Pick
from datetime import datetime
from app.scripts.media import check_user_creation, check_movie_creation, check_tv_show_creation, check_pick_creation, check_if_abandonned

@bp.route("/picks/<int:media_id>/add_to_current_user", methods=['PUT'])
@login_required
def add_pick_to_current_user(media_id):
    media = Media.query.get(media_id)
    check_pick_creation(media, current_user, datetime.utcnow(), "Picked up")
    return{
        "message" : "Picked up "+str(media)
    }

@bp.route("/picks/<int:media_id>/add_permanent", methods=['PUT'])
@login_required
def add_pick_permanent_collection(media_id):
    media = Media.query.get(media_id)
    permanent_user = User.query.filter_by(email="permanent").first()
    check_pick_creation(media, permanent_user, datetime.utcnow(), "Assigned")
    return{
        "message" : str(media)+" added to the permanent collection"
    }

@bp.route("/picks/add_watching", methods=['PUT'])
def add_pick_watching():
    data = json.loads((request.data.decode("utf-8")))
    current_app.logger.debug(data["email"]+" started watching something.")
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
    user = pick.user
    if pick.pick_method == "Ombi Request":
        #Should we delete the ombi request at this point and avoid double data in the db?
        current_app.logger.debug("Deleting Ombi Request for "+str(pick.media))
    db.session.delete(pick)
    db.session.commit()
    current_app.logger.info("User "+current_user.alias+" deleted "+str(pick))
    abandonned = check_if_abandonned(media, user)
    if abandonned:
        return{
            "message" : str(media)+" was let go. It has been abandonned as this was its last pick."
        }
    else:
        return{
            "message" : str(media)+" was let go. Others have picked this media, and it has not been abandonned yet."
        }