import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import  Marshmallow

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

# import views
from .clients.views import clients
from .studio.views import studio
from .booking.views import bookings


def create_app():
    """Construct the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # add extensions
    register_extensions(app)

    # add blueprints
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    with app.app_context():
        db.create_all()
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(clients)
    app.register_blueprint(studio)
    app.register_blueprint(bookings)
    return None
