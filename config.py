import os
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
url = os.getenv('DB_URL')
db = os.getenv('DB')


class Config:
    """Set Flask configuration vars from .env file."""
    global user
    global password
    global db
    global url

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
        .format(user=user, pw=password, url=url, db=db)
    # General
    TESTING = True
    FLASK_DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'SECRET'

    # Database
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = True
