from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import create_tables,Users, Recipe, RecipeComment, RecipeReview, UserFavorite, RecipeIngredient, StepImage, RecipeStep, RecipeStepImage, RecipeFilter
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import Config
from peewee import DoesNotExist
from datetime import date
import hashlib
import os
import base64

app = Flask(__name__)
create_tables()
app.config['UPLOAD_FOLDER_IMAGES'] = 'static/images'
app.config['UPLOAD_FOLDER_VIDEOS'] = 'static/videos'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)
mysql = MySQL(app)

def save_base64_file(base64_data, file_name, folder):
    if base64_data:
        try:
            if base64_data.startswith('data:'):
                base64_data = base64_data.split(',')[1]

            file_data = base64.b64decode(base64_data)

            file_path = os.path.join(folder, file_name)
            with open(file_path, 'wb') as file:
                file.write(file_data)

            return file_path
        except Exception as e:
            print(f"Error al guardar archivo base64: {e}")
            return None
    else:
        return None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    token = create_access_token(identity=email)
    type = data.get("type")
    if Users.select().where(Users.user_email == email).exists():
        return jsonify(message="ERROR")
    user = Users(user_name = name,user_email = email, user_password = hashlib.sha256(password.encode('utf-8')).hexdigest(), user_type = type,user_token = token, user_image= "/static/images/NonPerfil.webp", created_at = date.today(), modified_at = date.today())
    user.save()
    return jsonify(userToken = token, iduser = user.id)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    token = create_access_token(identity=email)
    if Users.select().where((Users.user_email == email) & (Users.user_password == hashlib.sha256(password.encode('utf-8')).hexdigest())).exists():
        user = Users.select(Users.id).where((Users.user_email == email) & (Users.user_password == hashlib.sha256(password.encode('utf-8')).hexdigest())).get()       
        Users.update(user_token=token).where(Users.id == user.id).execute()
        return jsonify(userToken=token, iduser=user.id)
    return jsonify(message="ERROR User NOT LOGGED")

@app.route('/create', methods=['POST'])
def createRecipe():
    data = request.get_json()
    title = data.get("title")
    image = data.get("image")
    image_url = None
    if image:  
        image_url = save_base64_file(image['base64'], image['name'], app.config['UPLOAD_FOLDER_IMAGES'])
    video = data.get("video")
    video_url = None
    if video:
        video_url = save_base64_file(video['base64'], video['name'], app.config['UPLOAD_FOLDER_VIDEOS'])
    description = data.get("description")
    ingredients = data.get("ingredients")
    quantities = data.get("quantities")
    steps = data.get("steps")
    if not quantities:
        quantities = []
    if not ingredients:
        ingredients = []
    if not steps:
        steps = []
    token = data.get("token")
    proteins = data.get("proteins")
    typeeat = data.get("typeeat")
    ccaa = data.get("ccaa")
    time = data.get("time")
    
    if Users.select().where((Users.user_token == token)).exists():
        user = Users.select(Users.id).where((Users.user_token == token)).get()
        recipe = Recipe(recipe_title = title,recipe_image = image_url,recipe_description = description, recipe_video = video_url, id_user_id = user.id, created_at = date.today(), modified_at = date.today())
        recipe.save() 
        for i in range(len(ingredients)):        
            quantity = quantities[i] if i < len(quantities) else ''
            recipe_ingredient = RecipeIngredient(id_recipe_id = recipe.id, id_user_id = user.id,ingredients_text=ingredients[i],quantity_unit=quantity, created_at = date.today(), modified_at = date.today())
            recipe_ingredient.save()
        for i in range(len(steps)):
            step_title = steps[i].get('title')
            step_text = steps[i].get('text')
            step_image = steps[i].get('image')

            step_image_url = None
            if step_image:
                step_image_url = save_base64_file(step_image['base64'], step_image['name'], app.config['UPLOAD_FOLDER_IMAGES'])

            recipe_step = RecipeStep(
                id_recipe=recipe.id,
                id_user_id=user.id,
                step_title=step_title,
                step_description=step_text,
                created_at=date.today(),
                modified_at=date.today()
            )
            recipe_step.save()
            
            if step_image_url:
                step_img = StepImage(
                    id_user_id=user.id,
                    step_image=step_image_url,
                    created_at=date.today(),
                    modified_at=date.today()
                )
                step_img.save()

                recipe_step_img = RecipeStepImage(
                    id_step=recipe_step.id,
                    id_image=step_img.id
                )
                recipe_step_img.save()
        """if proteins:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=proteins,created_at = date.today(), modified_at = date.today())
            filters.save()"""
        if typeeat:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=typeeat,created_at = date.today(), modified_at = date.today())
            filters.save()
        if ccaa:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=ccaa,created_at = date.today(), modified_at = date.today())
            filters.save()
        if time:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=time,created_at = date.today(), modified_at = date.today())
            filters.save()
        for protein in proteins:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=protein,created_at = date.today(), modified_at = date.today())
            filters.save()
        return jsonify(message= "RECETA SUBIDA")

