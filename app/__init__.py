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
    app.config["UPLOAD_FOLDER_IMAGES"] = Config.UPLOAD_FOLDER_IMAGES
    app.config["UPLOAD_FOLDER_VIDEOS"] = Config.UPLOAD_FOLDER_VIDEOS
    app.config["ALLOWED_EXTENSIONS"] = Config.ALLOWED_EXTENSIONS

    os.makedirs(app.config["UPLOAD_FOLDER_IMAGES"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER_VIDEOS"], exist_ok=True)

    CORS(
        app,
        resources={r"/*": {"origins": Config.CORS_ORIGINS}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        expose_headers=["Content-Type"],
    )
    JWTManager(app)
    register_blueprints(app)

    try:
        create_tables()
    except Exception as exc:
        print(f"[warn] create_tables: {exc}")

    return app


# Compatibilidad con gunicorn "app:app" (comando antiguo en Render)
app = create_app()

