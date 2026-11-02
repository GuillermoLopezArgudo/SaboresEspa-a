from datetime import date

from flask import Blueprint, current_app, jsonify, request
from peewee import fn

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
from app.security import MAX_COMMENT_LEN, login_required
from app.services.files import save_base64_file

recipes_bp = Blueprint("recipes", __name__)


def _save_filters(recipe_id, typeeat=None, ccaa=None, time=None, proteins=None):
    proteins = proteins or []
    mapping = [
        (typeeat, "typeeat"),
        (ccaa, "ccaa"),
        (time, "time"),
    ]
    for value, category in mapping:
        if value:
            RecipeFilter.create(
                id_recipe=recipe_id,
                type=value,
                category=category,
                created_at=date.today(),
                modified_at=date.today(),
            )
    for protein in proteins:
        if protein:
            RecipeFilter.create(
                id_recipe=recipe_id,
                type=protein,
                category="protein",
                created_at=date.today(),
                modified_at=date.today(),
            )


def _categories_for_recipes(recipes):
    categories_list = []
    for recipe in recipes:
        for categorie in RecipeFilter.select().where(RecipeFilter.id_recipe == recipe.id):
            categories_list.append(
                {
                    "recipe_id": recipe.id,
                    "type": categorie.type,
                    "category": categorie.category,
                }
            )
    return categories_list


def _recipe_dict(r):
    return {
        "id": r.id,
        "title": r.recipe_title,
        "image": r.recipe_image,
        "description": r.recipe_description,
        "video": r.recipe_video,
    }


def _can_manage_recipe(user, recipe) -> bool:
    return recipe.id_user_id == user.id or (user and user.user_type == "admin")


def _step_description(step: dict) -> str:
    """Acepta description (edit/view) o text (create legacy)."""
    if not isinstance(step, dict):
        return ""
    return (step.get("description") or step.get("text") or "").strip()


def _require_upload(file_dict, folder, kind, label):
    """Sube media si viene base64; falla la petición si el cliente envió archivo inválido."""
    if not file_dict or not isinstance(file_dict, dict):
        return None
    if not file_dict.get("base64"):
        # Solo nombre/URL previa (edición sin cambiar fichero)
        return file_dict.get("name") or None
    url = save_base64_file(
        file_dict.get("base64"),
        file_dict.get("name") or ("file.jpg" if kind == "image" else "file.mp4"),
        folder,
        kind=kind,
    )
    if not url:
        from flask import jsonify

        return jsonify(message=f"No se pudo guardar {label}"), 400
    return url


def _optional_user():
    try:
        from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

        from app.security import _bearer_token

        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity is None:
            return None
        user = Users.get_or_none(Users.id == int(identity))
        if not user or not user.user_token:
            return None
        token = _bearer_token()
        if token and user.user_token != token:
            return None
        return user
    except Exception:
        return None


def _can_view_recipe(user, recipe) -> bool:
    if recipe.recipe_visibility:
        return True
    if not user:
        return False
    return _can_manage_recipe(user, recipe)


def _delete_recipe_cascade(idrecipe):
    RecipeFilter.delete().where(RecipeFilter.id_recipe == idrecipe).execute()
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe == idrecipe).execute()
    RecipeComment.delete().where(RecipeComment.id_recipe == idrecipe).execute()
    UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe).execute()
    RecipeReview.delete().where(RecipeReview.id_recipe == idrecipe).execute()

    for step in RecipeStep.select().where(RecipeStep.id_recipe == idrecipe):
        links = list(RecipeStepImage.select().where(RecipeStepImage.id_step == step.id))
        image_ids = [link.id_image_id for link in links]
        RecipeStepImage.delete().where(RecipeStepImage.id_step == step.id).execute()
        if image_ids:
            StepImage.delete().where(StepImage.id.in_(image_ids)).execute()

    RecipeStep.delete().where(RecipeStep.id_recipe == idrecipe).execute()
    Recipe.delete().where(Recipe.id == idrecipe).execute()


