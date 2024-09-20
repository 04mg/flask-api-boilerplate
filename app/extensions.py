from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(origins=Config.CORS_ORIGINS)
oauth = OAuth()
