from app.media import bp
from flask_login import login_required, current_user
from flask import render_template
from app.models import Movie, TVShow

@bp.route("/abandonned_movies")
def abandonned_movies():
    movies = Movie.query.filter_by(owner_id="")
    return render_template("media/abandonned_movies.html", movies=movies)

@bp.route("/abandonned_shows")
def abandonned_shows():
    tvShows = TVShow.query.filter_by(owner_id="")
    return render_template("media/abandonned_shows.html", tvShows=tvShows)

@bp.route("/my_movies")
@login_required
def my_movies():
    movies = Movie.query.filter_by(owner_id=current_user.id)
    return render_template("media/my_movies.html", movies=movies)

@bp.route("/my_shows")
@login_required
def my_shows():
    tvShows = TVShow.query.filter_by(owner_id=current_user.id)
    return render_template("media/my_shows.html", tvShows=tvShows)

@bp.route("/all_movies")
@login_required
def all_movies():
    movies = Movie.query.all()
    return render_template("media/all_movies.html", movies=movies)

@bp.route("/all_shows")
@login_required
def all_shows():
    tvShows = TVShow.query.all()
    return render_template("media/all_shows.html", tvShows=tvShows)

@bp.route("/movies/<int:movie_id>/change_owner", methods=['POST'])
@login_required
def change_movie_owner(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie.owner_id:
        movie.owner_id = ""
    else:
        movie.owner_id = current_user.id

@bp.route("/tv_show/<int:show_id>/change_owner", methods=['POST'])
@login_required
def change_tvshow_owner(show_id):
    tvShow = TVShow.query.get_or_404(show_id)
    if tvShow.owner_id:
        tvShow.owner_id = ""
    else:
        tvShow.owner_id = current_user.id