@recipes_bp.post("/create")
@login_required
def create_recipe(current_user):
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(message="Título obligatorio"), 400

    # Subir TODA la media antes de tocar la BD (evita recetas huérfanas)
    image = data.get("image")
    video = data.get("video")
    image_url = None
    video_url = None
    if image and isinstance(image, dict) and image.get("base64"):
        image_url = _require_upload(
            image,
            current_app.config["UPLOAD_FOLDER_IMAGES"],
            "image",
            "la imagen de la receta",
        )
        if isinstance(image_url, tuple):
            return image_url
    if video and isinstance(video, dict) and video.get("base64"):
        video_url = _require_upload(
            video,
            current_app.config["UPLOAD_FOLDER_VIDEOS"],
            "video",
            "el vídeo de la receta",
        )
        if isinstance(video_url, tuple):
            return video_url

    ingredients = data.get("ingredients") or []
    quantities = data.get("quantities") or []
    steps = data.get("steps") or []
    prepared_steps = []
    for step in steps:
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict) and step_image.get("base64"):
            step_image_url = _require_upload(
                step_image,
                current_app.config["UPLOAD_FOLDER_IMAGES"],
                "image",
                "una imagen de paso",
            )
            if isinstance(step_image_url, tuple):
                return step_image_url
        prepared_steps.append((step, step_image_url))

    with db.atomic():
        recipe = Recipe.create(
            recipe_title=title,
            recipe_visibility=bool(data.get("visibility", True)),
            recipe_image=image_url,
            recipe_description=data.get("description"),
            recipe_video=video_url,
            id_user=current_user.id,
            created_at=date.today(),
            modified_at=date.today(),
        )

        for i, ingredient in enumerate(ingredients):
            RecipeIngredient.create(
                id_recipe=recipe.id,
                id_user=current_user.id,
                ingredients_text=ingredient,
                quantity_unit=quantities[i] if i < len(quantities) else "",
                created_at=date.today(),
                modified_at=date.today(),
            )

        for step, step_image_url in prepared_steps:
            recipe_step = RecipeStep.create(
                id_recipe=recipe.id,
                id_user=current_user.id,
                step_title=step.get("title"),
                step_description=_step_description(step),
                created_at=date.today(),
                modified_at=date.today(),
            )
            if step_image_url:
                step_img = StepImage.create(
                    id_user=current_user.id,
                    step_image=step_image_url,
                    created_at=date.today(),
                    modified_at=date.today(),
                )
                RecipeStepImage.create(id_step=recipe_step.id, id_image=step_img.id)

        _save_filters(
            recipe.id,
            data.get("typeeat"),
            data.get("ccaa"),
            data.get("time"),
            data.get("proteins") or [],
        )
    return jsonify(message="RECETA SUBIDA")

@recipes_bp.post("/viewRecipes")
@login_required
def view_personal_recipes(current_user):
    recipes = list(Recipe.select().where(Recipe.id_user == current_user.id))
    return jsonify(
        message=[_recipe_dict(r) for r in recipes],
        categories_list=_categories_for_recipes(recipes),
    )


@recipes_bp.post("/viewAll")
def view_all_recipes():
    """Público: solo recetas visibles. Favoritos/reviews si hay JWT válido."""
    current_user = _optional_user()

    recipes = list(Recipe.select().where(Recipe.recipe_visibility == True))  # noqa: E712
    payload = {
        "recipes_list": [_recipe_dict(r) for r in recipes],
        "categories_list": _categories_for_recipes(recipes),
        "favorites_list": [],
        "reviews_list": [],
    }
    if current_user:
        payload["favorites_list"] = [
            {"id_recipe": f.id_recipe_id}
            for f in UserFavorite.select().where(UserFavorite.id_user == current_user.id)
        ]
        payload["reviews_list"] = [
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(RecipeReview.id_user == current_user.id)
        ]
    return jsonify(**payload)


@recipes_bp.post("/updateFavs")
@login_required
def update_favs(current_user):
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400
    if not Recipe.get_or_none(Recipe.id == idrecipe):
        return jsonify(message="Receta no encontrada"), 404
    if not UserFavorite.select().where(
        (UserFavorite.id_recipe == idrecipe) & (UserFavorite.id_user == current_user.id)
    ).exists():
        UserFavorite.create(
            id_recipe=idrecipe,
            id_user=current_user.id,
            created_at=date.today(),
            modified_at=date.today(),
        )
    return jsonify(message="Favorite save")


@recipes_bp.post("/deleteFavs")
@login_required
def delete_favs(current_user):
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400
    UserFavorite.delete().where(
        (UserFavorite.id_recipe == idrecipe) & (UserFavorite.id_user == current_user.id)
    ).execute()
    return jsonify(message="Favorite delete")


