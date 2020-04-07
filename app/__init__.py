import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')

db = SQLAlchemy()
migrate = Migrate()

from app.clients.views import clients


def create_app():
    """Construct the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # load db
    db.init_app(app)
    # load migrations
    migrate.init_app(app, db)
    with app.app_context():

        # register blueprints
        app.register_blueprint(clients)

        # create table for models
        db.create_all()
        return app
