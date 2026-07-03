import os
from datetime import datetime, timezone
from http import HTTPStatus

from dotenv import load_dotenv
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

load_dotenv()


@auth_bp.post("/login")
def login():
    """
    Autentica al usuario mediante HTTP Basic Authentication y genera un
    token JWT para acceder a los recursos protegidos de la API.
    """
    auth = request.authorization

    # Valida que la petición incluya credenciales de autenticación.
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Authentication credentials are required."}), HTTPStatus.UNAUTHORIZED

    username = auth.username
    password = auth.password

    # Verifica que las credenciales coincidan con las configuradas en
    # las variables de entorno.
    if username != os.getenv("AUTH_USERNAME") or password != os.getenv("AUTH_PASSWORD"):
        return jsonify({"message": "Invalid credentials."}), HTTPStatus.UNAUTHORIZED

    # Genera el token JWT utilizando el nombre de usuario como identidad.
    access_token = create_access_token(identity=username)

    expires_delta = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    expires_at = datetime.now(timezone.utc) + expires_delta

    # Devuelve el token junto con su información de expiración.
    return (
        jsonify(
            {
                "access_token": access_token,
                "expires_at": expires_at.isoformat(),
                "expires_in": int(expires_delta.total_seconds()),
            }
        ),
        HTTPStatus.OK,
    )