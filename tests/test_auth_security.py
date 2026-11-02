"""Tests mínimos de seguridad: registro, JWT, cambio de contraseña, ownership."""

from app.models import Users
from app.security import hash_password, verify_password


def test_register_ignores_admin_type(client):
    res = client.post(
        "/register",
        json={
            "name": "Hacker",
            "email": "hacker@example.com",
            "password": "password123",
            "type": "admin",
        },
    )
    assert res.status_code == 200
    body = res.get_json()
    assert body["type"] == "user"
    user = Users.get(Users.user_email == "hacker@example.com")
    assert user.user_type == "user"
    assert user.user_password.startswith("$2")


def test_login_returns_jwt(client):
    client.post(
        "/register",
        json={"name": "A", "email": "a@example.com", "password": "password123"},
    )
    res = client.post(
        "/login", json={"email": "a@example.com", "password": "password123"}
    )
    assert res.status_code == 200
    assert res.get_json()["userToken"]


def test_login_rejects_bad_password(client):
    client.post(
        "/register",
        json={"name": "A", "email": "b@example.com", "password": "password123"},
    )
    res = client.post(
        "/login", json={"email": "b@example.com", "password": "wrongpass"}
    )
    assert res.status_code == 401


def test_view_profile_requires_auth(client):
    res = client.post("/viewProfile", json={})
    assert res.status_code == 401


def test_view_profile_ok_with_jwt(client, auth_headers):
    headers, data = auth_headers
    res = client.post("/viewProfile", headers=headers, json={})
    assert res.status_code == 200
    assert res.get_json()["message"][0]["email"] == data["email"]


def test_change_password_requires_current(client, auth_headers):
    headers, _ = auth_headers
    res = client.post(
        "/changePassword",
        headers=headers,
        json={"newPassword": "newpassword1"},
    )
    assert res.status_code == 400


def test_change_password_with_current(client, auth_headers):
    headers, data = auth_headers
    res = client.post(
        "/changePassword",
        headers=headers,
        json={"currentPassword": "password123", "newPassword": "newpassword1"},
    )
    assert res.status_code == 200
    login = client.post(
        "/login", json={"email": data["email"], "password": "newpassword1"}
    )
    assert login.status_code == 200


def test_all_users_forbidden_for_normal_user(client, auth_headers):
    headers, _ = auth_headers
    res = client.post("/allUsers", headers=headers, json={})
    assert res.status_code == 403


def test_legacy_sha256_migrates_on_login(client):
    import hashlib

    legacy = hashlib.sha256(b"password123").hexdigest()
    Users.create(
        user_name="Legacy",
        user_email="legacy@example.com",
        user_password=legacy,
        user_type="user",
        user_token="",
        user_image="/static/images/NonPerfil.webp",
    )
    res = client.post(
        "/login", json={"email": "legacy@example.com", "password": "password123"}
    )
    assert res.status_code == 200
    user = Users.get(Users.user_email == "legacy@example.com")
    assert user.user_password.startswith("$2")
    assert verify_password("password123", user.user_password)


def test_hash_password_bcrypt():
    h = hash_password("secret123")
    assert h.startswith("$2")
    assert verify_password("secret123", h)
    assert not verify_password("wrong", h)
