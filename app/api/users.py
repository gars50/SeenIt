from app.api import bp
from app.extensions import db
from flask import current_app
from flask_login import login_required
from app.models import User

@bp.route("/users/<int:user_id>/delete", methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_app.logger.info("Deleting user : "+str(user))
    if user.admin:
        return {
            "error" : user.email+" is an admin and cannot be deleted"
        }, 400
    db.session.delete(user)
    db.session.commit()
    return {
        "message" : user.email+" has been deleted"
    }