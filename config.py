from os import environ


class Config:
    """Set Flask configuration vars from .env file."""
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='maclean', pw='camarosss',
                                                                   url='127.0.0.1:5432', db='studios')
    # General
    TESTING = True
    FLASK_DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'SECRET'

    # Database
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = True