@app.route('/viewRecipes', methods=['POST'])
def viewPersonalRecipes():
    data = request.get_json()
    id = data.get("id")
    recipes = Recipe.select().join(Users).where(Users.id == id)
    recipes_list = [{"id": recipe.id, "title": recipe.recipe_title,"image":recipe.recipe_image, "description":recipe.recipe_description, "video":recipe.recipe_video} for recipe in recipes]
    return jsonify(message=recipes_list)
    
@app.route('/viewAll', methods=['POST'])
def viewAllRecipes():
    data = request.get_json()
    iduser = data.get("iduser")
    recipes = Recipe.select()
    recipes_list = [{"id": recipe.id, "title": recipe.recipe_title,"image":recipe.recipe_image, "description":recipe.recipe_description, "video":recipe.recipe_video} for recipe in recipes]
    if iduser:
        favorites = UserFavorite.select().where(UserFavorite.id_user_id ==iduser)
        favorites_list = [{"id_recipe": favorite.id_recipe_id} for favorite in favorites]
        reviews = RecipeReview.select().where(RecipeReview.id_user_id ==iduser)
        reviews_list = [{"id_recipe": review.id_recipe_id, "review": review.recipe_review_item_value} for review in reviews]
        return jsonify(recipes_list=recipes_list, favorites_list=favorites_list, reviews_list=reviews_list)
    return jsonify(recipes_list=recipes_list)

@app.route('/updateFavs', methods=['POST'])
def updateFavs():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    favorite = UserFavorite(id_recipe_id= idrecipe, id_user_id = iduser, created_at = date.today(), modified_at = date.today())
    favorite.save()
    return jsonify(message="Favorite save")

@app.route('/deleteFavs', methods=['POST'])
def deleteFavs():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    UserFavorite.delete().where(UserFavorite.id_recipe_id == idrecipe).execute()
    return jsonify(message="Favorite delete")

@app.route('/updateRating', methods=['POST'])
def updateRating():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    rating = data.get("rating")
    if RecipeReview.select().where((RecipeReview.id_recipe_id == idrecipe) & (RecipeReview.id_user_id==iduser)).exists():
        review=RecipeReview.select(RecipeReview.id).where((RecipeReview.id_recipe_id == idrecipe) & (RecipeReview.id_user_id==iduser)).get()
        RecipeReview.update(recipe_review_item_value=rating).where(RecipeReview.id == review.id).execute()
        return jsonify(message="Review update")
    review = RecipeReview(id_recipe_id= idrecipe, id_user_id = iduser, recipe_review_item_value= rating,created_at = date.today(), modified_at = date.today())
    review.save()
    return jsonify(message="Review save")

@app.route('/viewRecipe', methods=['POST'])
def viewRecipe():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    recipes = Recipe.select().where(Recipe.id == idrecipe)
    recipe_list = [{"title": recipe.recipe_title, "description": recipe.recipe_description, "video":recipe.recipe_video,"id_user":recipe.id_user_id, "image":recipe.recipe_image} for recipe in recipes]
    ingredientes = RecipeIngredient.select().where(RecipeIngredient.id_recipe_id ==idrecipe)
    ingredient_list = [{"ingredients":ingredient.ingredients_text, "quantity":ingredient.quantity_unit} for ingredient in ingredientes]
    steps = RecipeStep.select().where(RecipeStep.id_recipe == idrecipe)
    step_list = []
    for step in steps:
        step_image = (StepImage.select(StepImage.step_image).join(RecipeStepImage).where(RecipeStepImage.id_step == step.id).first())
        step_list.append({"title": step.step_title,"description": step.step_description,"image": step_image.step_image if step_image else None})
    if iduser:
        favorites = UserFavorite.select().where(UserFavorite.id_user_id ==iduser)
        favorites_list = [{"id_recipe": favorite.id_recipe_id} for favorite in favorites]
        return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list, favorites_list=favorites_list, step_list=step_list)
    return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list, step_list=step_list)

