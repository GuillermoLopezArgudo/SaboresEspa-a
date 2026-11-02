from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from peewee import fn
from datetime import date
import hashlib
import os
import base64

from models import (
    create_tables,
    Users,
    Recipe,
    RecipeComment,
    RecipeReview,
    UserFavorite,
    RecipeIngredient,
    StepImage,
    RecipeStep,
    RecipeStepImage,
    RecipeFilter,
)
from config import Config

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["UPLOAD_FOLDER_IMAGES"] = os.path.join("static", "images")
app.config["UPLOAD_FOLDER_VIDEOS"] = os.path.join("static", "videos")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

os.makedirs(app.config["UPLOAD_FOLDER_IMAGES"], exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER_VIDEOS"], exist_ok=True)

CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)
jwt = JWTManager(app)

try:
    create_tables()
except Exception as exc:
    # En arranque sin DB aún (build), no tumbar el proceso; Render/Neon reintentan al request.
    print(f"[warn] create_tables: {exc}")


def save_base64_file(base64_data, file_name, folder):
    if not base64_data or not file_name:
        return None
    try:
        if isinstance(base64_data, str) and base64_data.startswith("data:"):
            base64_data = base64_data.split(",", 1)[1]

        file_data = base64.b64decode(base64_data)
        safe_name = os.path.basename(file_name).replace("..", "_")
        file_path = os.path.join(folder, safe_name)
        os.makedirs(folder, exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(file_data)
        # Ruta relativa servida por Flask /static/...
        return file_path.replace("\\", "/")
    except Exception as e:
        print(f"Error al guardar archivo base64: {e}")
        return None


def _is_admin(user_token):
    return (
        Users.select()
        .where((Users.user_token == user_token) & (Users.user_type == "admin"))
        .exists()
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")


@app.route("/register", methods=["POST"])
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


@app.route("/login", methods=["POST"])
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


@app.route("/create", methods=["POST"])
def createRecipe():
    data = request.get_json() or {}
    title = data.get("title")
    image = data.get("image")
    image_url = None
    if image and isinstance(image, dict):
        image_url = save_base64_file(
            image.get("base64"), image.get("name"), app.config["UPLOAD_FOLDER_IMAGES"]
        )

    video = data.get("video")
    video_url = None
    if video and isinstance(video, dict):
        video_url = save_base64_file(
            video.get("base64"), video.get("name"), app.config["UPLOAD_FOLDER_VIDEOS"]
        )

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

    recipe = Recipe(
        recipe_title=title,
        recipe_visibility=bool(visibility),
        recipe_image=image_url,
        recipe_description=description,
        recipe_video=video_url,
        id_user=user.id,
        created_at=date.today(),
        modified_at=date.today(),
    )
    recipe.save()

    for i in range(len(ingredients)):
        quantity = quantities[i] if i < len(quantities) else ""
        RecipeIngredient.create(
            id_recipe=recipe.id,
            id_user=user.id,
            ingredients_text=ingredients[i],
            quantity_unit=quantity,
            created_at=date.today(),
            modified_at=date.today(),
        )

    for step in steps:
        step_title = step.get("title")
        step_text = step.get("text")
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict):
            step_image_url = save_base64_file(
                step_image.get("base64"),
                step_image.get("name"),
                app.config["UPLOAD_FOLDER_IMAGES"],
            )

        recipe_step = RecipeStep.create(
            id_recipe=recipe.id,
            id_user=user.id,
            step_title=step_title,
            step_description=step_text,
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

    if typeeat:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=typeeat,
            category="typeeat",
            created_at=date.today(),
            modified_at=date.today(),
        )
    if ccaa:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=ccaa,
            category="ccaa",
            created_at=date.today(),
            modified_at=date.today(),
        )
    if time:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=time,
            category="time",
            created_at=date.today(),
            modified_at=date.today(),
        )
    for protein in proteins:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=protein,
            category="protein",
            created_at=date.today(),
            modified_at=date.today(),
        )

    return jsonify(message="RECETA SUBIDA")


