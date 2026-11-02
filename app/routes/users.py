import hashlib
from datetime import date

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token

from app.models import (
    Recipe,
    RecipeComment,
    RecipeFilter,
    RecipeIngredient,
    RecipeReview,
    RecipeStep,
    RecipeStepImage,
    StepImage,
    UserFavorite,
    Users,
)
from app.services.files import save_base64_file

users_bp = Blueprint("users", __name__)


def _is_admin(user_token: str) -> bool:
    return (
        Users.select()
        .where((Users.user_token == user_token) & (Users.user_type == "admin"))
        .exists()
    )


def _delete_user_cascade(iduser):
    for recipe in Recipe.select().where(Recipe.id_user == iduser):
        for step in RecipeStep.select().where(RecipeStep.id_recipe == recipe.id):
            RecipeStepImage.delete().where(RecipeStepImage.id_step == step.id).execute()
        RecipeFilter.delete().where(RecipeFilter.id_recipe == recipe.id).execute()
        RecipeIngredient.delete().where(RecipeIngredient.id_recipe == recipe.id).execute()
        RecipeComment.delete().where(RecipeComment.id_recipe == recipe.id).execute()
        RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()
        RecipeReview.delete().where(RecipeReview.id_recipe == recipe.id).execute()
        UserFavorite.delete().where(UserFavorite.id_recipe == recipe.id).execute()

    StepImage.delete().where(StepImage.id_user == iduser).execute()
    UserFavorite.delete().where(UserFavorite.id_user == iduser).execute()
    Recipe.delete().where(Recipe.id_user == iduser).execute()
    Users.delete().where(Users.id == iduser).execute()


@users_bp.post("/viewProfile")
def view_profile():
    data = request.get_json() or {}
    users = Users.select(Users.user_name, Users.user_email, Users.user_image).where(
        Users.id == data.get("iduser")
    )
    return jsonify(
        message=[
            {"name": u.user_name, "email": u.user_email, "image": u.user_image}
            for u in users
        ]
    )


@users_bp.post("/changeImage")
def change_image():
    data = request.get_json() or {}
    image = data.get("image")
    if not image or not isinstance(image, dict) or not image.get("base64"):
        return jsonify(message="Image data not valid"), 400

    image_url = save_base64_file(
        image.get("base64"),
        image.get("name"),
        current_app.config["UPLOAD_FOLDER_IMAGES"],
    )
    if not image_url:
        return jsonify(message="Failed to save image"), 500

    Users.update(user_image=image_url, modified_at=date.today()).where(
        Users.id == data.get("iduser")
    ).execute()
    return jsonify(message="Image Changed", newImage=image_url)


@users_bp.post("/changeName")
def change_name():
    data = request.get_json() or {}
    if not Users.select().where(Users.user_token == data.get("userToken")).exists():
        return jsonify(message="ERROR"), 401
    Users.update(user_name=data.get("name"), modified_at=date.today()).where(
        Users.id == data.get("iduser")
    ).execute()
    return jsonify(message=data.get("name"))


@users_bp.post("/changeEmail")
def change_email():
    data = request.get_json() or {}
    if not Users.select().where(Users.user_token == data.get("userToken")).exists():
        return jsonify(message="ERROR"), 401
    email = data.get("email")
    iduser = data.get("iduser")
    Users.update(user_email=email, modified_at=date.today()).where(
        Users.id == iduser
    ).execute()
    token = create_access_token(identity=email)
    Users.update(user_token=token, modified_at=date.today()).where(
        Users.id == iduser
    ).execute()
    return jsonify(message=email, userToken=token)


@users_bp.post("/changePassword")
def change_password():
    data = request.get_json() or {}
    if not Users.select().where(Users.user_token == data.get("userToken")).exists():
        return jsonify(message="ERROR"), 401
    new_password = data.get("newPassword") or ""
    Users.update(
        user_password=hashlib.sha256(new_password.encode("utf-8")).hexdigest(),
        modified_at=date.today(),
    ).where(Users.id == data.get("iduser")).execute()
    return jsonify(message="Contraseña Actualizada")


@users_bp.post("/deleteProfile")
def delete_profile():
    data = request.get_json() or {}
    _delete_user_cascade(data.get("iduser"))
    return jsonify(message="Perfil eliminado")


@users_bp.post("/allUsers")
def all_users():
    data = request.get_json() or {}
    if not _is_admin(data.get("userToken")):
        return jsonify(users_list=[])
    users = Users.select().where(Users.user_type != data.get("type"))
    return jsonify(
        users_list=[
            {"iduser": u.id, "name": u.user_name, "email": u.user_email} for u in users
        ]
    )


@users_bp.post("/deleteUser")
def delete_user():
    data = request.get_json() or {}
    if not _is_admin(data.get("userToken")):
        return jsonify(message="ERROR"), 403
    _delete_user_cascade(data.get("iduser"))
    return jsonify(message="Perfil eliminado")
