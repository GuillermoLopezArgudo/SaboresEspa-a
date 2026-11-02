import os
import sys
from datetime import timedelta
from urllib.parse import unquote, urlparse


def parse_database_url(url: str) -> dict:
    """Soporta postgres://, postgresql:// y postgresql+psycopg:// (Neon / Render)."""
    normalized = url.strip()
    for prefix in ("postgresql+psycopg://", "postgres://"):
        if normalized.startswith(prefix):
            normalized = "postgresql://" + normalized[len(prefix) :]
            break

    parsed = urlparse(normalized)
    db_name = (parsed.path or "/").lstrip("/") or "sabores"
    host = parsed.hostname or "localhost"
    return {
        "name": db_name,
        "user": unquote(parsed.username) if parsed.username else None,
        "password": unquote(parsed.password) if parsed.password else None,
        "host": host,
        "port": parsed.port or 5432,
        "sslmode": (
            "require"
            if "sslmode=require" in (parsed.query or "") or "neon.tech" in host
            else None
        ),
    }


def _is_production() -> bool:
    env = (os.getenv("FLASK_ENV") or os.getenv("ENV") or "").strip().lower()
    if env in {"production", "prod"}:
        return True
    # Render / Vercel / similar
    return bool(os.getenv("RENDER") or os.getenv("DYNO") or os.getenv("K_SERVICE"))


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "1234")
    MYSQL_DB = os.getenv("MYSQL_DB", "recipesSpain")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))

    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
    SQLITE_PATH = os.getenv("SQLITE_PATH", "sabores_local.db")
    USE_SQLITE = os.getenv("USE_SQLITE", "").strip().lower() in {"1", "true", "yes"}

    _raw_jwt = os.getenv("JWT_SECRET_KEY", "").strip()
    _default_jwt = "dev-only-change-me"
    if _is_production() and (not _raw_jwt or _raw_jwt == _default_jwt):
        print(
            "[fatal] JWT_SECRET_KEY debe estar definido en producción "
            "(no uses el valor por defecto).",
            file=sys.stderr,
        )
        sys.exit(1)
    JWT_SECRET_KEY = _raw_jwt or _default_jwt
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_HOURS", "12"))
    )

    CORS_ORIGINS = [
        o.strip().rstrip("/")
        for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8080,http://127.0.0.1:8080,"
            "http://localhost:5173,http://127.0.0.1:5173,"
            "https://sabores-espana-one.vercel.app",
        ).split(",")
        if o.strip()
    ]

    # Rutas absolutas (Render/gunicorn no siempre usa el cwd esperado)
    _ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    UPLOAD_FOLDER_IMAGES = os.path.join(_ROOT, "static", "images")
    UPLOAD_FOLDER_VIDEOS = os.path.join(_ROOT, "static", "videos")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4", "mov", "avi", "webm"}

    # Cloudinary (recomendado en Render). Si no hay credenciales → disco local.
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL", "").strip()
    USE_CLOUDINARY = bool(
        CLOUDINARY_URL
        or (CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)
    )

    AUTH_RATE_LIMIT = int(os.getenv("AUTH_RATE_LIMIT", "20"))  # intentos
    AUTH_RATE_WINDOW = int(os.getenv("AUTH_RATE_WINDOW", "300"))  # segundos

    IS_PRODUCTION = _is_production()
