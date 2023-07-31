import logging
from flask import Flask, request
from datetime import datetime
from config import Config
from app.extensions import db, login, migrate, mail, moment, scheduler, logs
from app.setup import first_run_setup
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_extensions(app)
    register_blueprints(app)

    with app.app_context():
        scheduler.scheduler.add_jobstore(SQLAlchemyJobStore(engine=db.engine, metadata=db.metadata))
        scheduler.scheduler.configure(timezone='UTC')
        scheduler.start()
        import requests_cache
        requests_cache.install_cache('seenit_dns_cache')


    @app.before_first_request
    def before_first_request():
        first_run_setup()

    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response

    return app

def register_extensions(app):
    # Initialize Flask extensions here
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    moment.init_app(app)
    scheduler.init_app(app)
    logs.init_app(app)

    return None

def register_blueprints(app):
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

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return None