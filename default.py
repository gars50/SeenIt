class Config:
    #Generate this key with os.urandom(24).hex()
    SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

    SQLALCHEMY_DATABASE_URI = "sqlite:///SeenIt.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME="XXXX@XXXXX.XXX"
    MAIL_PASSWORD="XXXXXXXXXXXXX"
    SENDER="XXXXX@XXXXXX.XXX"