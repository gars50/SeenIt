from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
moment = Moment()
scheduler = APScheduler()

login = LoginManager()
login.login_view = 'auth.login_choice'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "info"