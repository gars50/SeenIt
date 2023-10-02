from app.media import bp
from flask_login import login_required, current_user
from flask import render_template
from app.models import Movie, TVShow, Pick, User

@bp.route("/abandonned_medias")
def abandonned_medias():
    return render_template("table_views/medias.html", page_title="Abandonned Medias", page="abandonned_medias", abandonned_page=True)

@bp.route("/all_medias")
@login_required
def all_medias():
    return render_template("table_views/medias.html", page_title="All Medias", page="all_medias")

@bp.route("/my_picks")
@login_required
def my_picks():
    return render_template("table_views/picks.html", page_title="My Picks", page="my_picks")

@bp.route("/permanent_picks")
def permanent_picks():
    permanent_user = User.query.filter_by(email="Permanent").first()
    return render_template("table_views/picks.html", page_title="Permanent Collection", page="permanent_picks", user_id=permanent_user.id)

@bp.route("/user/<int:user_id>/picks")
@login_required
def user_picks(user_id):
    user = User.query.get_or_404(user_id)
    page_title="Picks for "+user.alias+" ("+user.email+")"
    return render_template("table_views/picks.html", page_title=page_title, user_id=user_id)