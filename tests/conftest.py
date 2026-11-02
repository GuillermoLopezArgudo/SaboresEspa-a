import os
import tempfile
import uuid

# Forzar SQLite aislado antes de importar la app (ignorar Neon/MySQL del entorno)
os.environ["USE_SQLITE"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ.pop("MYSQL_HOST", None)
os.environ["JWT_SECRET_KEY"] = "test-secret-key-at-least-32-bytes!!"

_fd, _sqlite_path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["SQLITE_PATH"] = _sqlite_path

import pytest

from app import create_app
from app.db import db
from app.models import create_tables


@pytest.fixture()
def app():
    application = create_app()
    application.config["TESTING"] = True
    with application.app_context():
        if db.is_closed():
            db.connect(reuse_if_open=True)
        create_tables()
        yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    """Registra un usuario y devuelve headers Authorization."""
    email = f"user-{uuid.uuid4().hex[:10]}@example.com"
    res = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
            "type": "admin",  # debe ignorarse
        },
    )
    assert res.status_code == 200, res.get_json()
    data = res.get_json()
    assert data["type"] == "user"
    data["email"] = email
    token = data["userToken"]
    return {"Authorization": f"Bearer {token}"}, data