@recipes_bp.post("/updateRating")
@login_required
def update_rating(current_user):
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
        rating = int(data.get("rating"))
    except (TypeError, ValueError):
        return jsonify(message="Datos inválidos"), 400
    if rating < 1 or rating > 5:
        return jsonify(message="Rating fuera de rango"), 400

    existing = RecipeReview.get_or_none(
        (RecipeReview.id_recipe == idrecipe) & (RecipeReview.id_user == current_user.id)
    )
    if existing:
        RecipeReview.update(recipe_review_item_value=rating).where(
            RecipeReview.id == existing.id
        ).execute()
        return jsonify(message="Review update")
    RecipeReview.create(
        id_recipe=idrecipe,
        id_user=current_user.id,
        recipe_review_item_value=rating,
        created_at=date.today(),
        modified_at=date.today(),
    )
    return jsonify(message="Review save")


@recipes_bp.post("/viewRecipe")
def view_recipe():
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400

    recipe = Recipe.get_or_none(Recipe.id == idrecipe)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404

    viewer = _optional_user()
    if not _can_view_recipe(viewer, recipe):
        return jsonify(message="No autorizado"), 403

    recipe_list = [
        {
            "title": recipe.recipe_title,
            "description": recipe.recipe_description,
            "visibility": bool(recipe.recipe_visibility),
            "video": recipe.recipe_video,
            "id_user": recipe.id_user_id,
            "image": recipe.recipe_image,
        }
    ]
    ingredient_list = [
        {"ingredients": i.ingredients_text, "quantity": i.quantity_unit}
        for i in RecipeIngredient.select().where(RecipeIngredient.id_recipe == idrecipe)
    ]
    step_list = []
    for step in RecipeStep.select().where(RecipeStep.id_recipe == idrecipe):
        step_image = (
            StepImage.select(StepImage.step_image)
            .join(RecipeStepImage)
            .where(RecipeStepImage.id_step == step.id)
            .first()
        )
        step_list.append(
            {
                "title": step.step_title,
                "description": step.step_description,
                "image": step_image.step_image if step_image else None,
            }
        )
    filters_list = [
        {"type": f.type, "category": f.category}
        for f in RecipeFilter.select().where(RecipeFilter.id_recipe == idrecipe)
    ]
    payload = {
        "recipe_list": recipe_list,
        "ingredient_list": ingredient_list,
        "step_list": step_list,
        "filters_list": filters_list,
        "favorites_list": [],
    }

    viewer = _optional_user()
    if viewer:
        payload["favorites_list"] = [
            {"id_recipe": f.id_recipe_id}
            for f in UserFavorite.select().where(UserFavorite.id_user == viewer.id)
        ]

    return jsonify(**payload)


@recipes_bp.post("/viewComment")
def view_comment():
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400
    recipe = Recipe.get_or_none(Recipe.id == idrecipe)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404
    if not _can_view_recipe(_optional_user(), recipe):
        return jsonify(message="No autorizado"), 403
    comment_list = []
    for comment in RecipeComment.select().where(RecipeComment.id_recipe == idrecipe):
        user = Users.get_or_none(Users.id == comment.id_user_id)
        comment_list.append(
            {
                "id": comment.id,
                "comment": comment.comment_text,
                "iduser": comment.id_user_id,
                "username": user.user_name if user else "",
            }
        )
    return jsonify(comment_list=comment_list)


@recipes_bp.post("/createComment")
@login_required
def create_comment(current_user):
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400
    comment = (data.get("comment") or "").strip()
    if not comment:
        return jsonify(message="Comentario vacío"), 400
    if len(comment) > MAX_COMMENT_LEN:
        return jsonify(message=f"Comentario demasiado largo (máx. {MAX_COMMENT_LEN})"), 400
    recipe = Recipe.get_or_none(Recipe.id == idrecipe)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404
    if not _can_view_recipe(current_user, recipe):
        return jsonify(message="No autorizado"), 403
    RecipeComment.create(
        comment_text=comment,
        id_recipe=idrecipe,
        id_user=current_user.id,
        created_at=date.today(),
        modified_at=date.today(),
    )
    return jsonify(message="Comment Update", username=current_user.user_name)


@recipes_bp.post("/deleteRecipe")
@login_required
def delete_recipe(current_user):
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400
    recipe = Recipe.get_or_none(Recipe.id == idrecipe)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404
    if not _can_manage_recipe(current_user, recipe):
        return jsonify(message="No autorizado"), 403
    _delete_recipe_cascade(idrecipe)
    return jsonify(message="Recipe deleted")


@recipes_bp.post("/deleteComment")
@login_required
def delete_comment(current_user):
    data = request.get_json() or {}
    try:
        idcomment = int(data.get("idcomment"))
    except (TypeError, ValueError):
        return jsonify(message="Comentario inválido"), 400
    comment = RecipeComment.get_or_none(RecipeComment.id == idcomment)
    if not comment:
        return jsonify(message="Comentario no encontrado"), 404
    if comment.id_user_id != current_user.id and current_user.user_type != "admin":
        return jsonify(message="No autorizado"), 403
    RecipeComment.delete().where(RecipeComment.id == idcomment).execute()
    return jsonify(message="Comment deleted")


