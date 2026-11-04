from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from peewee import IntegrityError

from app.config import Config
from app.models import Users
from app.rate_limit import rate_limit
from app.security import (
    MAX_NAME_LEN,
    hash_password,
    is_valid_email,
    login_required,
    verify_password,
)

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
    if len(name) > MAX_NAME_LEN:
        return jsonify(message=f"Nombre demasiado largo (máx. {MAX_NAME_LEN})"), 400
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
    return jsonify(
        userToken=token,
        iduser=user.id,
        type=user.user_type,
        name=user.user_name,
        email=user.user_email,
        image=user.user_image,
    )


@auth_bp.post("/login")
@rate_limit(Config.AUTH_RATE_LIMIT, Config.AUTH_RATE_WINDOW, prefix="login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify(message="Credenciales inválidas"), 400

    from app.models import with_db_retry

    def _do_login():
        user = Users.get_or_none(Users.user_email == email)
        if not user or not verify_password(password, user.user_password):
            return None, jsonify(message="Credenciales inválidas"), 401

        # Migrar hash legacy SHA-256 → bcrypt
        stored = user.user_password or ""
        if not stored.startswith("$2"):
            Users.update(user_password=hash_password(password)).where(
                Users.id == user.id
            ).execute()

        token = create_access_token(identity=str(user.id))
        Users.update(user_token=token).where(Users.id == user.id).execute()
        return (
            True,
            jsonify(
                userToken=token,
                iduser=user.id,
                type=user.user_type,
                name=user.user_name,
                email=user.user_email,
                image=user.user_image or "",
            ),
            200,
        )

    try:
        _ok, payload, status = with_db_retry(_do_login)
        return payload, status
    except Exception as exc:
        # Evitar HTML 500 genérico en el cliente durante deploys / fallos puntuales
        print(f"[error] login: {exc}")
        return jsonify(message="No se pudo iniciar sesión. Inténtalo de nuevo."), 503



@auth_bp.post("/logout")
@login_required
def logout(current_user):
    Users.update(user_token="", modified_at=date.today()).where(
        Users.id == current_user.id
    ).execute()
    return jsonify(message="Sesión cerrada")
