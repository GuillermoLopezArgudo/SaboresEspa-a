from datetime import date

from flask import Blueprint, current_app, jsonify, request
from peewee import fn

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

recipes_bp = Blueprint("recipes", __name__)


def _save_filters(recipe_id, typeeat=None, ccaa=None, time=None, proteins=None):
    proteins = proteins or []
    if typeeat:
        RecipeFilter.create(
            id_recipe=recipe_id,
            type=typeeat,
            category="typeeat",
            created_at=date.today(),
            modified_at=date.today(),
        )
    if ccaa:
        RecipeFilter.create(
            id_recipe=recipe_id,
            type=ccaa,
            category="ccaa",
            created_at=date.today(),
            modified_at=date.today(),
        )
    if time:
        RecipeFilter.create(
            id_recipe=recipe_id,
            type=time,
            category="time",
            created_at=date.today(),
            modified_at=date.today(),
        )
    for protein in proteins:
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


@recipes_bp.post("/create")
def create_recipe():
    data = request.get_json() or {}
    title = data.get("title")
    image = data.get("image")
    video = data.get("video")
    description = data.get("description")
    ingredients = data.get("ingredients") or []
    quantities = data.get("quantities") or []
    steps = data.get("steps") or []
    token = data.get("token")
    proteins = data.get("proteins") or []
    typeeat = data.get("typeeat")
    ccaa = data.get("ccaa")
    time = data.get("time")
    visibility = data.get("visibility")

    user = Users.get_or_none(Users.user_token == token)
    if not user:
        return jsonify(message="Usuario no autenticado"), 401

    image_url = None
    if image and isinstance(image, dict):
        image_url = save_base64_file(
            image.get("base64"),
            image.get("name"),
            current_app.config["UPLOAD_FOLDER_IMAGES"],
        )
    video_url = None
    if video and isinstance(video, dict):
        video_url = save_base64_file(
            video.get("base64"),
            video.get("name"),
            current_app.config["UPLOAD_FOLDER_VIDEOS"],
        )

    recipe = Recipe.create(
        recipe_title=title,
        recipe_visibility=bool(visibility),
        recipe_image=image_url,
        recipe_description=description,
        recipe_video=video_url,
        id_user=user.id,
        created_at=date.today(),
        modified_at=date.today(),
    )

    for i, ingredient in enumerate(ingredients):
        RecipeIngredient.create(
            id_recipe=recipe.id,
            id_user=user.id,
            ingredients_text=ingredient,
            quantity_unit=quantities[i] if i < len(quantities) else "",
            created_at=date.today(),
            modified_at=date.today(),
        )

    for step in steps:
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict):
            step_image_url = save_base64_file(
                step_image.get("base64"),
                step_image.get("name"),
                current_app.config["UPLOAD_FOLDER_IMAGES"],
            )
        recipe_step = RecipeStep.create(
            id_recipe=recipe.id,
            id_user=user.id,
            step_title=step.get("title"),
            step_description=step.get("text"),
            created_at=date.today(),
            modified_at=date.today(),
        )
        if step_image_url:
            step_img = StepImage.create(
                id_user=user.id,
                step_image=step_image_url,
                created_at=date.today(),
                modified_at=date.today(),
            )
            RecipeStepImage.create(id_step=recipe_step.id, id_image=step_img.id)

    _save_filters(recipe.id, typeeat, ccaa, time, proteins)
    return jsonify(message="RECETA SUBIDA")


@recipes_bp.post("/viewRecipes")
def view_personal_recipes():
    data = request.get_json() or {}
    user_id = data.get("id")
    recipes = list(Recipe.select().join(Users).where(Users.id == user_id))
    recipes_list = [
        {
            "id": r.id,
            "title": r.recipe_title,
            "image": r.recipe_image,
            "description": r.recipe_description,
            "video": r.recipe_video,
        }
        for r in recipes
    ]
    return jsonify(message=recipes_list, categories_list=_categories_for_recipes(recipes))


@recipes_bp.post("/viewAll")
def view_all_recipes():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    recipes = list(Recipe.select().where(Recipe.recipe_visibility == True))  # noqa: E712
    recipes_list = [
        {
            "id": r.id,
            "title": r.recipe_title,
            "image": r.recipe_image,
            "description": r.recipe_description,
            "video": r.recipe_video,
        }
        for r in recipes
    ]
    payload = {
        "recipes_list": recipes_list,
        "categories_list": _categories_for_recipes(recipes),
    }
    if iduser:
        payload["favorites_list"] = [
            {"id_recipe": f.id_recipe_id}
            for f in UserFavorite.select().where(UserFavorite.id_user == iduser)
        ]
        payload["reviews_list"] = [
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(RecipeReview.id_user == iduser)
        ]
    return jsonify(**payload)