@app.route("/viewRecipes", methods=["POST"])
def viewPersonalRecipes():
    data = request.get_json() or {}
    user_id = data.get("id")
    recipes = Recipe.select().join(Users).where(Users.id == user_id)
    recipes_list = [
        {
            "id": recipe.id,
            "title": recipe.recipe_title,
            "image": recipe.recipe_image,
            "description": recipe.recipe_description,
            "video": recipe.recipe_video,
        }
        for recipe in recipes
    ]
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
    return jsonify(message=recipes_list, categories_list=categories_list)


@app.route("/viewAll", methods=["POST"])
def viewAllRecipes():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    recipes = Recipe.select().where(Recipe.recipe_visibility == True)  # noqa: E712
    recipes_list = [
        {
            "id": recipe.id,
            "title": recipe.recipe_title,
            "image": recipe.recipe_image,
            "description": recipe.recipe_description,
            "video": recipe.recipe_video,
        }
        for recipe in recipes
    ]
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
    if iduser:
        favorites_list = [
            {"id_recipe": favorite.id_recipe_id}
            for favorite in UserFavorite.select().where(UserFavorite.id_user == iduser)
        ]
        reviews_list = [
            {
                "id_recipe": review.id_recipe_id,
                "review": review.recipe_review_item_value,
            }
            for review in RecipeReview.select().where(RecipeReview.id_user == iduser)
        ]
        return jsonify(
            recipes_list=recipes_list,
            favorites_list=favorites_list,
            reviews_list=reviews_list,
            categories_list=categories_list,
        )
    return jsonify(recipes_list=recipes_list, categories_list=categories_list)


@app.route("/updateFavs", methods=["POST"])
def updateFavs():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    if not idrecipe or not iduser:
        return jsonify(message="ERROR"), 400
    if UserFavorite.select().where(
        (UserFavorite.id_recipe == idrecipe) & (UserFavorite.id_user == iduser)
    ).exists():
        return jsonify(message="Favorite save")
    UserFavorite.create(
        id_recipe=idrecipe,
        id_user=iduser,
        created_at=date.today(),
        modified_at=date.today(),
    )
    return jsonify(message="Favorite save")


@app.route("/deleteFavs", methods=["POST"])
def deleteFavs():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    query = UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe)
    if iduser:
        query = query.where(UserFavorite.id_user == iduser)
    query.execute()
    return jsonify(message="Favorite delete")


@app.route("/updateRating", methods=["POST"])
def updateRating():
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


@app.route("/viewRecipe", methods=["POST"])
def viewRecipe():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    recipes = Recipe.select().where(Recipe.id == idrecipe)
    recipe_list = [
        {
            "title": recipe.recipe_title,
            "description": recipe.recipe_description,
            "visibility": bool(recipe.recipe_visibility),
            "video": recipe.recipe_video,
            "id_user": recipe.id_user_id,
            "image": recipe.recipe_image,
        }
        for recipe in recipes
    ]
    ingredient_list = [
        {"ingredients": ingredient.ingredients_text, "quantity": ingredient.quantity_unit}
        for ingredient in RecipeIngredient.select().where(
            RecipeIngredient.id_recipe == idrecipe
        )
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
    if iduser:
        favorites_list = [
            {"id_recipe": favorite.id_recipe_id}
            for favorite in UserFavorite.select().where(UserFavorite.id_user == iduser)
        ]
        return jsonify(
            recipe_list=recipe_list,
            ingredient_list=ingredient_list,
            favorites_list=favorites_list,
            step_list=step_list,
            filters_list=filters_list,
        )
    return jsonify(
        recipe_list=recipe_list,
        ingredient_list=ingredient_list,
        step_list=step_list,
        filters_list=filters_list,
    )


@app.route("/viewComment", methods=["POST"])
def viewComment():
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


@app.route("/createComment", methods=["POST"])
def createComment():
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


@app.route("/deleteRecipe", methods=["POST"])
def deleteRecipe():
    data = request.get_json() or {}
    idrecipe = data.get("idrecipe")
    if not idrecipe:
        return jsonify(message="ERROR"), 400

    RecipeFilter.delete().where(RecipeFilter.id_recipe == idrecipe).execute()
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe == idrecipe).execute()
    RecipeComment.delete().where(RecipeComment.id_recipe == idrecipe).execute()
    UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe).execute()
    RecipeReview.delete().where(RecipeReview.id_recipe == idrecipe).execute()

    recipe_steps = list(RecipeStep.select().where(RecipeStep.id_recipe == idrecipe))
    for step in recipe_steps:
        links = list(RecipeStepImage.select().where(RecipeStepImage.id_step == step.id))
        image_ids = [link.id_image_id for link in links]
        RecipeStepImage.delete().where(RecipeStepImage.id_step == step.id).execute()
        if image_ids:
            StepImage.delete().where(StepImage.id.in_(image_ids)).execute()

    RecipeStep.delete().where(RecipeStep.id_recipe == idrecipe).execute()
    Recipe.delete().where(Recipe.id == idrecipe).execute()
    return jsonify(message="Recipe deleted")


