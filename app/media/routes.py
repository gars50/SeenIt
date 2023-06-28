from app.media import bp
from flask_login import login_required
from flask import render_template
from app.models import Movie, TVShow

@bp.route("/abandonnedmovies")
def abandonnedmovies():
    return render_template("media/abandonnedmovies.html")

@bp.route("/abandonnedshows")
def abandonnedshows():
    return render_template("media/abandonnedshows.html")

@bp.route("/mymovies")
@login_required
def mymovies():
    return render_template("media/mymovies.html")

@bp.route("/myshows")
@login_required
def myshows():
    return render_template("media/myshows.html")

@bp.route("/allmovies")
@login_required
def allmovies():
    movies = Movie.query.all()
    return render_template("media/allmovies.html", movies=movies)

@bp.route("/allshows")
@login_required
def allshows():
    tvshows = TVShow.query.all()
    return render_template("media/allshows.html", tvshows=tvshows)