@recipes_bp.post("/editComment")
@recipes_bp.post("/editeComment")  # alias legacy
@login_required
def edit_comment(current_user):
    data = request.get_json() or {}
    try:
        idcomment = int(data.get("idcomment"))
    except (TypeError, ValueError):
        return jsonify(message="Comentario inválido"), 400
    comment = RecipeComment.get_or_none(RecipeComment.id == idcomment)
    if not comment:
        return jsonify(message="Comentario no encontrado"), 404
    if comment.id_user_id != current_user.id and current_user.user_type != "admin":
        return jsonify(message="No autorizado"), 403
    text = (data.get("comment") or "").strip()
    if not text:
        return jsonify(message="Comentario vacío"), 400
    if len(text) > MAX_COMMENT_LEN:
        return jsonify(message=f"Comentario demasiado largo (máx. {MAX_COMMENT_LEN})"), 400
    RecipeComment.update(comment_text=text, modified_at=date.today()).where(
        RecipeComment.id == idcomment
    ).execute()
    return jsonify(message="Change Comment")


@recipes_bp.post("/viewFavs")
@login_required
def view_favs(current_user):
    favorites_list_ids = [
        f.id_recipe_id
        for f in UserFavorite.select(UserFavorite.id_recipe).where(
            UserFavorite.id_user == current_user.id
        )
    ]
    if not favorites_list_ids:
        return jsonify(favorites_list=[], reviews_list=[], categories_list=[])

    recipes = list(
        Recipe.select().where(
            (Recipe.id.in_(favorites_list_ids))
            & (Recipe.recipe_visibility == True)  # noqa: E712
        )
    )
    return jsonify(
        favorites_list=[_recipe_dict(r) for r in recipes],
        reviews_list=[
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(
                (RecipeReview.id_user == current_user.id)
                & (RecipeReview.id_recipe.in_(favorites_list_ids))
            )
        ],
        categories_list=_categories_for_recipes(recipes),
    )


@recipes_bp.post("/editRecipe")
@recipes_bp.post("/editeRecipe")  # alias legacy
@login_required
def edit_recipe(current_user):
    data = request.get_json() or {}
    try:
        recipe_id = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400

    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404
    if not _can_manage_recipe(current_user, recipe):
        return jsonify(message="No autorizado"), 403

    # Subir media ANTES de borrar/recrear hijos (evita pérdida de datos a mitad)
    image = data.get("image")
    video = data.get("video")
    image_url = None
    video_url = None
    if image and isinstance(image, dict):
        uploaded = _require_upload(
            image,
            current_app.config["UPLOAD_FOLDER_IMAGES"],
            "image",
            "la imagen de la receta",
        )
        if isinstance(uploaded, tuple):
            return uploaded
        image_url = uploaded
    if video and isinstance(video, dict):
        uploaded = _require_upload(
            video,
            current_app.config["UPLOAD_FOLDER_VIDEOS"],
            "video",
            "el vídeo de la receta",
        )
        if isinstance(uploaded, tuple):
            return uploaded
        video_url = uploaded

    ingredients = data.get("ingredients") or []
    quantities = data.get("quantities") or []
    prepared_steps = []
    for step in data.get("steps") or []:
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict):
            uploaded = _require_upload(
                step_image,
                current_app.config["UPLOAD_FOLDER_IMAGES"],
                "image",
                "una imagen de paso",
            )
            if isinstance(uploaded, tuple):
                return uploaded
            step_image_url = uploaded
        prepared_steps.append((step, step_image_url))

    with db.atomic():
        recipe.recipe_title = (data.get("title") or recipe.recipe_title).strip()
        recipe.recipe_description = data.get("description")
        recipe.recipe_visibility = bool(data.get("visibility"))
        if image_url:
            recipe.recipe_image = image_url
        if video_url:
            recipe.recipe_video = video_url
        recipe.modified_at = date.today()
        recipe.save()

        step_ids = [
            s.id
            for s in RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id)
        ]
        if step_ids:
            image_ids = [
                link.id_image_id
                for link in RecipeStepImage.select().where(
                    RecipeStepImage.id_step.in_(step_ids)
                )
            ]
            RecipeStepImage.delete().where(RecipeStepImage.id_step.in_(step_ids)).execute()
            if image_ids:
                StepImage.delete().where(StepImage.id.in_(image_ids)).execute()

        RecipeFilter.delete().where(RecipeFilter.id_recipe == recipe.id).execute()
        RecipeIngredient.delete().where(RecipeIngredient.id_recipe == recipe.id).execute()
        RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()

        for i, ingredient in enumerate(ingredients):
            RecipeIngredient.create(
                id_recipe=recipe.id,
                id_user=current_user.id,
                ingredients_text=ingredient,
                quantity_unit=quantities[i] if i < len(quantities) else "",
                created_at=date.today(),
                modified_at=date.today(),
            )

        for step, step_image_url in prepared_steps:
            recipe_step = RecipeStep.create(
                id_recipe=recipe.id,
                id_user=current_user.id,
                step_title=step.get("title"),
                step_description=_step_description(step),
                created_at=date.today(),
                modified_at=date.today(),
            )
            if step_image_url:
                step_img = StepImage.create(
                    id_user=current_user.id,
                    step_image=step_image_url,
                    created_at=date.today(),
                    modified_at=date.today(),
                )
                RecipeStepImage.create(id_step=recipe_step.id, id_image=step_img.id)

        _save_filters(
            recipe.id,
            data.get("typeeat"),
            data.get("ccaa"),
            data.get("time"),
            data.get("proteins") or [],
        )
    return jsonify(message="Receta actualizada correctamente")


