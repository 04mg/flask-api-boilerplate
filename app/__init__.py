from flask import Flask
from .extensions import db, migrate, api
from .routes import register_routes
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    register_routes(api)
    api.init_app(app)

    return app