@app.route("/deleteComment", methods=["POST"])
def deleteComment():
    data = request.get_json() or {}
    idcomment = data.get("idcomment")
    RecipeComment.delete().where(RecipeComment.id == idcomment).execute()
    return jsonify(message="Comment deleted")


@app.route("/editeComment", methods=["POST"])
def editeComment():
    data = request.get_json() or {}
    comment = data.get("comment")
    idcomment = data.get("idcomment")
    RecipeComment.update(comment_text=comment, modified_at=date.today()).where(
        RecipeComment.id == idcomment
    ).execute()
    return jsonify(message="Change Comment")


@app.route("/viewFavs", methods=["POST"])
def viewFavs():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    favorites = UserFavorite.select(UserFavorite.id_recipe).where(
        UserFavorite.id_user == iduser
    )
    favorites_list = [favorite.id_recipe_id for favorite in favorites]
    if not favorites_list:
        return jsonify(favorites_list=[], reviews_list=[], categories_list=[])

    recipes = Recipe.select().where(
        (Recipe.id.in_(favorites_list)) & (Recipe.recipe_visibility == True)  # noqa: E712
    )
    recipes_list = [
        {
            "id": recipe.id,
            "title": recipe.recipe_title,
            "image": recipe.recipe_image,
            "description": recipe.recipe_description,
        }
        for recipe in recipes
    ]
    reviews_list = [
        {
            "id_recipe": review.id_recipe_id,
            "review": review.recipe_review_item_value,
        }
        for review in RecipeReview.select().where(
            (RecipeReview.id_user == iduser)
            & (RecipeReview.id_recipe.in_(favorites_list))
        )
    ]
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
    return jsonify(
        favorites_list=recipes_list,
        reviews_list=reviews_list,
        categories_list=categories_list,
    )


@app.route("/viewProfile", methods=["POST"])
def viewProfile():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    users = Users.select(Users.user_name, Users.user_email, Users.user_image).where(
        Users.id == iduser
    )
    users_list = [
        {"name": user.user_name, "email": user.user_email, "image": user.user_image}
        for user in users
    ]
    return jsonify(message=users_list)


