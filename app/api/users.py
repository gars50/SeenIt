from app.api import bp
from app.extensions import db
from flask import current_app
from flask_login import login_required
from app.decorators import admin_required
from app.models import User

@bp.route("/users/<int:user_id>/delete", methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_app.logger.info(f'Deleting {user}')
    if user.is_administrator():
        return {
            "error" : user.email+" is an admin and cannot be deleted"
        }, 400
    elif user.is_system_user():
        return {
            "error" : "Cannot delete a system user"
        }, 400
    for pick in user.picks:
        temp_media = pick.media
        db.session.delete(pick)
        db.session.commit()
        temp_media.update_abandoned_details()
    db.session.delete(user)
    db.session.commit()
    return {
        "message" : user.email+" has been deleted"
    }