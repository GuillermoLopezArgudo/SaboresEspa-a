import hashlib
import re
from functools import wraps

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models import Users

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_COMMENT_LEN = 2000
MAX_NAME_LEN = 255
MAX_QUANTITY_LEN = 50
MAX_STEP_TITLE_LEN = 255


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, stored: str) -> bool:
    if not stored:
        return False
    if not isinstance(stored, str):
        stored = str(stored)
    if stored.startswith("$2"):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
        except Exception:
            # Hash corrupto / truncado: tratar como credencial inválida, no 500
            return False
    try:
        return hashlib.sha256(password.encode("utf-8")).hexdigest() == stored
    except Exception:
        return False



def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email) and len(email) <= 255)


def _bearer_token() -> str:
    auth = request.headers.get("Authorization") or ""
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return ""


def resolve_user_from_jwt(*, optional: bool = False) -> Users | None:
    """Resuelve usuario por JWT (identity = id numérico) + user_token (revocación).

    Identidades email legacy se rechazan (forzar re-login).
    """
    verify_jwt_in_request(optional=optional)
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        # No aceptar identity email: saltaba la revocación por user_token
        return None

    user = Users.get_or_none(Users.id == user_id)
    if not user:
        return None

    token = _bearer_token()
    if not user.user_token:
        return None
    if token and user.user_token != token:
        return None
    return user


def get_current_user() -> Users | None:
    """Usuario autenticado vía JWT; el token debe coincidir con user_token (revocación)."""
    return resolve_user_from_jwt(optional=False)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user = get_current_user()
        except Exception:
            return jsonify(message="No autenticado"), 401
        if not user:
            return jsonify(message="No autenticado"), 401
        return fn(user, *args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user = get_current_user()
        except Exception:
            return jsonify(message="No autenticado"), 401
        if not user:
            return jsonify(message="No autenticado"), 401
        if user.user_type != "admin":
            return jsonify(message="No autorizado"), 403
        return fn(user, *args, **kwargs)

    return wrapper