@recipes_bp.post("/updateFavs")
def update_favs():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    if not idrecipe or not iduser:
        return jsonify(message="ERROR"), 400
    if not UserFavorite.select().where(
        (UserFavorite.id_recipe == idrecipe) & (UserFavorite.id_user == iduser)
    ).exists():
        UserFavorite.create(
            id_recipe=idrecipe,
            id_user=iduser,
            created_at=date.today(),
            modified_at=date.today(),
        )
    return jsonify(message="Favorite save")


@recipes_bp.post("/deleteFavs")
def delete_favs():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    query = UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe)
    if iduser:
        query = query.where(UserFavorite.id_user == iduser)
    query.execute()
    return jsonify(message="Favorite delete")


@recipes_bp.post("/updateRating")
def update_rating():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    rating = data.get("rating")
    existing = RecipeReview.get_or_none(
        (RecipeReview.id_recipe == idrecipe) & (RecipeReview.id_user == iduser)
    )
    if existing:
        RecipeReview.update(recipe_review_item_value=rating).where(
            RecipeReview.id == existing.id
        ).execute()
        return jsonify(message="Review update")
    RecipeReview.create(
        id_recipe=idrecipe,
        id_user=iduser,
        recipe_review_item_value=rating,
        created_at=date.today(),
        modified_at=date.today(),
    )
    return jsonify(message="Review save")


@recipes_bp.post("/viewRecipe")
def view_recipe():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    recipes = list(Recipe.select().where(Recipe.id == idrecipe))
    recipe_list = [
        {
            "title": r.recipe_title,
            "description": r.recipe_description,
            "visibility": bool(r.recipe_visibility),
            "video": r.recipe_video,
            "id_user": r.id_user_id,
            "image": r.recipe_image,
        }
        for r in recipes
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
    }
    if iduser:
        payload["favorites_list"] = [
            {"id_recipe": f.id_recipe_id}
            for f in UserFavorite.select().where(UserFavorite.id_user == iduser)
        ]
    return jsonify(**payload)


@recipes_bp.post("/viewComment")
def view_comment():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
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
def create_comment():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    comment = data.get("comment")
    user = Users.get_or_none(Users.id == iduser)
    if not user:
        return jsonify(message="Usuario no encontrado"), 404
    RecipeComment.create(
        comment_text=comment,
        id_recipe=idrecipe,
        id_user=iduser,
        created_at=date.today(),
        modified_at=date.today(),
    )
    return jsonify(message="Comment Update", username=user.user_name)


@recipes_bp.post("/deleteRecipe")
def delete_recipe():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    if not idrecipe:
        return jsonify(message="ERROR"), 400

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
    return jsonify(message="Recipe deleted")


@recipes_bp.post("/deleteComment")
def delete_comment():
    data = request.get_json() or {}
    RecipeComment.delete().where(RecipeComment.id == data.get("idcomment")).execute()
    return jsonify(message="Comment deleted")


@recipes_bp.post("/editeComment")
def edit_comment():
    data = request.get_json() or {}
    RecipeComment.update(
        comment_text=data.get("comment"), modified_at=date.today()
    ).where(RecipeComment.id == data.get("idcomment")).execute()
    return jsonify(message="Change Comment")


