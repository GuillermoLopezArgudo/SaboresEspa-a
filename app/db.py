import os

from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase

from app.config import Config, parse_database_url

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass


def build_database():
    """
    Prioridad:
    1) DATABASE_URL → PostgreSQL (Neon/Render)
    2) USE_SQLITE=1 o sin MYSQL_HOST → SQLite local
    3) MySQL (docker-compose)
    """
    if Config.DATABASE_URL:
        info = parse_database_url(Config.DATABASE_URL)
        kwargs = {}
        if info.get("sslmode"):
            kwargs["sslmode"] = info["sslmode"]
        return PostgresqlDatabase(
            info["name"],
            user=info["user"],
            password=info["password"],
            host=info["host"],
            port=info["port"],
            **kwargs,
        )

    use_sqlite = Config.USE_SQLITE or (
        os.getenv("USE_SQLITE") is None and not os.getenv("MYSQL_HOST")
    )
    if use_sqlite:
        return SqliteDatabase(Config.SQLITE_PATH)

    return MySQLDatabase(
        Config.MYSQL_DB,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
    )


db = build_database()
