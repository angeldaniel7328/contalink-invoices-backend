import logging

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, swagger, jwt
from app.routes import register_routes
from app.scheduler import start_scheduler


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(name)s:%(funcName)s: %(message)s")

    db.init_app(app)
    swagger.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    app.url_map.strict_slashes = False

    register_routes(app)

    start_scheduler(app)

    return app