@app.route('/viewComment', methods=['POST'])
def viewComment(): 
    data = request.get_json()
    idrecipe = data.get("idrecipe") 
    comments = RecipeComment.select().where(RecipeComment.id_recipe_id ==idrecipe)
    comment_list = []
    for comment in comments:
        user = Users.get(Users.id == comment.id_user_id)
        comment_list.append({
            "id": comment.id,
            "comment": comment.comment_text,
            "iduser": comment.id_user_id,
            "username": user.user_name
        })
    return jsonify(comment_list=comment_list)
    
@app.route('/createComment', methods=['POST'])
def createComment():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser=data.get("iduser")
    comment=data.get("comment")
    user = Users.select(Users.user_name).where(Users.id == iduser).execute()
    commentRecipe = RecipeComment(comment_text= comment,id_recipe_id= idrecipe, id_user_id= iduser,created_at = date.today(), modified_at = date.today())
    commentRecipe.save() 
    return jsonify(message ="Comment Update",username=user[0].user_name)

@app.route('/deleteRecipe', methods=['POST'])
def deleteRecipe():
    data = request.get_json()
    idrecipe = data.get('idrecipe')
    RecipeFilter.delete().where(RecipeFilter.id_recipe==idrecipe).execute()
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe == idrecipe).execute()
    RecipeComment.delete().where(RecipeComment.id_recipe == idrecipe).execute()
    UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe).execute()
    RecipeReview.delete().where(RecipeReview.id_recipe == idrecipe).execute()
    recipe_steps = RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == idrecipe).execute()
    for step in recipe_steps:
        step_images = RecipeStepImage.select().where(RecipeStepImage.id_step == step.id)
        for step_image in step_images:     
            RecipeStepImage.delete().where(RecipeStepImage.id_step == step.id).execute()
        StepImage.delete().where(StepImage.id == step_image.id_image).execute()
    RecipeStep.delete().where(RecipeStep.id_recipe == idrecipe).execute()
    Recipe.delete().where(Recipe.id == idrecipe).execute()
    return jsonify(message="Recipe comment")

@app.route('/deleteComment', methods=['POST'])
def deleteComment():
    data = request.get_json()
    idcomment = data.get('idcomment')
    RecipeComment.delete().where(RecipeComment.id == idcomment).execute()
    return jsonify(message="Recipe deleted")

@app.route('/editeComment', methods=['POST'])
def editeComment():
    data = request.get_json()
    comment = data.get('comment')
    idcomment = data.get('idcomment')
    RecipeComment.update(comment_text=comment).where(RecipeComment.id == idcomment).execute()
    return jsonify(message="Change Comment")

@app.route('/viewFavs', methods=['POST'])
def viewFavs():
    data = request.get_json()
    iduser = data.get("iduser")
    favorites = UserFavorite.select(UserFavorite.id_recipe).where(UserFavorite.id_user == iduser).execute()
    favorites_list = [favorite.id_recipe_id for favorite in favorites]
    recipes = Recipe.select().where(Recipe.id.in_(favorites_list))
    recipes_list = [{
        "id": recipe.id,
        "title": recipe.recipe_title,
        "image": recipe.recipe_image,
        "description": recipe.recipe_description
    } for recipe in recipes]
    reviews = RecipeReview.select().where(
        (RecipeReview.id_user_id == iduser) &
        (RecipeReview.id_recipe_id.in_(favorites_list))
    )
    reviews_list = [{
        "id_recipe": review.id_recipe_id,
        "review": review.recipe_review_item_value
    } for review in reviews]
    return jsonify(message=recipes_list, message2=reviews_list)

@app.route('/viewProfile',methods=['POST'])
def viewProfile():
    data = request.get_json()
    iduser = data.get("iduser")
    users = Users.select(Users.user_name,Users.user_email, Users.user_image ).where(Users.id == iduser).execute()
    users_list = [{"name":user.user_name, "email":user.user_email, "image":user.user_image} for user in users]
    return jsonify(message=users_list )