@recipes_bp.post("/filterRecipe")
def filter_recipe():
    """Devuelve ids que cumplen TODAS las categorías enviadas (AND entre categorías)."""
    data = request.get_json() or {}
    conditions = []
    if data.get("typeeat"):
        conditions.append(("typeeat", data["typeeat"]))
    if data.get("ccaa"):
        conditions.append(("ccaa", data["ccaa"]))
    if data.get("time"):
        conditions.append(("time", data["time"]))
    for protein in data.get("proteins") or []:
        if protein:
            conditions.append(("protein", protein))

    if not conditions:
        return jsonify(message=[])

    # Intersección de recipe ids
    id_sets = []
    for category, value in conditions:
        ids = {
            f.id_recipe_id
            for f in RecipeFilter.select().where(
                (RecipeFilter.category == category) & (RecipeFilter.type == value)
            )
        }
        id_sets.append(ids)

    result_ids = set.intersection(*id_sets) if id_sets else set()
    if not result_ids:
        return jsonify(message=[])

    # Solo IDs de recetas públicas (no filtrar privadas por categoría)
    visible = {
        r.id
        for r in Recipe.select(Recipe.id).where(
            (Recipe.id.in_(list(result_ids)))
            & (Recipe.recipe_visibility == True)  # noqa: E712
        )
    }
    return jsonify(message=[{"idrecipe": rid} for rid in visible])


@recipes_bp.post("/recipeFilter")
def recipe_filter():
    data = request.get_json() or {}
    filtered = data.get("filtered") or []
    idrecipes = [item["idrecipe"] for item in filtered if "idrecipe" in item]
    if not idrecipes:
        return jsonify(filtered_recipes=[])

    filtereds = list(
        Recipe.select().where(
            (Recipe.id.in_(idrecipes)) & (Recipe.recipe_visibility == True)  # noqa: E712
        )
    )
    payload = {
        "filtered_recipes": [_recipe_dict(r) for r in filtereds],
        "favorites_list": [],
        "reviews_list": [],
    }
    viewer = _optional_user()
    if viewer:
        payload["favorites_list"] = [
            {"id_recipe": f.id_recipe_id}
            for f in UserFavorite.select().where(UserFavorite.id_user == viewer.id)
        ]
        payload["reviews_list"] = [
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(RecipeReview.id_user == viewer.id)
        ]

    return jsonify(**payload)


@recipes_bp.post("/averageStars")
def average_stars():
    try:
        query = (
            RecipeReview.select(
                RecipeReview.id_recipe,
                fn.AVG(RecipeReview.recipe_review_item_value).alias("average_rating"),
            )
            .join(Recipe, on=(RecipeReview.id_recipe == Recipe.id))
            .where(Recipe.recipe_visibility == True)  # noqa: E712
            .group_by(RecipeReview.id_recipe)
        )
        return jsonify(
            media=[
                {
                    "recipe_id": item.id_recipe_id,
                    "average_rating": round(float(item.average_rating or 0), 2),
                }
                for item in query
            ]
        )
    except Exception:
        return jsonify(message="No se pudieron calcular las valoraciones"), 500
