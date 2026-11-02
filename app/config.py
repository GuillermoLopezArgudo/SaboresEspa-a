import os
from urllib.parse import urlparse, unquote


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


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "1234")
    MYSQL_DB = os.getenv("MYSQL_DB", "recipesSpain")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))

    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
    # Local sin Docker/Neon: SQLite por defecto
    SQLITE_PATH = os.getenv("SQLITE_PATH", "sabores_local.db")
    USE_SQLITE = os.getenv("USE_SQLITE", "").strip().lower() in {"1", "true", "yes"}

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-change-me")
    CORS_ORIGINS = [
        o.strip().rstrip("/")
        for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8080,http://127.0.0.1:8080,https://sabores-espana-one.vercel.app",
        ).split(",")
        if o.strip()
    ]

    UPLOAD_FOLDER_IMAGES = os.path.join("static", "images")
    UPLOAD_FOLDER_VIDEOS = os.path.join("static", "videos")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}
