from flask import render_template
from app.main import bp
from flask_login import login_required

@bp.route("/")
def index():
    return render_template("index.html")