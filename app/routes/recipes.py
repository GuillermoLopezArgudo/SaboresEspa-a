import os
from datetime import date

from flask import Blueprint, current_app, jsonify, request
from peewee import IntegrityError, JOIN, fn

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

DEFAULT_PAGE_SIZE = 12
MAX_PAGE_SIZE = 48
from app.security import (
    MAX_COMMENT_LEN,
    MAX_QUANTITY_LEN,
    MAX_STEP_TITLE_LEN,
    login_required,
)
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
    if not recipes:
        return []
    recipe_ids = [recipe.id for recipe in recipes]
    return [
        {
            "recipe_id": categorie.id_recipe_id,
            "type": categorie.type,
            "category": categorie.category,
        }
        for categorie in RecipeFilter.select().where(RecipeFilter.id_recipe.in_(recipe_ids))
    ]


def _recipe_dict(r, author=""):
    return {
        "id": r.id,
        "title": r.recipe_title,
        "image": r.recipe_image,
        "description": r.recipe_description,
        "video": r.recipe_video,
        "id_user": r.id_user_id,
        "author": author or "",
    }


def _recipes_as_dicts(recipes):
    """Serializa recetas con nombre de autor en un solo query de usuarios."""
    user_ids = {r.id_user_id for r in recipes if r.id_user_id}
    names = {}
    if user_ids:
        names = {
            u.id: u.user_name
            for u in Users.select(Users.id, Users.user_name).where(
                Users.id.in_(list(user_ids))
            )
        }
    return [_recipe_dict(r, names.get(r.id_user_id, "")) for r in recipes]


def _can_manage_recipe(user, recipe) -> bool:
    return recipe.id_user_id == user.id or (user and user.user_type == "admin")


def _step_description(step: dict) -> str:
    """Acepta description (edit/view) o text (create legacy)."""
    if not isinstance(step, dict):
        return ""
    return (step.get("description") or step.get("text") or "").strip()


def _media_refs_equal(a, b) -> bool:
    if not a or not b:
        return False
    a, b = str(a).strip(), str(b).strip()
    if a == b:
        return True
    # Comparar por basename por si el front manda solo el nombre
    return os.path.basename(a) == os.path.basename(b) and bool(os.path.basename(a))


def _require_upload(file_dict, folder, kind, label, allowed_existing=None):
    """Sube media si viene base64; falla la petición si el cliente envió archivo inválido.

    Sin base64 solo se acepta name/URL si está en allowed_existing (anti-hijack de media ajena).
    """
    if not file_dict or not isinstance(file_dict, dict):
        return None
    if not file_dict.get("base64"):
        name = file_dict.get("name") or None
        if not name:
            return None
        if allowed_existing is None:
            # Create u contexto sin lista: ignorar name suelto (no es un upload real)
            return None
        for allowed in allowed_existing:
            if _media_refs_equal(name, allowed):
                return allowed  # canonical stored value
        return jsonify(message=f"Referencia de {label} no válida"), 400
    url = save_base64_file(
        file_dict.get("base64"),
        file_dict.get("name") or ("file.jpg" if kind == "image" else "file.mp4"),
        folder,
        kind=kind,
    )
    if not url:
        return jsonify(message=f"No se pudo guardar {label}"), 400
    return url


def _optional_user():
    try:
        from app.security import resolve_user_from_jwt

        return resolve_user_from_jwt(optional=True)
    except Exception:
        return None


def _parse_pagination(data):
    data = data or {}
    fetch_all = bool(data.get("all"))
    try:
        page = max(1, int(data.get("page") or 1))
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = int(data.get("page_size") or DEFAULT_PAGE_SIZE)
    except (TypeError, ValueError):
        page_size = DEFAULT_PAGE_SIZE
    page_size = min(max(1, page_size), MAX_PAGE_SIZE)
    q = (data.get("q") or data.get("search") or "").strip()
    sort = (data.get("sort") or "rating-desc").strip()
    if sort not in ("rating-desc", "title-asc", "author-asc"):
        sort = "rating-desc"
    return page, page_size, q, sort, fetch_all


