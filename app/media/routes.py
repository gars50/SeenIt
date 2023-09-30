from app.media import bp
from flask_login import login_required, current_user
from flask import render_template
from app.models import Movie, TVShow, Pick, User

@bp.route("/abandonned_medias")
def abandonned_medias():
    return render_template("views/medias.html", page_title="Abandonned Medias", page="abandonned_medias")

@bp.route("/my_picks")
@login_required
def my_picks():
    movie_picks = Pick.query.filter_by(user=current_user, media_type="movie")
    return render_template("views/picks.html", page_title="My Picks", page="my_picks")

@bp.route("/permanent_picks")
def permanent_picks():
    permanent_user = User.query.filter_by(email="Permanent").first()
    return render_template("views/picks.html", page_title="Permanent Collection", page="permanent_picks")

@bp.route("/all_medias")
@login_required
def all_medias():
    return render_template("views/medias.html", page_title="All Medias", page="all_medias")

@bp.route("/user/<int:user_id>/medias/")
@login_required
def user_medias(user_id):
    return render_template("views/picks.html")