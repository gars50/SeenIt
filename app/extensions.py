from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

login = LoginManager()
login.login_view = 'auth.login_choice'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "info"