def _pagination_meta(page, page_size, total):
    total_pages = max(1, (total + page_size - 1) // page_size) if total else 1
    page = min(page, total_pages) if total else 1
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next": bool(total) and page < total_pages,
        "has_prev": page > 1,
    }


def _avg_reviews_alias():
    return (
        RecipeReview.select(
            RecipeReview.id_recipe.alias("recipe_id"),
            fn.AVG(RecipeReview.recipe_review_item_value).alias("avg_rating"),
        )
        .group_by(RecipeReview.id_recipe)
        .alias("recipe_avg")
    )


def _apply_search_sort(query, q, sort, *, joined_users=False):
    """Aplica búsqueda y orden. Asume Recipe en el SELECT; une Users si hace falta."""
    if not joined_users:
        query = query.join(Users, on=(Recipe.id_user == Users.id))

    if q:
        like = f"%{q}%"
        query = query.where(
            Recipe.recipe_title.ilike(like)
            | Recipe.recipe_description.ilike(like)
            | Users.user_name.ilike(like)
        )

    avg = _avg_reviews_alias()
    query = query.switch(Recipe).join(
        avg, JOIN.LEFT_OUTER, on=(Recipe.id == avg.c.recipe_id)
    )

    if sort == "title-asc":
        query = query.order_by(fn.Lower(Recipe.recipe_title).asc(), Recipe.id.desc())
    elif sort == "author-asc":
        query = query.order_by(fn.Lower(Users.user_name).asc(), Recipe.id.desc())
    else:
        query = query.order_by(
            fn.COALESCE(avg.c.avg_rating, -1).desc(),
            Recipe.id.desc(),
        )
    return query


def _paginate_recipes(query, page, page_size, fetch_all=False):
    total = query.count()
    if fetch_all:
        recipes = list(query)
        meta = {
            "page": 1,
            "page_size": total or page_size,
            "total": total,
            "total_pages": 1,
            "has_next": False,
            "has_prev": False,
        }
        return recipes, meta
    meta = _pagination_meta(page, page_size, total)
    recipes = list(query.paginate(meta["page"], page_size))
    return recipes, meta


