import os

class Config:
    SQLALCHEMY_DATABASE_URI = "posgresql://kyra:15342282.k@kyradornish-748.postgres.pythonanywhere-services.com:10748/recipespinnerdb"
    SQLALCHEMY_POOL_RECYCLE = 299

    SECRET_KEY = 'super-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['kyradornish@gmail.com']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


# 'postgresql://kyra:ladies1271@localhost:5433/recipe_spinner'