@app.route('/editeRecipe', methods=['POST'])
def editeRecipe():
    data = request.get_json()
    recipe_id = data.get("idrecipe") 
    title = data.get("title")
    image = data.get("image")
    video = data.get("video")
    description = data.get("description")
    ingredients = data.get("ingredients") or []
    quantities = data.get("quantities") or []
    steps = data.get("steps") or []
    token = data.get("token")

    user = Users.get_or_none(Users.user_token == token)
    if not user:
        return jsonify(message="Usuario no autenticado"), 401

    recipe = Recipe.get_or_none((Recipe.id == recipe_id) & (Recipe.id_user_id == user.id))
    if not recipe:
        return jsonify(message="Receta no encontrada"), 404

    image_url = None
    if image and isinstance(image, dict):
        if "base64" in image and image["base64"]:
            image_url = save_base64_file(image['base64'], image['name'], app.config['UPLOAD_FOLDER_IMAGES'])
        else:
            image_url = image.get("name") 

    video_url = None
    if video and isinstance(video, dict):
        if "base64" in video and video["base64"]:
            video_url = save_base64_file(video['base64'], video['name'], app.config['UPLOAD_FOLDER_VIDEOS'])
        else:
            video_url = video.get("name")

    recipe.recipe_title = title
    recipe.recipe_description = description
    recipe.recipe_image = image_url if image_url else recipe.recipe_image  
    recipe.recipe_video = video_url if video_url else recipe.recipe_video  
    recipe.modified_at = date.today()
    recipe.save()

    RecipeIngredient.delete().where(RecipeIngredient.id_recipe_id == recipe.id).execute()

    RecipeStepImage.delete().where(RecipeStepImage.id_step.in_(
        RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id)
    )).execute()

    StepImage.delete().where(StepImage.id.in_(
        RecipeStepImage.select(RecipeStepImage.id_image).where(
            RecipeStepImage.id_step.in_(RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id))
        )
    )).execute()

    RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()

    for i in range(len(ingredients)):
        quantity = quantities[i] if i < len(quantities) else ''
        RecipeIngredient.create(
            id_recipe_id=recipe.id,
            id_user_id=user.id,
            ingredients_text=ingredients[i],
            quantity_unit=quantity,
            created_at=date.today(),
            modified_at=date.today()
        )

    for step in steps:
        step_title = step.get('title')
        step_text = step.get('description')
        step_image = step.get('image')

        step_image_url = None
        if step_image and isinstance(step_image, dict):
            if "base64" in step_image and step_image["base64"]:
                step_image_url = save_base64_file(step_image['base64'], step_image['name'], app.config['UPLOAD_FOLDER_IMAGES'])
            else:
                step_image_url = step_image.get("name")

        recipe_step = RecipeStep.create(
            id_recipe=recipe.id,
            id_user_id=user.id,
            step_title=step_title,
            step_description=step_text,
            created_at=date.today(),
            modified_at=date.today()
        )
        if step_image_url:
            step_img = StepImage.create(
                id_user_id=user.id,
                step_image=step_image_url,
                created_at=date.today(),
                modified_at=date.today()
            )

            RecipeStepImage.create(
                id_step=recipe_step.id,
                id_image=step_img.id
            )

    return jsonify(message="Receta actualizada correctamente")

@app.route('/changeImage',methods=['POST'])
def changeImage():
    data = request.get_json()
    iduser = data.get("iduser")
    image = data.get("image")
    token = data.get("userToken")
    image_url = None
    if image:  
        image_base64 = image.get("base64")
        image_name = image.get("name")
        
        if image_base64:
            image_url = save_base64_file(image_base64, image_name, app.config['UPLOAD_FOLDER_IMAGES'])
            if image_url:
                Users.update(user_image=image_url).where(Users.id == iduser).execute()
                return jsonify(message="Image Changed", newImage=image_url)
            else:
                return jsonify(message="Failed to save image")
        else:
            return jsonify(message="No base64 data found")

    return jsonify(message="Image data not valid")

@app.route('/changeName',methods=['POST'])
def changeName():
    data = request.get_json()
    name = data.get("name")
    iduser = data.get("iduser")
    userToken = data.get("userToken")
    if Users.select().where((Users.user_token == userToken)).exists():
        Users.update(user_name=name).where(Users.id == iduser).execute()
        return jsonify(message=name)
    
@app.route('/changeEmail',methods=['POST'])
def changeEmail():
    data = request.get_json()
    email = data.get("email")
    iduser = data.get("iduser")
    userToken = data.get("userToken")
    if Users.select().where((Users.user_token == userToken)).exists():
        Users.update(user_email=email).where(Users.id == iduser).execute()
        token = create_access_token(identity=email)
        user = Users.select(Users.id).where((Users.user_email == email)).get() 
        Users.update(user_token=token).where(Users.id == user.id).execute()
        return jsonify(message=email,userToken=token)

@app.route('/filterRecipe', methods=['POST'])
def filterRecipe():
    data = request.get_json()
    typeeat = data.get("typeeat")
    filters=RecipeFilter.select().where(RecipeFilter.type == typeeat).execute()
    filter_list = [{"idrecipe":filter.id_recipe_id} for filter in filters]
    return jsonify(message=filter_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

