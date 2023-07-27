import os
class Config:
    #Generate this key with os.urandom(24).hex()
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")