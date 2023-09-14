from app.api import bp
from flask import current_app, render_template
from flask_login import login_required, current_user
from app.models import Media
from app.scripts.media import delete_media_everywhere

@bp.route("/medias/<int:media_id>/picks_modal", methods=['GET'])
@login_required
def picks_modal(media_id):
    media = Media.query.get_or_404(media_id)
    content = render_template("media/picks_modal.html", media=media)
    return content

@bp.route("/medias/<int:media_id>/delete", methods=['DELETE'])
@login_required
def delete_media(media_id):
    if not current_user.admin:
        return {
            "error" : "Not allowed!"
        }, 405
    media = Media.query.get_or_404(media_id)
    current_app.logger.debug(str(current_user)+" is trying to delete "+str(media))
    script_result = delete_media_everywhere(media)
    return {
        "message" : script_result
    }