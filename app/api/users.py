from app.api import bp
from app.extensions import db
from flask import current_app
from flask_login import login_required
from app.decorators import admin_required
from app.scripts.media import delete_pick_and_check_abandoned
from app.models import User, Permission

@bp.route("/users/<int:user_id>/delete", methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_app.logger.info("Deleting user : "+str(user))
    if user.is_administrator():
        return {
            "error" : user.email+" is an admin and cannot be deleted"
        }, 400
    elif user.system_user:
        return {
            "error" : "Cannot delete a system user"
        }, 400
    for pick in user.picks:
        delete_pick_and_check_abandoned(pick)
    db.session.delete(user)
    db.session.commit()
    return {
        "message" : user.email+" has been deleted"
    }