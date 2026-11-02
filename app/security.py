import hashlib
from functools import wraps

import bcrypt
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models import Users


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, stored: str) -> bool:
    if not stored:
        return False
    # bcrypt
    if stored.startswith("$2"):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
        except ValueError:
            return False
    # legacy SHA-256 (TFG) → migrar en login
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == stored


def get_current_user() -> Users | None:
    """Usuario autenticado vía JWT (identity = id de usuario)."""
    verify_jwt_in_request()
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return Users.get_or_none(Users.user_email == identity)
    return Users.get_or_none(Users.id == user_id)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify(message="No autenticado"), 401
        return fn(user, *args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify(message="No autenticado"), 401
        if user.user_type != "admin":
            return jsonify(message="No autorizado"), 403
        return fn(user, *args, **kwargs)

    return wrapper
