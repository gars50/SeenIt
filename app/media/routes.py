from app.media import bp
from flask_login import login_required, current_user
from flask import render_template
from app.models import Movie, TVShow, Pick, User

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

@bp.route("/user/<int:user_id>/movies/")
@login_required
def user_movies(user_id):
    user = User.query.get_or_404(user_id)
    movie_picks = Pick.query.filter_by(user=user, media_type="movie")
    return render_template("media/user_movies.html", movie_picks=movie_picks, user=user)

@bp.route("/user/<int:user_id>/shows/")
@login_required
def user_shows(user_id):
    user = User.query.get_or_404(user_id)
    tv_show_picks = Pick.query.filter_by(user=user, media_type="tv_show")
    return render_template("media/user_shows.html", tv_show_picks=tv_show_picks, user=user)

@bp.route("/permanent_movies")
def permanent_movies():
    permanent_user = User.query.filter_by(email="Permanent").first()
    movie_picks = Pick.query.filter_by(user=permanent_user, media_type="movie")
    return render_template("media/permanent_movies.html", movie_picks=movie_picks)

@bp.route("/permanent_shows")
def permanent_shows():
    permanent_user = User.query.filter_by(email="Permanent").first()
    tv_show_picks = Pick.query.filter_by(user=permanent_user, media_type="tv_show")
    return render_template("media/permanent_shows.html", tv_show_picks=tv_show_picks)

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