def _viewer_favs_reviews(viewer, recipe_ids=None):
    """Favoritos y valoraciones del usuario (todos, para marcar corazones en UI)."""
    favorites_list = []
    reviews_list = []
    if not viewer:
        return favorites_list, reviews_list
    favorites_list = [
        {"id_recipe": f.id_recipe_id}
        for f in UserFavorite.select().where(UserFavorite.id_user == viewer.id)
    ]
    review_q = RecipeReview.select().where(RecipeReview.id_user == viewer.id)
    if recipe_ids is not None:
        if not recipe_ids:
            return favorites_list, []
        review_q = review_q.where(RecipeReview.id_recipe.in_(recipe_ids))
    reviews_list = [
        {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
        for r in review_q
    ]
    return favorites_list, reviews_list


def _can_view_recipe(user, recipe) -> bool:
    if recipe.recipe_visibility:
        return True
    if not user:
        return False
    return _can_manage_recipe(user, recipe)


def _delete_recipe_cascade(idrecipe):
    with db.atomic():
        RecipeFilter.delete().where(RecipeFilter.id_recipe == idrecipe).execute()
        RecipeIngredient.delete().where(RecipeIngredient.id_recipe == idrecipe).execute()
        RecipeComment.delete().where(RecipeComment.id_recipe == idrecipe).execute()
        UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe).execute()
        RecipeReview.delete().where(RecipeReview.id_recipe == idrecipe).execute()

        for step in RecipeStep.select().where(RecipeStep.id_recipe == idrecipe):
            links = list(
                RecipeStepImage.select().where(RecipeStepImage.id_step == step.id)
            )
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
    if len(title) > 255:
        return jsonify(message="Título demasiado largo (máx. 255)"), 400

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
        step_title = (step.get("title") or "").strip()
        if not step_title:
            return jsonify(message="Cada paso necesita título"), 400
        if len(step_title) > MAX_STEP_TITLE_LEN:
            return jsonify(message=f"Título de paso demasiado largo (máx. {MAX_STEP_TITLE_LEN})"), 400
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
        prepared_steps.append((step, step_title, step_image_url))

    for i, _ingredient in enumerate(ingredients):
        qty = quantities[i] if i < len(quantities) else ""
        if qty is not None and len(str(qty)) > MAX_QUANTITY_LEN:
            return jsonify(message=f"Cantidad demasiado larga (máx. {MAX_QUANTITY_LEN})"), 400

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
            qty = quantities[i] if i < len(quantities) else ""
            RecipeIngredient.create(
                id_recipe=recipe.id,
                id_user=current_user.id,
                ingredients_text=ingredient,
                quantity_unit=str(qty or "")[:MAX_QUANTITY_LEN],
                created_at=date.today(),
                modified_at=date.today(),
            )

        for step, step_title, step_image_url in prepared_steps:
            recipe_step = RecipeStep.create(
                id_recipe=recipe.id,
                id_user=current_user.id,
                step_title=step_title,
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
    data = request.get_json(silent=True) or {}
    page, page_size, q, sort, fetch_all = _parse_pagination(data)

    query = Recipe.select(Recipe).where(Recipe.id_user == current_user.id)
    query = _apply_search_sort(query, q, sort)
    recipes, pagination = _paginate_recipes(query, page, page_size, fetch_all)
    return jsonify(
        message=_recipes_as_dicts(recipes),
        categories_list=_categories_for_recipes(recipes),
        pagination=pagination,
    )


@recipes_bp.post("/viewAll")
def view_all_recipes():
    """Público: solo recetas visibles. Favoritos/reviews si hay JWT válido.

    Acepta page, page_size, q/search, sort (rating-desc|title-asc|author-asc).
    """
    data = request.get_json(silent=True) or {}
    page, page_size, q, sort, fetch_all = _parse_pagination(data)
    current_user = _optional_user()

    query = Recipe.select(Recipe).where(Recipe.recipe_visibility == True)  # noqa: E712
    query = _apply_search_sort(query, q, sort)
    recipes, pagination = _paginate_recipes(query, page, page_size, fetch_all)

    favorites_list, reviews_list = _viewer_favs_reviews(current_user)
    return jsonify(
        recipes_list=_recipes_as_dicts(recipes),
        categories_list=_categories_for_recipes(recipes),
        favorites_list=favorites_list,
        reviews_list=reviews_list,
        pagination=pagination,
    )


@recipes_bp.post("/updateFavs")
@login_required
def update_favs(current_user):
    data = request.get_json() or {}
    try:
        idrecipe = int(data.get("idrecipe"))
    except (TypeError, ValueError):
        return jsonify(message="Receta inválida"), 400
    recipe = Recipe.get_or_none(Recipe.id == idrecipe)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404
    if not _can_view_recipe(current_user, recipe):
        return jsonify(message="No autorizado"), 403
    if not UserFavorite.select().where(
        (UserFavorite.id_recipe == idrecipe) & (UserFavorite.id_user == current_user.id)
    ).exists():
        try:
            UserFavorite.create(
                id_recipe=idrecipe,
                id_user=current_user.id,
                created_at=date.today(),
                modified_at=date.today(),
            )
        except IntegrityError:
            pass  # carrera concurrente; índice único ya lo cubre
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

    recipe = Recipe.get_or_none(Recipe.id == idrecipe)
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404
    if not _can_view_recipe(current_user, recipe):
        return jsonify(message="No autorizado"), 403

    existing = RecipeReview.get_or_none(
        (RecipeReview.id_recipe == idrecipe) & (RecipeReview.id_user == current_user.id)
    )
    if existing:
        RecipeReview.update(recipe_review_item_value=rating).where(
            RecipeReview.id == existing.id
        ).execute()
        return jsonify(message="Review update")
    try:
        RecipeReview.create(
            id_recipe=idrecipe,
            id_user=current_user.id,
            recipe_review_item_value=rating,
            created_at=date.today(),
            modified_at=date.today(),
        )
    except IntegrityError:
        RecipeReview.update(recipe_review_item_value=rating).where(
            (RecipeReview.id_recipe == idrecipe)
            & (RecipeReview.id_user == current_user.id)
        ).execute()
        return jsonify(message="Review update")
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

    author = ""
    owner = Users.get_or_none(Users.id == recipe.id_user_id)
    if owner:
        author = owner.user_name or ""

    recipe_list = [
        {
            "title": recipe.recipe_title,
            "description": recipe.recipe_description,
            "visibility": bool(recipe.recipe_visibility),
            "video": recipe.recipe_video,
            "id_user": recipe.id_user_id,
            "image": recipe.recipe_image,
            "author": author,
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
    data = request.get_json(silent=True) or {}
    page, page_size, q, sort, fetch_all = _parse_pagination(data)

    favorites_list_ids = [
        f.id_recipe_id
        for f in UserFavorite.select(UserFavorite.id_recipe).where(
            UserFavorite.id_user == current_user.id
        )
    ]
    if not favorites_list_ids:
        return jsonify(
            favorites_list=[],
            reviews_list=[],
            categories_list=[],
            pagination=_pagination_meta(1, page_size, 0),
        )

    # Visibles para el usuario (públicas o suyas/privadas)
    query = Recipe.select(Recipe).where(
        (Recipe.id.in_(favorites_list_ids))
        & (
            (Recipe.recipe_visibility == True)  # noqa: E712
            | (Recipe.id_user == current_user.id)
        )
    )
    query = _apply_search_sort(query, q, sort)
    recipes, pagination = _paginate_recipes(query, page, page_size, fetch_all)
    visible_ids = [r.id for r in recipes]
    return jsonify(
        favorites_list=_recipes_as_dicts(recipes),
        reviews_list=[
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(
                (RecipeReview.id_user == current_user.id)
                & (RecipeReview.id_recipe.in_(visible_ids or [0]))
            )
        ],
        categories_list=_categories_for_recipes(recipes),
        pagination=pagination,
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

    new_title = None
    if "title" in data:
        new_title = (data.get("title") or "").strip()
        if not new_title:
            return jsonify(message="Título obligatorio"), 400
        if len(new_title) > 255:
            return jsonify(message="Título demasiado largo (máx. 255)"), 400

    # Media ya asociada a esta receta (única permitida sin nuevo base64)
    existing_images = set()
    if recipe.recipe_image:
        existing_images.add(recipe.recipe_image)
    for step in RecipeStep.select().where(RecipeStep.id_recipe == recipe.id):
        for link in RecipeStepImage.select().where(RecipeStepImage.id_step == step.id):
            img = StepImage.get_or_none(StepImage.id == link.id_image_id)
            if img and img.step_image:
                existing_images.add(img.step_image)
    existing_videos = {recipe.recipe_video} if recipe.recipe_video else set()

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
            allowed_existing=existing_images,
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
            allowed_existing=existing_videos,
        )
        if isinstance(uploaded, tuple):
            return uploaded
        video_url = uploaded

    ingredients = data.get("ingredients") or []
    quantities = data.get("quantities") or []
    prepared_steps = []
    for step in data.get("steps") or []:
        step_title = (step.get("title") or "").strip()
        if not step_title:
            return jsonify(message="Cada paso necesita título"), 400
        if len(step_title) > MAX_STEP_TITLE_LEN:
            return jsonify(message=f"Título de paso demasiado largo (máx. {MAX_STEP_TITLE_LEN})"), 400
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict):
            uploaded = _require_upload(
                step_image,
                current_app.config["UPLOAD_FOLDER_IMAGES"],
                "image",
                "una imagen de paso",
                allowed_existing=existing_images,
            )
            if isinstance(uploaded, tuple):
                return uploaded
            step_image_url = uploaded
        prepared_steps.append((step, step_title, step_image_url))

    for i, _ingredient in enumerate(ingredients):
        qty = quantities[i] if i < len(quantities) else ""
        if qty is not None and len(str(qty)) > MAX_QUANTITY_LEN:
            return jsonify(message=f"Cantidad demasiado larga (máx. {MAX_QUANTITY_LEN})"), 400

    with db.atomic():
        if new_title is not None:
            recipe.recipe_title = new_title
        if "description" in data:
            recipe.recipe_description = data.get("description")
        if "visibility" in data:
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

        # Siempre el dueño de la receta (no el admin editor) → evita FKs cruzadas al borrar usuarios
        owner_id = recipe.id_user_id

        for i, ingredient in enumerate(ingredients):
            qty = quantities[i] if i < len(quantities) else ""
            RecipeIngredient.create(
                id_recipe=recipe.id,
                id_user=owner_id,
                ingredients_text=ingredient,
                quantity_unit=str(qty or "")[:MAX_QUANTITY_LEN],
                created_at=date.today(),
                modified_at=date.today(),
            )

        for step, step_title, step_image_url in prepared_steps:
            recipe_step = RecipeStep.create(
                id_recipe=recipe.id,
                id_user=owner_id,
                step_title=step_title,
                step_description=_step_description(step),
                created_at=date.today(),
                modified_at=date.today(),
            )
            if step_image_url:
                step_img = StepImage.create(
                    id_user=owner_id,
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


def _filter_conditions_from_payload(data):
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
    return conditions


def _recipe_ids_matching_filters(conditions):
    """AND entre condiciones: intersección progresiva solo de IDs."""
    if not conditions:
        return []

    matched = None
    for category, value in conditions:
        ids = {
            row.id_recipe_id
            for row in RecipeFilter.select(RecipeFilter.id_recipe).where(
                (RecipeFilter.category == category) & (RecipeFilter.type == value)
            )
        }
        matched = ids if matched is None else (matched & ids)
        if not matched:
            return []
    return list(matched)


@recipes_bp.post("/filterRecipe")
def filter_recipe():
    """Devuelve ids (y opcionalmente recetas) que cumplen TODAS las categorías (AND).

    Acepta page, page_size, q/search, sort como viewAll.
    """
    data = request.get_json() or {}
    page, page_size, q, sort, fetch_all = _parse_pagination(data)
    conditions = _filter_conditions_from_payload(data)
    empty_meta = _pagination_meta(1, page_size, 0)
    if not conditions:
        return jsonify(
            message=[],
            filtered_recipes=[],
            categories_list=[],
            favorites_list=[],
            reviews_list=[],
            pagination=empty_meta,
        )

    matched_ids = _recipe_ids_matching_filters(conditions)
    if not matched_ids:
        return jsonify(
            message=[],
            filtered_recipes=[],
            categories_list=[],
            favorites_list=[],
            reviews_list=[],
            pagination=empty_meta,
        )

    query = Recipe.select(Recipe).where(
        (Recipe.id.in_(matched_ids)) & (Recipe.recipe_visibility == True)  # noqa: E712
    )
    query = _apply_search_sort(query, q, sort)
    recipes, pagination = _paginate_recipes(query, page, page_size, fetch_all)
    message = [{"idrecipe": r.id} for r in recipes]
    viewer = _optional_user()
    favorites_list, reviews_list = _viewer_favs_reviews(viewer)
    return jsonify(
        message=message,
        filtered_recipes=_recipes_as_dicts(recipes),
        categories_list=_categories_for_recipes(recipes),
        favorites_list=favorites_list,
        reviews_list=reviews_list,
        pagination=pagination,
    )


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
        "filtered_recipes": _recipes_as_dicts(filtereds),
        "categories_list": _categories_for_recipes(filtereds),
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
