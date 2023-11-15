from app.media import bp
from flask_login import login_required
from flask import render_template
from app.decorators import super_user_required
from app.models import User
from flask_mobility.decorators import mobile_template

@bp.route("/abandoned_medias")
@login_required
@mobile_template("{mobile/}table_views/medias.html")
def abandoned_medias(template):
    return render_template(template, page_title="Abandoned Medias", page="abandoned_medias")

@bp.route("/all_medias")
@login_required
@mobile_template("{mobile/}table_views/medias.html")
def all_medias(template):
    return render_template(template, page_title="All Medias", page="all_medias")

@bp.route("/my_picks")
@login_required
@mobile_template("{mobile/}table_views/picks.html")
def my_picks(template):
    return render_template(template, page_title="My Picks", page="my_picks")

@bp.route("/permanent_picks")
@login_required
@mobile_template("{mobile/}table_views/picks.html")
def permanent_picks(template):
    permanent_user = User.query.filter_by(email="Permanent").first()
    return render_template(template, page_title="Permanent Collection", page="permanent_picks", user_id=permanent_user.id)

@bp.route("/user/<int:user_id>/picks")
@login_required
@super_user_required
@mobile_template("{mobile/}table_views/picks.html")
def user_picks(user_id, template):
    user = User.query.get_or_404(user_id)
    page_title = f'Picks for {user.alias} ({user.email})'
    return render_template(template, page_title=page_title, user_id=user_id)