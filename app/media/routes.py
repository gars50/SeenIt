from app.media import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template
from app.models import Movie, TVShow, Pick

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
    return render_template("media/my_movies.html", moviePicks=current_user.movie_picks)

@bp.route("/my_shows")
@login_required
def my_shows():
    return render_template("media/my_shows.html", tvShowPicks=current_user.tvshow_picks)

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

@bp.route("/movie/<int:movie_id>/change_owner", methods=['POST'])
@login_required
def change_movie_owner(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie.owner_id:
        movie.owner_id = None
        db.session.commit()
        return{
            "message" : "Abandonned "+movie.title
        }
    else:
        movie.owner_id = current_user.id
        db.session.commit()
        return{
            "message" : "Adopted "+movie.title
        }

@bp.route("/pick/<int:pick_id>/delete", methods=['DELETE'])
@login_required
def delete_pick(pick_id):
    pick = Pick.query.get_or_404(pick_id)
    db.session.delete(pick)
    db.session.commit()
    return{
        "message" : "Abandonned "+pick.media.title
    }

@bp.route("/movie/<int:movie_id>/delete", methods=['DELETE'])
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie.picks)
    db.session.delete(movie)
    db.session.commit()
    return {
        "message" : "Deleted "+movie.title
    }

@bp.route("/tv_show/<int:show_id>/delete", methods=['DELETE'])
@login_required
def delete_tv_show(show_id):
    tvShow = TVShow.query.get_or_404(show_id)
    db.session.delete(tvShow.picks)
    db.session.delete(tvShow)
    db.session.commit()
    return {
        "message" : "Deleted "+tvShow.title
    }