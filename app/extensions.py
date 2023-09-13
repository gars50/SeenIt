from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_apscheduler import APScheduler
from app.flask_logs import LogSetup
from requests_cache import CachedSession

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
mail = Mail()
moment = Moment()
scheduler = APScheduler()
logs = LogSetup()
cache_session = CachedSession(expire_after=30)

login = LoginManager()
login.login_view = 'auth.login_choice'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "info"