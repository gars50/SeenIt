from flask import render_template
from app.main import bp

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/mymovies")
def mymovies():
    return render_template("mymovies.html")

@bp.route("/myshows")
def myshows():
    return render_template("myshows.html")

@bp.route("/abandonnedmovies")
def abandonnedmovies():
    return render_template("abandonnedmovies.html")

@bp.route("/abandonnedshows")
def abandonnedshows():
    return render_template("abandonnedshows.html")