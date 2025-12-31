import os

db_user = os.environ.get('DB_USER')
db_passwd = os.environ.get('DB_PASSWD')
db_host = os.environ.get('DB_HOST')

secret_key = os.environ.get('SECRET_KEY')

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_passwd}@{db_host}/applogs"
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
    }
    SECRET_KEY = secret_key