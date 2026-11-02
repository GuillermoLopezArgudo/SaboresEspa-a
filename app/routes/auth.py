from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from peewee import IntegrityError

from app.config import Config
from app.models import Users
from app.rate_limit import rate_limit
from app.security import hash_password, is_valid_email, login_required, verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
@rate_limit(Config.AUTH_RATE_LIMIT, Config.AUTH_RATE_WINDOW, prefix="register")
def register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify(message="Datos incompletos"), 400
    if not is_valid_email(email):
        return jsonify(message="Email no válido"), 400
    if len(password) < 8:
        return jsonify(message="La contraseña debe tener al menos 8 caracteres"), 400
    if Users.select().where(Users.user_email == email).exists():
        return jsonify(message="El email ya está registrado"), 409

    # Nunca confiar en type del cliente
    user = Users(
        user_name=name,
        user_email=email,
        user_password=hash_password(password),
        user_type="user",
        user_token="",
        user_image="/static/images/NonPerfil.webp",
        created_at=date.today(),
        modified_at=date.today(),
    )
    try:
        user.save()
    except IntegrityError:
        return jsonify(message="El email ya está registrado"), 409

    token = create_access_token(identity=str(user.id))
    Users.update(user_token=token).where(Users.id == user.id).execute()
    return jsonify(userToken=token, iduser=user.id, type=user.user_type)


@auth_bp.post("/login")
@rate_limit(Config.AUTH_RATE_LIMIT, Config.AUTH_RATE_WINDOW, prefix="login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify(message="Credenciales inválidas"), 400

    user = Users.get_or_none(Users.user_email == email)
    if not user or not verify_password(password, user.user_password):
        return jsonify(message="Credenciales inválidas"), 401

    # Migrar hash legacy SHA-256 → bcrypt
    if not user.user_password.startswith("$2"):
        Users.update(user_password=hash_password(password)).where(
            Users.id == user.id
        ).execute()

    token = create_access_token(identity=str(user.id))
    Users.update(user_token=token).where(Users.id == user.id).execute()
    return jsonify(userToken=token, iduser=user.id, type=user.user_type)


@auth_bp.post("/logout")
@login_required
def logout(current_user):
    Users.update(user_token="", modified_at=date.today()).where(
        Users.id == current_user.id
    ).execute()
    return jsonify(message="Sesión cerrada")
