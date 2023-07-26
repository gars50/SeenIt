from flask import Flask
from config import Config
from app.extensions import db, login, migrate, mail, moment, scheduler
from app.setup import first_run_setup
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    moment.init_app(app)
    scheduler.init_app(app)

    with app.app_context():
        scheduler.scheduler.add_jobstore(SQLAlchemyJobStore(engine=db.engine, metadata=db.metadata))
        scheduler.scheduler.configure(timezone='UTC')
        scheduler.start()

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix="/settings")

    from app.media import bp as media_bp
    app.register_blueprint(media_bp, url_prefix='/media')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/errors')

    @app.before_first_request
    def before_first_request():
        first_run_setup()

    return app