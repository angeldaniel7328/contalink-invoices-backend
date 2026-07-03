import logging

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, swagger, jwt
from app.routes import register_routes


def create_app(config_class=Config):
    """
    Crea e inicializa la aplicación Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configura el formato de los mensajes registrados por el logger.
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(name)s:%(funcName)s: %(message)s")

    # Inicializa las extensiones utilizadas por la aplicación.
    db.init_app(app)
    swagger.init_app(app)
    jwt.init_app(app)

    # Habilita CORS para permitir el acceso a la API desde clientes externos.
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    # Permite acceder a las rutas con o sin barra diagonal al final.
    app.url_map.strict_slashes = False

    # Registra los blueprints que exponen los endpoints de la aplicación.
    register_routes(app)

    return app