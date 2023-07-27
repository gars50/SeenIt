from flask import render_template
from app.main import bp
from app.models import Pick, Media, AppSettings
from flask_login import login_required, current_user

@bp.route("/")
@login_required
def index():
    app_settings = AppSettings.query.first()
    movie_picks = Pick.query.filter_by(user=current_user, media_type="movie")
    tv_show_picks = Pick.query.filter_by(user=current_user, media_type="tv_show")
    movie_picks_count = movie_picks.count()
    tv_show_picks_count = tv_show_picks.count()

    total_movie_size = 0
    total_tv_show_size = 0
    total_used_space = 0
    total_available_space = 19000000000000

    for movie_pick in movie_picks:
        total_movie_size += movie_pick.media.total_size

    for tv_show_pick in tv_show_picks:
        total_tv_show_size += tv_show_pick.media.total_size

    for media in Media.query.all():
        total_used_space += media.total_size

    return render_template("index.html", movie_picks_count=movie_picks_count, tv_show_picks_count=tv_show_picks_count, total_movie_size=total_movie_size, total_tv_show_size=total_tv_show_size, total_used_space=total_used_space, total_available_space=total_available_space, app_name=app_settings.app_name)