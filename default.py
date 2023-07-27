import os
class Config:
    #Generate this key with os.urandom(24).hex()
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")

    # Logging Setup
    LOG_TYPE = os.environ.get("LOG_TYPE", "stream")  # Default is a Stream handler
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # File Logging Setup
    LOG_DIR = os.environ.get("LOG_DIR", "./logs")
    APP_LOG_NAME = os.environ.get("APP_LOG_NAME", "app.log")
    WWW_LOG_NAME = os.environ.get("WWW_LOG_NAME", "www.log")
    LOG_MAX_BYTES = os.environ.get("LOG_MAX_BYTES", 100_000_000)  # 100MB in bytes
    LOG_COPIES = os.environ.get("LOG_COPIES", 5)

    #Used if you are serving this application in a subfolder of a domain
    #For example https:google.ca/seenit instead of https:google.ca/
    #You would have to put APPLICATION_ROOT="/seenit"
    APPLICATION_ROOT=""