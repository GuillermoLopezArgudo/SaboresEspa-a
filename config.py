import os
from urllib.parse import urlparse, unquote


def _parse_database_url(url: str):
    """Soporta postgres://, postgresql:// y postgresql+psycopg:// (Neon / Render)."""
    normalized = url.strip()
    for prefix in ("postgresql+psycopg://", "postgres://"):
        if normalized.startswith(prefix):
            normalized = "postgresql://" + normalized[len(prefix) :]
            break

    parsed = urlparse(normalized)
    db_name = (parsed.path or "/").lstrip("/") or "sabores"
    return {
        "name": db_name,
        "user": unquote(parsed.username) if parsed.username else None,
        "password": unquote(parsed.password) if parsed.password else None,
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "sslmode": "require" if "sslmode=require" in (parsed.query or "") or "neon.tech" in (parsed.hostname or "") else None,
    }


class Config:
    # MySQL local (docker-compose) — solo si no hay DATABASE_URL
    MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "1234")
    MYSQL_DB = os.getenv("MYSQL_DB", "recipesSpain")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))

    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "cambia-este-secreto-en-produccion")
    CORS_ORIGINS = [
        o.strip()
        for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8080,http://127.0.0.1:8080",
        ).split(",")
        if o.strip()
    ]
