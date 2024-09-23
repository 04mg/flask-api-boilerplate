from flask import Flask
from werkzeug.exceptions import HTTPException
from .exceptions import handle_http_exception
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

    app.register_error_handler(HTTPException, handle_http_exception)

    return app
