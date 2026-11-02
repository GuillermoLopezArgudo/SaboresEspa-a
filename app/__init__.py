import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import Config
from app.models import create_tables
from app.routes import register_blueprints


def create_app() -> Flask:
    app = Flask(__name__, static_folder="../static", static_url_path="/static")
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["UPLOAD_FOLDER_IMAGES"] = Config.UPLOAD_FOLDER_IMAGES
    app.config["UPLOAD_FOLDER_VIDEOS"] = Config.UPLOAD_FOLDER_VIDEOS
    app.config["ALLOWED_EXTENSIONS"] = Config.ALLOWED_EXTENSIONS

    os.makedirs(app.config["UPLOAD_FOLDER_IMAGES"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER_VIDEOS"], exist_ok=True)

    CORS(
        app,
        resources={r"/*": {"origins": Config.CORS_ORIGINS}},
        supports_credentials=False,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin",
        ],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        expose_headers=["Content-Type"],
        always_send=True,
    )
    JWTManager(app)
    register_blueprints(app)

    @app.after_request
    def _ensure_cors(response):
        # Refuerzo por si un 4xx/5xx de proxy pierde cabeceras en preflight
        origin = None
        try:
            from flask import request as flask_request

            origin = flask_request.headers.get("Origin")
        except Exception:
            origin = None
        if origin and origin.rstrip("/") in {o.rstrip("/") for o in Config.CORS_ORIGINS}:
            response.headers.setdefault("Access-Control-Allow-Origin", origin)
            response.headers.setdefault(
                "Access-Control-Allow-Headers",
                "Content-Type, Authorization, X-Requested-With, Accept, Origin",
            )
            response.headers.setdefault(
                "Access-Control-Allow-Methods",
                "GET, POST, PUT, PATCH, DELETE, OPTIONS",
            )
        return response

    try:
        create_tables()
    except Exception as exc:
        print(f"[warn] create_tables: {exc}")

    return app


# Compatibilidad con gunicorn "app:app" (comando antiguo en Render)
app = create_app()

