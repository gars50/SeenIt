import math
from app.media import bp
from app import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_login import login_required, current_user
from flask import render_template
from app.scripts.media import check_pick_creation
from app.models import Media, Movie, TVShow, Pick, AppSettings

def check_if_abandonned(media):
    #If this was the last pick that was just deleted, we need to set the expiryDate and deletionDate
    if (not media.picks):
        app_settings = AppSettings.query.first()
        media.expiryDate = datetime.utcnow() + relativedelta(**{app_settings.expiryTimeUnit: app_settings.expiryTimeNumber})
        
        delete_time = app_settings.nextDelete
        if (delete_time < media.expiryDate):
            #Find the next deletion date that lands after the expiration date
            deletion_delta = relativedelta(**{app_settings.deletionTimeUnit: app_settings.deletionTimeNumber})
            while delete_time < media.expiryDate:
                delete_time += deletion_delta
            #There should be a faster way to calculate this, but I do not know it
            #It shouldn't have a big impact anyway.
            #This method does not work because division of relativedelta is not doable.
            #deltaMulti = math.ceil(relativedelta(media.expiryDate, delete_time)/deletion_delta)
            #delete_time = deltaMulti * deletion_delta
        media.deletionDate = delete_time
        db.session.commit()

@bp.route("/abandonned_movies")
def abandonned_movies():
    movies = Movie.query.filter_by(picks=None)
    return render_template("media/abandonned_movies.html", movies=movies)

@bp.route("/abandonned_shows")
def abandonned_shows():
    tvShows = TVShow.query.filter_by(picks=None)
    return render_template("media/abandonned_shows.html", tvShows=tvShows)

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
    all_tvShows = TVShow.query.all()
    return render_template("media/all_shows.html", tvShows=all_tvShows)

@bp.route("/<int:media_id>/add_pick", methods=['POST'])
@login_required
def add_pick(media_id):
    media = Media.query.get(media_id)
    check_pick_creation(media, current_user, datetime.utcnow(), "Picked up")
    return{
        "message" : "Picked up "+media.title
    }

@bp.route("/pick/<int:pick_id>/delete", methods=['DELETE'])
@login_required
def delete_pick(pick_id):
    pick = Pick.query.get_or_404(pick_id)
    media = pick.media
    db.session.delete(pick)
    db.session.commit()
    check_if_abandonned(media)
    return{
        "message" : "Pick of "+media.title+" deleted"
    }

@bp.route("/<int:media_id>/delete", methods=['DELETE'])
@login_required
def delete_media(media_id):
    media = Media.query.get_or_404(media_id)
    title = media.title
    db.session.delete(media)
    db.session.commit()
    return {
        "message" : "Deleted "+title
    }

@bp.route("/<int:media_id>/picks_modal", methods=['GET'])
@login_required
def picks_modal(media_id):
    media = Media.query.get_or_404(media_id)
    picks = Pick.query.filter_by(media=media)
    content = render_template("media/picks_modal.html", picks=picks)
    return content