from datetime import date

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token

from app.db import db
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
from app.config import Config
from app.rate_limit import rate_limit
from app.security import admin_required, hash_password, is_valid_email, login_required
from app.services.files import save_base64_file

users_bp = Blueprint("users", __name__)


def _reassign_child_to_recipe_owner(model, iduser):
    """Filas de este usuario en recetas ajenas → dueño de la receta (limpia FKs admin-edit)."""
    for row in list(model.select().where(model.id_user == iduser)):
        recipe = Recipe.get_or_none(Recipe.id == row.id_recipe_id)
        if recipe and recipe.id_user_id != iduser:
            model.update(id_user=recipe.id_user_id).where(model.id == row.id).execute()
        elif not recipe:
            row.delete_instance()


def _delete_user_cascade(iduser):
    from app.routes.recipes import _delete_recipe_cascade

    with db.atomic():
        # 1) Borrar recetas propias (cascade completo)
        owned_ids = [
            r.id for r in Recipe.select(Recipe.id).where(Recipe.id_user == iduser)
        ]
        for rid in owned_ids:
            _delete_recipe_cascade(rid)

        # 2) Reasignar restos en recetas ajenas (p.ej. admin editó y dejó id_user propio)
        _reassign_child_to_recipe_owner(RecipeIngredient, iduser)
        _reassign_child_to_recipe_owner(RecipeStep, iduser)
        for img in list(StepImage.select().where(StepImage.id_user == iduser)):
            # Vincular al dueño vía step → recipe si existe; si no, borrar
            link = RecipeStepImage.get_or_none(RecipeStepImage.id_image == img.id)
            if link:
                step = RecipeStep.get_or_none(RecipeStep.id == link.id_step_id)
                recipe = (
                    Recipe.get_or_none(Recipe.id == step.id_recipe_id) if step else None
                )
                if recipe and recipe.id_user_id != iduser:
                    StepImage.update(id_user=recipe.id_user_id).where(
                        StepImage.id == img.id
                    ).execute()
                    continue
            img.delete_instance()

        # 3) Datos sociales del usuario
        UserFavorite.delete().where(UserFavorite.id_user == iduser).execute()
        RecipeComment.delete().where(RecipeComment.id_user == iduser).execute()
        RecipeReview.delete().where(RecipeReview.id_user == iduser).execute()
        Users.delete().where(Users.id == iduser).execute()


@users_bp.post("/viewProfile")
@login_required
def view_profile(current_user):
    data = request.get_json(silent=True) or {}
    # Solo el propio perfil o admin
    target_id = data.get("iduser") or current_user.id
    try:
        target_id = int(target_id)
    except (TypeError, ValueError):
        return jsonify(message="Usuario inválido"), 400

    if target_id != current_user.id and current_user.user_type != "admin":
        return jsonify(message="No autorizado"), 403

    user = Users.get_or_none(Users.id == target_id)
    if not user:
        return jsonify(message="Usuario no encontrado"), 404
    return jsonify(
        message=[
            {"name": user.user_name, "email": user.user_email, "image": user.user_image}
        ]
    )


@users_bp.post("/changeImage")
@login_required
def change_image(current_user):
    data = request.get_json() or {}
    image = data.get("image")
    if not image or not isinstance(image, dict) or not image.get("base64"):
        return jsonify(message="Imagen no válida"), 400

    image_url = save_base64_file(
        image.get("base64"),
        image.get("name") or "avatar.jpg",
        current_app.config["UPLOAD_FOLDER_IMAGES"],
        kind="image",
    )
    if not image_url:
        return jsonify(message="No se pudo guardar la imagen"), 400

    Users.update(user_image=image_url, modified_at=date.today()).where(
        Users.id == current_user.id
    ).execute()
    return jsonify(message="Image Changed", newImage=image_url)


@users_bp.post("/changeName")
@login_required
def change_name(current_user):
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify(message="Nombre vacío"), 400
    Users.update(user_name=name, modified_at=date.today()).where(
        Users.id == current_user.id
    ).execute()
    return jsonify(message=name)


@users_bp.post("/changeEmail")
@login_required
def change_email(current_user):
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify(message="Email vacío"), 400
    if not is_valid_email(email):
        return jsonify(message="Email no válido"), 400
    if (
        Users.select()
        .where((Users.user_email == email) & (Users.id != current_user.id))
        .exists()
    ):
        return jsonify(message="Email en uso"), 409

    Users.update(user_email=email, modified_at=date.today()).where(
        Users.id == current_user.id
    ).execute()
    token = create_access_token(identity=str(current_user.id))
    Users.update(user_token=token, modified_at=date.today()).where(
        Users.id == current_user.id
    ).execute()
    return jsonify(message=email, userToken=token)


@users_bp.post("/changePassword")
@login_required
@rate_limit(Config.AUTH_RATE_LIMIT, Config.AUTH_RATE_WINDOW, prefix="change_password")
def change_password(current_user):
    data = request.get_json() or {}
    current_password = data.get("currentPassword") or data.get("oldPassword") or ""
    new_password = data.get("newPassword") or ""
    if len(new_password) < 8:
        return jsonify(message="La contraseña debe tener al menos 8 caracteres"), 400

    # Exigir contraseña actual si se envía; si no, rechazar por seguridad
    from app.security import verify_password

    if not current_password or not verify_password(
        current_password, current_user.user_password
    ):
        # Compat: si el front aún no manda currentPassword, exigir newPassword fuerte
        # pero NO permitir cambio sin demostrar posesión del token JWT (ya lo tenemos)
        # Mejor: exigir currentPassword siempre
        if not current_password:
            return jsonify(message="Debes indicar la contraseña actual"), 400
        # 400 (no 401): el interceptor del front no debe cerrar sesión por typo
        return jsonify(message="Contraseña actual incorrecta"), 400

    token = create_access_token(identity=str(current_user.id))
    Users.update(
        user_password=hash_password(new_password),
        user_token=token,
        modified_at=date.today(),
    ).where(Users.id == current_user.id).execute()
    return jsonify(message="Contraseña Actualizada", userToken=token)


@users_bp.post("/deleteProfile")
@login_required
def delete_profile(current_user):
    _delete_user_cascade(current_user.id)
    return jsonify(message="Perfil eliminado")


@users_bp.post("/allUsers")
@admin_required
def all_users(current_user):
    users = Users.select().where(Users.id != current_user.id)
    return jsonify(
        users_list=[
            {"iduser": u.id, "name": u.user_name, "email": u.user_email} for u in users
        ]
    )


@users_bp.post("/deleteUser")
@admin_required
def delete_user(current_user):
    data = request.get_json() or {}
    try:
        target_id = int(data.get("iduser"))
    except (TypeError, ValueError):
        return jsonify(message="Usuario inválido"), 400
    if target_id == current_user.id:
        return jsonify(message="No puedes borrarte desde admin así"), 400
    if not Users.get_or_none(Users.id == target_id):
        return jsonify(message="Usuario no encontrado"), 404
    _delete_user_cascade(target_id)
    return jsonify(message="Perfil eliminado")