@recipes_bp.post("/viewFavs")
def view_favs():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    favorites_list_ids = [
        f.id_recipe_id
        for f in UserFavorite.select(UserFavorite.id_recipe).where(
            UserFavorite.id_user == iduser
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
        favorites_list=[
            {
                "id": r.id,
                "title": r.recipe_title,
                "image": r.recipe_image,
                "description": r.recipe_description,
            }
            for r in recipes
        ],
        reviews_list=[
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(
                (RecipeReview.id_user == iduser)
                & (RecipeReview.id_recipe.in_(favorites_list_ids))
            )
        ],
        categories_list=_categories_for_recipes(recipes),
    )


@recipes_bp.post("/editeRecipe")
def edit_recipe():
    data = request.get_json() or {}
    recipe_id = data.get("idrecipe")
    token = data.get("token")
    user = Users.get_or_none(Users.user_token == token)
    if not user:
        return jsonify(message="Usuario no autenticado"), 401

    recipe = Recipe.get_or_none((Recipe.id == recipe_id) & (Recipe.id_user == user.id))
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404

    image = data.get("image")
    video = data.get("video")
    image_url = None
    if image and isinstance(image, dict):
        if image.get("base64"):
            image_url = save_base64_file(
                image["base64"],
                image.get("name"),
                current_app.config["UPLOAD_FOLDER_IMAGES"],
            )
        else:
            image_url = image.get("name")
    video_url = None
    if video and isinstance(video, dict):
        if video.get("base64"):
            video_url = save_base64_file(
                video["base64"],
                video.get("name"),
                current_app.config["UPLOAD_FOLDER_VIDEOS"],
            )
        else:
            video_url = video.get("name")

    recipe.recipe_title = data.get("title")
    recipe.recipe_description = data.get("description")
    recipe.recipe_visibility = bool(data.get("visibility"))
    if image_url:
        recipe.recipe_image = image_url
    if video_url:
        recipe.recipe_video = video_url
    recipe.modified_at = date.today()
    recipe.save()

    step_ids = [
        s.id for s in RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id)
    ]
    if step_ids:
        image_ids = [
            link.id_image_id
            for link in RecipeStepImage.select().where(RecipeStepImage.id_step.in_(step_ids))
        ]
        RecipeStepImage.delete().where(RecipeStepImage.id_step.in_(step_ids)).execute()
        if image_ids:
            StepImage.delete().where(StepImage.id.in_(image_ids)).execute()

    RecipeFilter.delete().where(RecipeFilter.id_recipe == recipe.id).execute()
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe == recipe.id).execute()
    RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()

    ingredients = data.get("ingredients") or []
    quantities = data.get("quantities") or []
    for i, ingredient in enumerate(ingredients):
        RecipeIngredient.create(
            id_recipe=recipe.id,
            id_user=user.id,
            ingredients_text=ingredient,
            quantity_unit=quantities[i] if i < len(quantities) else "",
            created_at=date.today(),
            modified_at=date.today(),
        )

    for step in data.get("steps") or []:
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict):
            if step_image.get("base64"):
                step_image_url = save_base64_file(
                    step_image["base64"],
                    step_image.get("name"),
                    current_app.config["UPLOAD_FOLDER_IMAGES"],
                )
            else:
                step_image_url = step_image.get("name")
        recipe_step = RecipeStep.create(
            id_recipe=recipe.id,
            id_user=user.id,
            step_title=step.get("title"),
            step_description=step.get("description"),
            created_at=date.today(),
            modified_at=date.today(),
        )
        if step_image_url:
            step_img = StepImage.create(
                id_user=user.id,
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
    data = request.get_json() or {}
    clause = None
    for value in [
        data.get("typeeat"),
        data.get("ccaa"),
        data.get("time"),
        *(data.get("proteins") or []),
    ]:
        if not value:
            continue
        part = RecipeFilter.type == value
        clause = part if clause is None else (clause | part)
    if clause is None:
        return jsonify(message=[])
    return jsonify(
        message=[
            {"idrecipe": f.id_recipe_id} for f in RecipeFilter.select().where(clause)
        ]
    )


@recipes_bp.post("/recipeFilter")
def recipe_filter():
    data = request.get_json() or {}
    filtered = data.get("filtered") or []
    iduser = data.get("iduser")
    idrecipes = [item["idrecipe"] for item in filtered if "idrecipe" in item]
    if not idrecipes:
        return jsonify(filtered_recipes=[])
    filtereds = list(
        Recipe.select().where(
            (Recipe.id.in_(idrecipes)) & (Recipe.recipe_visibility == True)  # noqa: E712
        )
    )
    payload = {
        "filtered_recipes": [
            {
                "id": r.id,
                "title": r.recipe_title,
                "image": r.recipe_image,
                "description": r.recipe_description,
                "video": r.recipe_video,
            }
            for r in filtereds
        ]
    }
    if iduser:
        payload["favorites_list"] = [
            {"id_recipe": f.id_recipe_id}
            for f in UserFavorite.select().where(UserFavorite.id_user == iduser)
        ]
        payload["reviews_list"] = [
            {"id_recipe": r.id_recipe_id, "review": r.recipe_review_item_value}
            for r in RecipeReview.select().where(RecipeReview.id_user == iduser)
        ]
    return jsonify(**payload)


@recipes_bp.post("/averageStars")
def average_stars():
    try:
        query = RecipeReview.select(
            RecipeReview.id_recipe,
            fn.AVG(RecipeReview.recipe_review_item_value).alias("average_rating"),
        ).group_by(RecipeReview.id_recipe)
        return jsonify(
            media=[
                {
                    "recipe_id": item.id_recipe_id,
                    "average_rating": round(float(item.average_rating or 0), 2),
                }
                for item in query
            ]
        )
    except Exception as exc:
        return jsonify(message="Error: " + str(exc)), 500
