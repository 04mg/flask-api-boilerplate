from flask import Flask
from .extensions import db, migrate, cors, oauth
from .routes import register_routes
from .config import Config
from .oauth_registry import register_oauth


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    oauth.init_app(app)
    register_oauth()

    register_routes(app)

    return app