@app.route("/editeRecipe", methods=["POST"])
def editeRecipe():
    data = request.get_json() or {}
    recipe_id = data.get("idrecipe")
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

    recipe = Recipe.get_or_none((Recipe.id == recipe_id) & (Recipe.id_user == user.id))
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404

    image_url = None
    if image and isinstance(image, dict):
        if image.get("base64"):
            image_url = save_base64_file(
                image["base64"], image.get("name"), app.config["UPLOAD_FOLDER_IMAGES"]
            )
        else:
            image_url = image.get("name")

    video_url = None
    if video and isinstance(video, dict):
        if video.get("base64"):
            video_url = save_base64_file(
                video["base64"], video.get("name"), app.config["UPLOAD_FOLDER_VIDEOS"]
            )
        else:
            video_url = video.get("name")

    recipe.recipe_title = title
    recipe.recipe_description = description
    recipe.recipe_visibility = bool(visibility)
    if image_url:
        recipe.recipe_image = image_url
    if video_url:
        recipe.recipe_video = video_url
    recipe.modified_at = date.today()
    recipe.save()

    step_ids = [s.id for s in RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id)]
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

    for i in range(len(ingredients)):
        quantity = quantities[i] if i < len(quantities) else ""
        RecipeIngredient.create(
            id_recipe=recipe.id,
            id_user=user.id,
            ingredients_text=ingredients[i],
            quantity_unit=quantity,
            created_at=date.today(),
            modified_at=date.today(),
        )

    for step in steps:
        step_title = step.get("title")
        step_text = step.get("description")
        step_image = step.get("image")
        step_image_url = None
        if step_image and isinstance(step_image, dict):
            if step_image.get("base64"):
                step_image_url = save_base64_file(
                    step_image["base64"],
                    step_image.get("name"),
                    app.config["UPLOAD_FOLDER_IMAGES"],
                )
            else:
                step_image_url = step_image.get("name")

        recipe_step = RecipeStep.create(
            id_recipe=recipe.id,
            id_user=user.id,
            step_title=step_title,
            step_description=step_text,
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

    if typeeat:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=typeeat,
            category="typeeat",
            created_at=date.today(),
            modified_at=date.today(),
        )
    if ccaa:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=ccaa,
            category="ccaa",
            created_at=date.today(),
            modified_at=date.today(),
        )
    if time:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=time,
            category="time",
            created_at=date.today(),
            modified_at=date.today(),
        )
    for protein in proteins:
        RecipeFilter.create(
            id_recipe=recipe.id,
            type=protein,
            category="protein",
            created_at=date.today(),
            modified_at=date.today(),
        )
    return jsonify(message="Receta actualizada correctamente")


@app.route("/changeImage", methods=["POST"])
def changeImage():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    image = data.get("image")
    if not image or not isinstance(image, dict):
        return jsonify(message="Image data not valid"), 400

    image_base64 = image.get("base64")
    image_name = image.get("name")
    if not image_base64:
        return jsonify(message="No base64 data found"), 400

    image_url = save_base64_file(
        image_base64, image_name, app.config["UPLOAD_FOLDER_IMAGES"]
    )
    if not image_url:
        return jsonify(message="Failed to save image"), 500

    Users.update(user_image=image_url, modified_at=date.today()).where(
        Users.id == iduser
    ).execute()
    return jsonify(message="Image Changed", newImage=image_url)


@app.route("/changeName", methods=["POST"])
def changeName():
    data = request.get_json() or {}
    name = data.get("name")
    iduser = data.get("iduser")
    user_token = data.get("userToken")
    if not Users.select().where(Users.user_token == user_token).exists():
        return jsonify(message="ERROR"), 401
    Users.update(user_name=name, modified_at=date.today()).where(
        Users.id == iduser
    ).execute()
    return jsonify(message=name)


@app.route("/changeEmail", methods=["POST"])
def changeEmail():
    data = request.get_json() or {}
    email = data.get("email")
    iduser = data.get("iduser")
    user_token = data.get("userToken")
    if not Users.select().where(Users.user_token == user_token).exists():
        return jsonify(message="ERROR"), 401
    Users.update(user_email=email, modified_at=date.today()).where(
        Users.id == iduser
    ).execute()
    token = create_access_token(identity=email)
    Users.update(user_token=token, modified_at=date.today()).where(
        Users.id == iduser
    ).execute()
    return jsonify(message=email, userToken=token)


@app.route("/filterRecipe", methods=["POST"])
def filterRecipe():
    data = request.get_json() or {}
    typeeat = data.get("typeeat")
    ccaa = data.get("ccaa")
    time = data.get("time")
    proteins = data.get("proteins") or []

    clause = None
    for value in [typeeat, ccaa, time, *proteins]:
        if not value:
            continue
        part = RecipeFilter.type == value
        clause = part if clause is None else (clause | part)

    if clause is None:
        return jsonify(message=[])

    filter_list = [
        {"idrecipe": f.id_recipe_id} for f in RecipeFilter.select().where(clause)
    ]
    return jsonify(message=filter_list)


