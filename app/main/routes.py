from flask import render_template
from app.main import bp
from app.models import Pick, Media, AppSettings
from flask_login import current_user

@bp.route("/")
def index():
    app_settings = AppSettings.query.first()

    delete_date = app_settings.next_delete

    total_used_space = 0
    for media in Media.query.all():
        total_used_space += media.total_size

    total_space = total_used_space + app_settings.free_space

    total_space_to_be_freed = 0
    for media in Media.query.filter_by(picks=None):
        total_space_to_be_freed += media.total_size

    if current_user.is_authenticated:
        movie_picks = Pick.query.filter_by(user=current_user, media_type="movie")
        tv_show_picks = Pick.query.filter_by(user=current_user, media_type="tv_show")
        movie_picks_count = movie_picks.count()
        tv_show_picks_count = tv_show_picks.count()

        return render_template("index.html", 
                               movie_picks_count=movie_picks_count,
                               tv_show_picks_count=tv_show_picks_count,
                               total_movie_size=current_user.movie_storage_usage,
                               total_tv_show_size=current_user.show_storage_usage,
                               total_used_space=total_used_space,
                               free_space=app_settings.free_space,
                               total_space_to_be_freed=total_space_to_be_freed,
                               total_space=total_space,
                               delete_date=delete_date,
                               app_name=app_settings.app_name)
    else:
        return render_template("index.html", 
                               total_used_space=total_used_space,
                               free_space=app_settings.free_space,
                               total_space_to_be_freed=total_space_to_be_freed,
                               total_space=total_space,
                               delete_date=delete_date,
                               app_name=app_settings.app_name)

@bp.route("/test")
def test():
    return render_template("mobile/table_views/picks.html")