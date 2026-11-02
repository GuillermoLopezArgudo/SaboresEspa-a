import hashlib
from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.models import Users

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    user_type = data.get("type") or "user"

    if not name or not email or not password:
        return jsonify(message="ERROR"), 400
    if Users.select().where(Users.user_email == email).exists():
        return jsonify(message="ERROR"), 409

    token = create_access_token(identity=email)
    user = Users(
        user_name=name,
        user_email=email,
        user_password=hashlib.sha256(password.encode("utf-8")).hexdigest(),
        user_type=user_type,
        user_token=token,
        user_image="/static/images/NonPerfil.webp",
        created_at=date.today(),
        modified_at=date.today(),
    )
    user.save()
    return jsonify(userToken=token, iduser=user.id, type=user.user_type)


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify(message="ERROR User NOT LOGGED"), 400

    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = Users.get_or_none(
        (Users.user_email == email) & (Users.user_password == password_hash)
    )
    if not user:
        return jsonify(message="ERROR User NOT LOGGED"), 401

    token = create_access_token(identity=email)
    Users.update(user_token=token).where(Users.id == user.id).execute()
    return jsonify(userToken=token, iduser=user.id, type=user.user_type)