@app.route("/recipeFilter", methods=["POST"])
def recipeFilter():
    data = request.get_json() or {}
    filtered = data.get("filtered") or []
    iduser = data.get("iduser")
    idrecipes = [item["idrecipe"] for item in filtered if "idrecipe" in item]
    if not idrecipes:
        return jsonify(filtered_recipes=[])

    filtereds = Recipe.select().where(
        (Recipe.id.in_(idrecipes)) & (Recipe.recipe_visibility == True)  # noqa: E712
    )
    filtered_recipes = [
        {
            "id": recipe.id,
            "title": recipe.recipe_title,
            "image": recipe.recipe_image,
            "description": recipe.recipe_description,
            "video": recipe.recipe_video,
        }
        for recipe in filtereds
    ]
    if iduser:
        favorites_list = [
            {"id_recipe": favorite.id_recipe_id}
            for favorite in UserFavorite.select().where(UserFavorite.id_user == iduser)
        ]
        reviews_list = [
            {
                "id_recipe": review.id_recipe_id,
                "review": review.recipe_review_item_value,
            }
            for review in RecipeReview.select().where(RecipeReview.id_user == iduser)
        ]
        return jsonify(
            filtered_recipes=filtered_recipes,
            favorites_list=favorites_list,
            reviews_list=reviews_list,
        )
    return jsonify(filtered_recipes=filtered_recipes)


@app.route("/changePassword", methods=["POST"])
def changePassword():
    data = request.get_json() or {}
    user_token = data.get("userToken")
    iduser = data.get("iduser")
    new_password = data.get("newPassword")
    if not Users.select().where(Users.user_token == user_token).exists():
        return jsonify(message="ERROR"), 401
    Users.update(
        user_password=hashlib.sha256(new_password.encode("utf-8")).hexdigest(),
        modified_at=date.today(),
    ).where(Users.id == iduser).execute()
    return jsonify(message="Contraseña Actualizada")


def _delete_user_cascade(iduser):
    id_recipes = list(Recipe.select().where(Recipe.id_user == iduser))
    for recipe in id_recipes:
        steps = list(RecipeStep.select().where(RecipeStep.id_recipe == recipe.id))
        for step in steps:
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


@app.route("/deleteProfile", methods=["POST"])
def deleteProfile():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    _delete_user_cascade(iduser)
    return jsonify(message="Perfil eliminado")


@app.route("/allUsers", methods=["POST"])
def allUsers():
    data = request.get_json() or {}
    user_type = data.get("type")
    user_token = data.get("userToken")
    if not _is_admin(user_token):
        return jsonify(users_list=[])
    users = Users.select().where(Users.user_type != user_type)
    users_list = [
        {"iduser": user.id, "name": user.user_name, "email": user.user_email}
        for user in users
    ]
    return jsonify(users_list=users_list)


@app.route("/deleteUser", methods=["POST"])
def deleteUser():
    data = request.get_json() or {}
    iduser = data.get("iduser")
    user_token = data.get("userToken")
    if not _is_admin(user_token):
        return jsonify(message="ERROR"), 403
    _delete_user_cascade(iduser)
    return jsonify(message="Perfil eliminado")


@app.route("/averageStars", methods=["POST"])
def averageStars():
    try:
        query = (
            RecipeReview.select(
                RecipeReview.id_recipe,
                fn.AVG(RecipeReview.recipe_review_item_value).alias("average_rating"),
            ).group_by(RecipeReview.id_recipe)
        )
        result = []
        for item in query:
            average_rating = item.average_rating if item.average_rating is not None else 0
            result.append(
                {
                    "recipe_id": item.id_recipe_id,
                    "average_rating": round(float(average_rating), 2),
                }
            )
        return jsonify(media=result)
    except Exception as e:
        return jsonify(message="Error: " + str(e)), 500


# Compatibilidad por si algún cliente pide ficheros fuera de /static
@app.route("/static/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER_IMAGES"], filename)


@app.route("/static/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER_VIDEOS"], filename)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=port)
