import json
from app.media import bp
from app import db
from datetime import datetime
from flask_login import login_required, current_user
from flask import render_template, request, current_app
from app.scripts.media import check_pick_creation, delete_media_everywhere, check_user_creation, check_movie_creation, check_tv_show_creation, modify_deletion_date
from app.models import Media, Movie, TVShow, Pick, AppSettings

def check_if_abandonned(media):
    abandonned = (not media.picks)
    #If this was the last pick that was just deleted, we need to set the expiryDate and deletionDate
    if abandonned:
        media.abandonned_date = datetime.utcnow()
        modify_deletion_date([media])
        current_app.logger.info(str(media)+" has been abandonned.")
    return abandonned

@bp.route("/abandonned_movies")
def abandonned_movies():
    movies = Movie.query.filter_by(picks=None)
    return render_template("media/abandonned_movies.html", movies=movies)

@bp.route("/abandonned_shows")
def abandonned_shows():
    tv_shows = TVShow.query.filter_by(picks=None)
    return render_template("media/abandonned_shows.html", tv_shows=tv_shows)

@bp.route("/my_movies")
@login_required
def my_movies():
    movie_picks = Pick.query.filter_by(user=current_user, media_type="movie")
    return render_template("media/my_movies.html", movie_picks=movie_picks)

@bp.route("/my_shows")
@login_required
def my_shows():
    tv_show_picks = Pick.query.filter_by(user=current_user, media_type="tv_show")
    return render_template("media/my_shows.html", tv_show_picks=tv_show_picks)

@bp.route("/all_movies")
@login_required
def all_movies():
    all_movies = Movie.query.all()
    return render_template("media/all_movies.html", movies=all_movies)

@bp.route("/all_shows")
@login_required
def all_shows():
    all_tv_shows = TVShow.query.all()
    return render_template("media/all_shows.html", tv_shows=all_tv_shows)

@bp.route("/<int:media_id>/add_pick", methods=['POST'])
@login_required
def add_pick(media_id):
    media = Media.query.get(media_id)
    check_pick_creation(media, current_user, datetime.utcnow(), "Picked up")
    return{
        "message" : "Picked up "+str(media)
    }

@bp.route("/pick/<int:pick_id>/delete", methods=['DELETE'])
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


@bp.route("/<int:media_id>/delete", methods=['DELETE'])
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

@bp.route("/<int:media_id>/picks_modal", methods=['GET'])
@login_required
def picks_modal(media_id):
    media = Media.query.get_or_404(media_id)
    picks = Pick.query.filter_by(media=media)
    content = render_template("media/picks_modal.html", picks=picks)
    return content

@bp.route("/add_pick_watching", methods=['POST'])
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