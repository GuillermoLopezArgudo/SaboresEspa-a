import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request, abort, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import create_tables,Users, Recipe, RecipeComment, RecipeReview, UserFavorite, RecipeIngredient, StepImage, RecipeStep, RecipeStepImage, RecipeFilter,SubRecipeStep,SubRecipeIngredient,RecipeSubStepImage,SubStepImage,LikesComment,DislikeComment,RecipeSubComment
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import Config
from peewee import DoesNotExist
from datetime import date
from peewee import fn
import hashlib
import base64
from models import db, BaseModel
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER_IMAGES'] = 'static/images'
app.config['UPLOAD_FOLDER_VIDEOS'] = 'static/videos'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') 
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')


CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)
mysql = MySQL(app)
mail = Mail(app)


try:
    db.connect(reuse_if_open=True)
    print("✅ Conectado a MySQL")
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)

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
    create_tables()
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
    return jsonify(userToken = token)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    token = create_access_token(identity=email)
    if Users.select().where((Users.user_email == email) & (Users.user_password == hashlib.sha256(password.encode('utf-8')).hexdigest())).exists():
        user = Users.select(Users.id,Users.user_type).where((Users.user_email == email) & (Users.user_password == hashlib.sha256(password.encode('utf-8')).hexdigest())).get()       
        Users.update(user_token=token).where(Users.id == user.id).execute()
        return jsonify(userToken=token)
    return jsonify(message="ERROR User NOT LOGGED")

@app.route('/create', methods=['POST'])
def createRecipe():
    #create_tables()
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
    subingredients = data.get("subingredients")
    subquantities = data.get("subquantities")
    substeps = data.get("substeps")
    if not quantities:
        quantities = []
    if not ingredients:
        ingredients = []
    if not steps:
        steps = []
    if not subquantities:
        subquantities = []
    if not subingredients:
        subingredients = []
    if not substeps:
        substeps = []
    token = data.get("token")
    proteins = data.get("proteins")
    typeeat = data.get("typeeat")
    ccaa = data.get("ccaa")
    time = data.get("time")
    visibility = data.get('visibility')
    
    if Users.select().where((Users.user_token == token)).exists():
        user = Users.select(Users.id).where((Users.user_token == token)).get()
        recipe = Recipe(recipe_title = title,recipe_visibility=visibility,recipe_image = image_url,recipe_description = description, recipe_video = video_url, id_user_id = user.id, created_at = date.today(), modified_at = date.today())
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
        for i in range(len(subingredients)):        
            subquantity = subquantities[i] if i < len(subquantities) else ''
            recipe_ingredient = SubRecipeIngredient(id_recipe_id = recipe.id, id_user_id = user.id,ingredients_text=subingredients[i],quantity_unit=subquantity, created_at = date.today(), modified_at = date.today())
            recipe_ingredient.save()
        for i in range(len(substeps)):
            step_title = substeps[i].get('title')
            step_text = substeps[i].get('text')
            step_image = substeps[i].get('image')

            step_image_url = None
            if step_image:
                step_image_url = save_base64_file(step_image['base64'], step_image['name'], app.config['UPLOAD_FOLDER_IMAGES'])

            recipe_step = SubRecipeStep(
                id_recipe=recipe.id,
                id_user_id=user.id,
                step_title=step_title,
                step_description=step_text,
                created_at=date.today(),
                modified_at=date.today()
            )
            recipe_step.save()
            
            if step_image_url:
                step_img = SubStepImage(
                    id_user_id=user.id,
                    step_image=step_image_url,
                    created_at=date.today(),
                    modified_at=date.today()
                )
                step_img.save()

                recipe_step_img = RecipeSubStepImage(
                    id_step=recipe_step.id,
                    id_image=step_img.id
                )
                recipe_step_img.save()
        if typeeat:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=typeeat,category="typeeat",created_at = date.today(), modified_at = date.today())
            filters.save()
        if ccaa:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=ccaa,category="ccaa",created_at = date.today(), modified_at = date.today())
            filters.save()
        if time:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=time,category="time",created_at = date.today(), modified_at = date.today())
            filters.save()
        for protein in proteins:
            filters = RecipeFilter(id_recipe_id=recipe.id,type=protein,category="protein",created_at = date.today(), modified_at = date.today())
            filters.save()
        return jsonify(message= "RECETA SUBIDA")

@app.route('/viewRecipes', methods=['POST'])
def viewPersonalRecipes():
    data = request.get_json()
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        recipes = Recipe.select().join(Users).where(Users.id == user_id)
        recipes_list = [{"id": recipe.id, "title": recipe.recipe_title,"image":recipe.recipe_image, "description":recipe.recipe_description, "video":recipe.recipe_video} for recipe in recipes]
        categories_list = []
        for recipe in recipes:
            categories = RecipeFilter.select().where(RecipeFilter.id_recipe == recipe.id)
            for categorie in categories:
                categories_list.append({
                    "recipe_id": recipe.id,
                    "type": categorie.type,
                    "category": categorie.category
                })    
        return jsonify(recipes_list=recipes_list,categories_list=categories_list)
    return jsonify(recipes_list="",categories_list="")
    
@app.route('/viewAll', methods=['POST'])
def viewAllRecipes():

    data = request.get_json()
    recipes = Recipe.select().where(Recipe.recipe_visibility == 1)
    recipes_list = [{"id": recipe.id, "title": recipe.recipe_title,"image":recipe.recipe_image, "description":recipe.recipe_description, "video":recipe.recipe_video} for recipe in recipes]
    categories_list = []
    for recipe in recipes:
        categories = RecipeFilter.select().where(RecipeFilter.id_recipe == recipe.id)
        for categorie in categories:
            categories_list.append({
                "recipe_id": recipe.id,
                "type": categorie.type,
                "category": categorie.category
            })
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        favorites = UserFavorite.select().where(UserFavorite.id_user_id ==user_id)
        favorites_list = [{"id_recipe": favorite.id_recipe_id} for favorite in favorites]
        reviews = RecipeReview.select().where(RecipeReview.id_user_id ==user_id)
        reviews_list = [{"id_recipe": review.id_recipe_id, "review": review.recipe_review_item_value} for review in reviews]

        return jsonify(recipes_list=recipes_list, favorites_list=favorites_list, reviews_list=reviews_list,categories_list=categories_list,user_id=user_id)
    return jsonify(recipes_list=recipes_list,categories_list=categories_list)

@app.route('/updateFavs', methods=['POST'])
def updateFavs():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        favorite = UserFavorite(id_recipe_id= idrecipe, id_user_id = user_id, created_at = date.today(), modified_at = date.today())
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
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        rating = data.get("rating")
        if RecipeReview.select().where((RecipeReview.id_recipe_id == idrecipe) & (RecipeReview.id_user_id==user_id)).exists():
            review=RecipeReview.select(RecipeReview.id).where((RecipeReview.id_recipe_id == idrecipe) & (RecipeReview.id_user_id==user_id)).get()
            RecipeReview.update(recipe_review_item_value=rating).where(RecipeReview.id == review.id).execute()
            return jsonify(message="Review update")
        review = RecipeReview(id_recipe_id= idrecipe, id_user_id = user_id, recipe_review_item_value= rating,created_at = date.today(), modified_at = date.today())
        review.save()
        return jsonify(message="Review save")

@app.route('/viewRecipe', methods=['POST'])
def viewRecipe():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    recipes = Recipe.select().where(Recipe.id == idrecipe)
    recipe = Recipe.select().where(Recipe.id == idrecipe).first()
    names =Users.select().where(Users.id == recipe.id_user).first()
    user_name = names.user_name
    recipe_list = [{"title": recipe.recipe_title, "description": recipe.recipe_description,"visibility": bool(recipe.recipe_visibility),"video":recipe.recipe_video,"id_user":recipe.id_user_id, "image":recipe.recipe_image} for recipe in recipes]
    ingredientes = RecipeIngredient.select().where(RecipeIngredient.id_recipe_id ==idrecipe)
    ingredient_list = [{"ingredients":ingredient.ingredients_text, "quantity":ingredient.quantity_unit} for ingredient in ingredientes]
    steps = RecipeStep.select().where(RecipeStep.id_recipe == idrecipe)
    step_list = []
    for step in steps:
        step_image = (StepImage.select(StepImage.step_image).join(RecipeStepImage).where(RecipeStepImage.id_step == step.id).first())
        step_list.append({"title": step.step_title,"description": step.step_description,"image": step_image.step_image if step_image else None})
    subingredientes = SubRecipeIngredient.select().where(SubRecipeIngredient.id_recipe_id ==idrecipe)
    subingredient_list = [{"ingredients":subingredient.ingredients_text, "quantity":subingredient.quantity_unit} for subingredient in subingredientes]
    substeps = SubRecipeStep.select().where(SubRecipeStep.id_recipe == idrecipe)
    substep_list = []
    for substep in substeps:
        step_image = (SubStepImage.select(SubStepImage.step_image).join(RecipeSubStepImage).where(RecipeSubStepImage.id_step == substep.id).first())
        substep_list.append({"title": substep.step_title,"description": substep.step_description,"image": step_image.step_image if step_image else None})        
    filters = RecipeFilter.select().where(RecipeFilter.id_recipe_id == idrecipe)
    filters_list = [{"type":filter.type, "category":filter.category} for filter in filters]
    countLikes = LikesComment.select()
    countLikes_list = [{"id_comment":countLike.id_comment_id} for countLike in countLikes]
    countDisLikes = DislikeComment.select()
    countDisLikes_list = [{"id_comment":countDisLike.id_comment_id} for countDisLike in countDisLikes]
    if user:
        user_id = user.id
        user_token = user.user_token
        user_type = user.user_type
        if user_id:
            favorites = UserFavorite.select().where(UserFavorite.id_user_id ==user_id)
            favorites_list = [{"id_recipe": favorite.id_recipe_id} for favorite in favorites]
            likes = LikesComment.select().where(LikesComment.id_user == user.id)
            likes_list = [{"id_recipe":like.id_comment_id } for like in likes]
            dislikes = DislikeComment.select().where(DislikeComment.id_user == user.id)
            dislikes_list = [{"id_recipe":like.id_comment_id } for like in dislikes]
            return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list, favorites_list=favorites_list, step_list=step_list, filters_list=filters_list, subingredient_list=subingredient_list,substep_list=substep_list,user_id=user_id,user_token=user_token,user_name=user_name,user_type=user_type, likes_list= likes_list,dislikes_list=dislikes_list,countLikes_list=countLikes_list,countDisLikes_list=countDisLikes_list)
        return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list, favorites_list=favorites_list, step_list=step_list, filters_list=filters_list, subingredient_list=subingredient_list,substep_list=substep_list,user_id=user_id,user_token=user_token,user_name=user_name,user_type=user_type, likes_list= likes_list,dislikes_list=dislikes_list,countLikes_list=countLikes_list,countDisLikes_list=countDisLikes_list)
    return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list, step_list=step_list, filters_list=filters_list,subingredient_list=subingredient_list,substep_list=substep_list,user_name=user_name,countLikes_list=countLikes_list,countDisLikes_list=countDisLikes_list)

@app.route('/viewComment', methods=['POST'])
def viewComment(): 
    data = request.get_json()
    idrecipe = data.get("idrecipe") 
    token = data.get("userToken")
    comments = RecipeComment.select().where(RecipeComment.id_recipe_id == idrecipe)
    subcomments = RecipeSubComment.select().where(RecipeSubComment.id_recipe == idrecipe)
    comment_list = []
    for comment in comments:
        users = Users.select().where(Users.user_token == token).first()
        user = Users.get(Users.id == comment.id_user_id)
        user_type = users.user_type if users else ''
        comment_list.append({
            "id": comment.id,
            "comment": comment.comment_text,
            "iduser": comment.id_user_id,
            "username": user.user_name,
            "userToken": user.user_token,
            "type": user_type
        })
    subcomments_list = []
    for subcomment in subcomments:
        users = Users.select().where(Users.user_token == token).first()
        user = Users.get(Users.id == comment.id_user_id)
        user_type = users.user_type if users else ''
        subcomments_list.append({
            "id": subcomment.id,
            "id_comment": subcomment.id_comment_id,
            "comment": subcomment.comment_text,
            "iduser": subcomment.id_user_id,
            "username": user.user_name,
            "userToken": user.user_token,
            "type": user_type
        })
    return jsonify(comment_list=comment_list,subcomments_list=subcomments_list)
    
@app.route('/createComment', methods=['POST'])
def createComment():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    token = data.get("userToken")
    comment=data.get("comment")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        user = Users.select(Users.user_name).where(Users.id == user_id).execute()
        commentRecipe = RecipeComment(comment_text= comment,id_recipe_id= idrecipe, id_user_id= user_id,created_at = date.today(), modified_at = date.today())
        commentRecipe.save() 
        return jsonify(message ="Comment Update",username=user[0].user_name)

@app.route('/createSubComment', methods=['POST'])
def createSubComment():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    token = data.get("userToken")
    comment=data.get("comment")
    idcomment = data.get("idcomment")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        user = Users.select(Users.user_name).where(Users.id == user_id).execute()
        commentRecipe = RecipeSubComment(id_comment_id = idcomment, comment_text= comment,id_recipe_id= idrecipe, id_user_id= user_id,created_at = date.today(), modified_at = date.today())
        commentRecipe.save() 
        return jsonify(message ="Comment Update",username=user[0].user_name)

@app.route('/deleteRecipe', methods=['POST'])
def deleteRecipe():
    data = request.get_json()
    idrecipe = data.get('idrecipe')
    RecipeFilter.delete().where(RecipeFilter.id_recipe==idrecipe).execute()
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe == idrecipe).execute()
    SubRecipeIngredient.delete().where(SubRecipeIngredient.id_recipe == idrecipe).execute()
    DislikeComment.delete().where(DislikeComment.id_recipe== idrecipe).execute()
    LikesComment.delete().where(LikesComment.id_recipe== idrecipe).execute()
    RecipeSubComment.delete().where(RecipeSubComment.id_recipe == idrecipe).execute()
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
    recipe_substeps = SubRecipeStep.select(SubRecipeStep.id).where(SubRecipeStep.id_recipe == idrecipe).execute()
    for step in recipe_substeps:
        substep_images = RecipeSubStepImage.select().where(RecipeSubStepImage.id_step == step.id)
        for step_image in substep_images:     
            RecipeSubStepImage.delete().where(RecipeSubStepImage.id_step == step.id).execute()
            SubStepImage.delete().where(SubStepImage.id == step_image.id_image).execute()
    SubRecipeStep.delete().where(SubRecipeStep.id_recipe == idrecipe).execute()
    Recipe.delete().where(Recipe.id == idrecipe).execute()
    return jsonify(message="Recipe deleted")

@app.route('/deleteComment', methods=['POST'])
def deleteComment():
    data = request.get_json()
    idcomment = data.get('idcomment')
    DislikeComment.delete().where(DislikeComment.id_comment== idcomment).execute()
    LikesComment.delete().where(LikesComment.id_comment== idcomment).execute()
    RecipeSubComment.delete().where(RecipeSubComment.id_comment == idcomment).execute()
    RecipeComment.delete().where(RecipeComment.id == idcomment).execute()
    return jsonify(message="Recipe deleted")

@app.route('/deleteSubComment', methods=['POST'])
def deleteSubComment():
    data = request.get_json()
    idcomment = data.get('idcomment')
    RecipeSubComment.delete().where(RecipeSubComment.id_comment == idcomment).execute()
    return jsonify(message="Recipe deleted")

@app.route('/editeComment', methods=['POST'])
def editeComment():
    data = request.get_json()
    comment = data.get('comment')
    idcomment = data.get('idcomment')
    RecipeComment.update(comment_text=comment,modified_at=date.today()).where(RecipeComment.id == idcomment).execute()
    return jsonify(message="Change Comment")

@app.route('/editeSubComment', methods=['POST'])
def editeSubComment():
    data = request.get_json()
    comment = data.get('comment')
    idcomment = data.get('idcomment')
    RecipeSubComment.update(comment_text=comment,modified_at=date.today()).where(RecipeSubComment.id_comment == idcomment).execute()
    return jsonify(message="Change Comment")

@app.route('/viewFavs', methods=['POST'])
def viewFavs():
    data = request.get_json()
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        favorites = UserFavorite.select(UserFavorite.id_recipe).where(UserFavorite.id_user == user_id).execute()
        favorites_list = [favorite.id_recipe for favorite in favorites]
        recipes = Recipe.select().where(Recipe.id.in_(favorites_list) & (Recipe.recipe_visibility == 1))
        recipes_list = [{
            "id": recipe.id,
            "title": recipe.recipe_title,
            "image": recipe.recipe_image,
            "description": recipe.recipe_description
        } for recipe in recipes]
        reviews = RecipeReview.select().where(
            (RecipeReview.id_user_id == user_id) &
            (RecipeReview.id_recipe_id.in_(favorites_list))
        )
        reviews_list = [{
            "id_recipe": review.id_recipe_id,
            "review": review.recipe_review_item_value
        } for review in reviews]
        categories_list = []
        for recipe in recipes:
            categories = RecipeFilter.select().where(RecipeFilter.id_recipe == recipe.id)
            for categorie in categories:
                categories_list.append({
                    "recipe_id": recipe.id,
                    "type": categorie.type,
                    "category": categorie.category
                })
        return jsonify(favorites_list=recipes_list, reviews_list=reviews_list,categories_list=categories_list)

@app.route('/viewProfile',methods=['POST'])
def viewProfile():
    data = request.get_json()
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        users = Users.select(Users.user_name,Users.user_email, Users.user_image ).where(Users.id == user_id).execute()
        users_list = [{"name":user.user_name, "email":user.user_email, "image":user.user_image} for user in users]
        return jsonify(message=users_list,type=user.user_type)

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
    subingredients = data.get("subingredients") or []
    subquantities = data.get("subquantities") or []
    substeps = data.get("substeps") or []
    token = data.get("token")
    proteins = data.get("proteins")
    typeeat = data.get("typeeat")
    ccaa = data.get("ccaa")
    time = data.get("time")
    visibility = data.get("visibility")
    
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
    recipe.recipe_visibility = visibility
    recipe.recipe_image = image_url if image_url else recipe.recipe_image  
    recipe.recipe_video = video_url if video_url else recipe.recipe_video  
    recipe.modified_at = date.today()
    recipe.save()
    RecipeFilter.delete().where(RecipeFilter.id_recipe_id == recipe.id).execute()
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe_id == recipe.id).execute()
    SubRecipeIngredient.delete().where(SubRecipeIngredient.id_recipe_id == recipe.id).execute()
    
    RecipeStepImage.delete().where(RecipeStepImage.id_step.in_(
        RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id)
    )).execute()
    RecipeSubStepImage.delete().where(RecipeSubStepImage.id_step.in_(
        SubRecipeStep.select(SubRecipeStep.id).where(SubRecipeStep.id_recipe == recipe.id)
    )).execute()

    StepImage.delete().where(StepImage.id.in_(
        RecipeStepImage.select(RecipeStepImage.id_image).where(
            RecipeStepImage.id_step.in_(RecipeStep.select(RecipeStep.id).where(RecipeStep.id_recipe == recipe.id))
        )
    )).execute()
    SubStepImage.delete().where(SubStepImage.id.in_(
        RecipeSubStepImage.select(RecipeSubStepImage.id_image).where(
            RecipeSubStepImage.id_step.in_(SubRecipeStep.select(SubRecipeStep.id).where(SubRecipeStep.id_recipe == recipe.id))
        )
    )).execute()

    RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()
    SubRecipeStep.delete().where(SubRecipeStep.id_recipe == recipe.id).execute()

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
           
    for i in range(len(subingredients)):
        quantity = subquantities[i] if i < len(subquantities) else ''
        SubRecipeIngredient.create(
            id_recipe_id=recipe.id,
            id_user_id=user.id,
            ingredients_text=subingredients[i],
            quantity_unit=quantity,
            created_at=date.today(),
            modified_at=date.today()
        ) 
    for step in substeps:
        step_title = step.get('title')
        step_text = step.get('description')
        step_image = step.get('image')

        step_image_url = None
        if step_image and isinstance(step_image, dict):
            if "base64" in step_image and step_image["base64"]:
                step_image_url = save_base64_file(step_image['base64'], step_image['name'], app.config['UPLOAD_FOLDER_IMAGES'])
            else:
                step_image_url = step_image.get("name")

        recipe_step = SubRecipeStep.create(
            id_recipe=recipe.id,
            id_user_id=user.id,
            step_title=step_title,
            step_description=step_text,
            created_at=date.today(),
            modified_at=date.today()
        )
        if step_image_url:
            step_img = SubStepImage.create(
                id_user_id=user.id,
                step_image=step_image_url,
                created_at=date.today(),
                modified_at=date.today()
            )

            RecipeSubStepImage.create(
                id_step=recipe_step.id,
                id_image=step_img.id
            )
    if typeeat:
        filters = RecipeFilter(id_recipe_id=recipe.id,type=typeeat,category="typeeat",created_at = date.today(), modified_at = date.today())
        filters.save()
    if ccaa:
        filters = RecipeFilter(id_recipe_id=recipe.id,type=ccaa,category="ccaa",created_at = date.today(), modified_at = date.today())
        filters.save()
    if time:
        filters = RecipeFilter(id_recipe_id=recipe.id,type=time,category="time",created_at = date.today(), modified_at = date.today())
        filters.save()
    for protein in proteins:
        filters = RecipeFilter(id_recipe_id=recipe.id,type=protein,category="protein",created_at = date.today(), modified_at = date.today())
        filters.save()
    return jsonify(message="Receta actualizada correctamente")

@app.route('/changeImage',methods=['POST'])
def changeImage():
    data = request.get_json()
    iduser = data.get("iduser")
    image = data.get("image")
    image_url = None
    if image:  
        image_base64 = image.get("base64")
        image_name = image.get("name")
        
        if image_base64:
            image_url = save_base64_file(image_base64, image_name, app.config['UPLOAD_FOLDER_IMAGES'])
            if image_url:
                Users.update(user_image=image_url,modified_at=date.today()).where(Users.id == iduser).execute()
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
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        Users.update(user_name=name,modified_at=date.today()).where(Users.id == user_id).execute()
        return jsonify(message=name)
    
@app.route('/changeEmail',methods=['POST'])
def changeEmail():
    data = request.get_json()
    email = data.get("email")
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        Users.update(user_email=email,modified_at=date.today()).where(Users.id == user_id).execute()
        token = create_access_token(identity=email)
        user = Users.select(Users.id).where((Users.user_email == email)).get() 
        Users.update(user_token=token,modified_at=date.today()).where(Users.id == user.id).execute()
        return jsonify(message=email,userToken=token)

@app.route('/filterRecipe', methods=['POST'])
def filterRecipe():
    data = request.get_json()
    typeeat = data.get("typeeat")
    ccaa = data.get("ccaa")
    time = data.get("time")
    proteins = data.get("proteins", [])
    
    query = RecipeFilter.select(RecipeFilter.id_recipe_id)
    
    if typeeat:
        query = query.where(
            RecipeFilter.id_recipe_id.in_(
                RecipeFilter.select(RecipeFilter.id_recipe_id)
                .where((RecipeFilter.category == 'typeeat') & (RecipeFilter.type == typeeat))
            )
        )
    
    if ccaa:
        query = query.where(
            RecipeFilter.id_recipe_id.in_(
                RecipeFilter.select(RecipeFilter.id_recipe_id)
                .where((RecipeFilter.category == 'ccaa') & (RecipeFilter.type == ccaa))
            )
        )
    
    if time:
        query = query.where(
            RecipeFilter.id_recipe_id.in_(
                RecipeFilter.select(RecipeFilter.id_recipe_id)
                .where((RecipeFilter.category == 'time') & (RecipeFilter.type == time))
            )
        )
    
    if proteins:
        query = query.where(
            RecipeFilter.id_recipe_id.in_(
                RecipeFilter.select(RecipeFilter.id_recipe_id)
                .where((RecipeFilter.category == 'protein') & (RecipeFilter.type.in_(proteins)))
            )
        )
    
    query = query.group_by(RecipeFilter.id_recipe_id)

    active_filters = sum([1 for f in [typeeat, ccaa, time, proteins] if f])
    
    if active_filters > 0:
        query = query.having(fn.COUNT(RecipeFilter.id_recipe_id) >= active_filters)

    recipe_ids = [r.id_recipe_id for r in query.distinct()]
    
    return jsonify(message=[{"idrecipe": id_} for id_ in recipe_ids])

@app.route('/recipeFilter', methods=['POST'])
def recipeFilter():
    data = request.get_json()
    filtered = data.get("filtered")
    
    idrecipes = [item["idrecipe"] for item in filtered]
    filtereds = Recipe.select().where((Recipe.id.in_(idrecipes))& (Recipe.recipe_visibility==1)).execute()
    filtered_recipes = [{"id": recipe.id, "title": recipe.recipe_title,"image":recipe.recipe_image, "description":recipe.recipe_description, "video":recipe.recipe_video} for recipe in filtereds]
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        favorites = UserFavorite.select().where(UserFavorite.id_user_id ==user_id)
        favorites_list = [{"id_recipe": favorite.id_recipe_id} for favorite in favorites]
        reviews = RecipeReview.select().where(RecipeReview.id_user_id ==user_id)
        reviews_list = [{"id_recipe": review.id_recipe_id, "review": review.recipe_review_item_value} for review in reviews]
        return jsonify(filtered_recipes=filtered_recipes, favorites_list=favorites_list, reviews_list=reviews_list)
    return jsonify(filtered_recipes=filtered_recipes)

@app.route('/changePassword', methods=['POST'])
def changePassword():
    data = request.get_json()
    newPassword = data.get("newPassword")
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()
    if user:
        user_id = user.id
        Users.update(user_password=hashlib.sha256(newPassword.encode('utf-8')).hexdigest(),modified_at=date.today()).where(Users.id == user_id).execute()
        return jsonify(message="Contraseña Actualizada")

@app.route('/deleteProfile', methods=['POST'])
def deleteProfile():
    data = request.get_json()
    token = data.get("userToken")
    user = Users.select().where(Users.user_token == token).first()

    if not user:
        return jsonify(message="Usuario no encontrado"), 404

    user_id = user.id
    idRecipes = Recipe.select().where(Recipe.id_user == user_id)

    for recipe in idRecipes:
        # Eliminar imágenes de pasos
        steps = RecipeStep.select().where(RecipeStep.id_recipe == recipe.id)
        for step in steps:
            RecipeStepImage.delete().where(RecipeStepImage.id_step == step.id).execute()
        RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()
        # Eliminar imágenes de los subpasos
        subSteps = SubRecipeStep.select().where(SubRecipeStep.id_recipe == recipe.id)
        for subStep in subSteps:
            SubStepImage.delete().where(SubStepImage.id_step == subStep.id).execute()
        SubRecipeStep.delete().where(SubRecipeStep.id_recipe == recipe.id).execute()
        # Eliminar filtros, ingredientes y reviews
        RecipeFilter.delete().where(RecipeFilter.id_recipe == recipe.id).execute()
        RecipeIngredient.delete().where(RecipeIngredient.id_recipe == recipe.id).execute()
        
        RecipeReview.delete().where(RecipeReview.id_recipe == recipe.id).execute()

        # Eliminar comentarios secundarios y likes/dislikes de cada comentario
        comments = RecipeComment.select().where(RecipeComment.id_recipe == recipe.id)
        for comment in comments:
            LikesComment.delete().where(LikesComment.id_comment_id == comment.id).execute()
            DislikeComment.delete().where(DislikeComment.id_comment_id == comment.id).execute()
            RecipeSubComment.delete().where(RecipeSubComment.id_comment == comment.id).execute()

        RecipeComment.delete().where(RecipeComment.id_recipe == recipe.id).execute()

    # Eliminar imágenes subidas por el usuario
    StepImage.delete().where(StepImage.id_user == user_id).execute()

    # Eliminar favoritos del usuario
    UserFavorite.delete().where(UserFavorite.id_user == user_id).execute()

    # Eliminar recetas y el perfil
    Recipe.delete().where(Recipe.id_user == user_id).execute()
    Users.delete().where(Users.id == user_id).execute()

    return jsonify(message="Perfil eliminado correctamente")

@app.route('/allUsers', methods=['POST'])
def allUsers():
    data = request.get_json()
    token = data.get("userToken")
    user = Users.select().where((Users.user_token == token) & (Users.user_type == "admin")).first()
    type = "admin"
    if user:
        if Users.select().where((Users.user_token == token) & (Users.user_type == "admin")):
            users = Users.select().where(Users.user_type != type)
            users_list = [{"iduser":user.id,"name":user.user_name,"email":user.user_email}for user in users]
            return jsonify(users_list=users_list)
        return jsonify(users_list=[])

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    data = request.get_json()
    iduser = data.get('iduser')
    userToken = data.get('userToken')
    if Users.select().where((Users.user_token == userToken) & (Users.user_type=="admin")):
        idRecipes = Recipe.select().where(Recipe.id_user == iduser)
        for recipe in idRecipes:
            steps = RecipeStep.select().where(RecipeStep.id_recipe == recipe.id)
            substeps = SubRecipeStep.select().where(SubRecipeStep.id_recipe == recipe.id)
            for step in steps:
                RecipeStepImage.delete().where(RecipeStepImage.id_step == step.id).execute()
            for step in substeps:
                RecipeSubStepImage.delete().where(RecipeSubStepImage.id_step == step.id).execute()
            RecipeFilter.delete().where(RecipeFilter.id_recipe == recipe.id).execute()
            RecipeIngredient.delete().where(RecipeIngredient.id_recipe == recipe.id).execute()
            SubRecipeIngredient.delete().where(SubRecipeIngredient.id_recipe == recipe.id).execute()
            RecipeComment.delete().where(RecipeComment.id_recipe == recipe.id).execute()
            RecipeStep.delete().where(RecipeStep.id_recipe == recipe.id).execute()
            RecipeReview.delete().where(RecipeReview.id_recipe == recipe.id).execute()
            SubStepImage.delete().where(SubStepImage.id_user == iduser).execute()
            StepImage.delete().where(StepImage.id_user == iduser).execute()
            UserFavorite.delete().where(UserFavorite.id_user == iduser).execute()

        Recipe.delete().where(Recipe.id_user == iduser).execute()
        Users.delete().where(Users.id == iduser).execute()    
        return jsonify(message="Perfil eliminado")

@app.route('/averageStars', methods=["POST"])
def averageStars():
    try:
        query = (RecipeReview
                 .select(RecipeReview.id_recipe_id, fn.AVG(RecipeReview.recipe_review_item_value).alias('average_rating'))
                 .group_by(RecipeReview.id_recipe_id))

        result = []
        for item in query:
            average_rating = item.average_rating if item.average_rating is not None else 0
            result.append({
                'recipe_id': item.id_recipe_id, 
                'average_rating': round(average_rating, 2) 
            })

        return jsonify(media=result)

    except Exception as e:
        return jsonify(message="Error: " + str(e)), 500

@app.route('/report-recipe', methods=['POST'])
def report_recipe():
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        required_fields = ['idrecipe', 'reason', 'usertoken']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Get data from request
        recipe_id = data['idrecipe']
        reason = data['reason']
        user_token = data['usertoken']
        
        # Validate recipe exists
        try:
            recipe = Recipe.get_by_id(recipe_id)
            recipe_owner = Users.get_by_id(recipe.id_user_id)
        except DoesNotExist:
            return jsonify({"error": "Recipe not found"}), 404
            
        # Validate reporting user exists
        try:
            reporting_user = Users.get(Users.user_token == user_token)
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404

        # Prepare email
        msg = Message(
            subject=f"🚨 Reporte de Receta #{recipe_id} - {recipe.recipe_title}",
            recipients=['Calvopika@gmail.com'],  # Your admin email
            html=render_template(
                'report_email.html',
                recipe=recipe,
                recipe_id=recipe_id,
                reason=reason,
                reporting_user=reporting_user,
                recipe_owner=recipe_owner,
                report_date=date.today().strftime('%d/%m/%Y')
            )
        )

        # Send email with error handling
        try:
            mail.send(msg)
            return jsonify({
                "message": "Report sent successfully",
                "details": {
                    "recipe_id": recipe_id,
                    "reported_by": reporting_user.user_email
                }
            }), 200
        except Exception as e:
            app.logger.error(f"Failed to send report email: {str(e)}")
            return jsonify({
                "error": "Failed to send report email",
                "details": str(e)
            }), 500

    except Exception as e:
        app.logger.error(f"Error in report-recipe: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500
    
@app.route('/report-comment', methods=['POST'])
def report_comment():
    try:
        data = request.get_json()
        required_fields = ['commentId', 'reason', 'userToken']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Get data from request
        comment_id = data['commentId']
        reason = data['reason']
        user_token = data['userToken']
        
        # Validate comment exists
        try:
            comment = RecipeComment.get_by_id(comment_id)
            recipe = Recipe.get_by_id(comment.id_recipe_id)
            comment_author = Users.get_by_id(comment.id_user_id)
        except DoesNotExist:
            try:
                comment = RecipeSubComment.get_by_id(comment_id)
                recipe = Recipe.get_by_id(comment.id_recipe_id)
                comment_author = Users.get_by_id(comment.id_user_id)
            except DoesNotExist:
                return jsonify({"error": "Comment not found"}), 404
            
        # Validate reporting user exists
        try:
            reporting_user = Users.get(Users.user_token == user_token)
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404

        # Prepare email
        msg = Message(
            subject=f"🚨 Reporte de Comentario #{comment_id}",
            recipients=['Calvopika@gmail.com'],  # Your admin email
            html=render_template(
                'comment_report_email.html',
                comment=comment,
                comment_id=comment_id,
                reason=reason,
                reporting_user=reporting_user,
                comment_author=comment_author,
                recipe=recipe,
                report_date=date.today().strftime('%d/%m/%Y')
            )
        )

        # Send email
        try:
            mail.send(msg)
            return jsonify({
                "message": "Comment report sent successfully",
                "details": {
                    "comment_id": comment_id,
                    "reported_by": reporting_user.user_email
                }
            }), 200
        except Exception as e:
            app.logger.error(f"Failed to send comment report email: {str(e)}")
            return jsonify({
                "error": "Failed to send report email",
                "details": str(e)
            }), 500

    except Exception as e:
        app.logger.error(f"Error in report-comment: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500    
    
@app.route('/likeComment', methods=['POST'])
def likeComment():
    data = request.get_json()
    idcomment = data.get("idcomment")
    DislikeComment.delete().where(DislikeComment.id_comment == idcomment).execute()
    
    token = data.get("userToken")
    users = Users.select().where((Users.user_token == token)).first()
    iduser = users.id
    idrecipe = data.get('idrecipe')
    user = LikesComment(id_comment = idcomment,id_user = iduser, id_recipe = idrecipe,created_at = date.today(), modified_at = date.today())
    user.save()
    return '', 204 

@app.route('/disLikeComment', methods=['POST'])
def disLikeComment():
    data = request.get_json()
    idcomment = data.get("idcomment")
    LikesComment.delete().where(LikesComment.id_comment == idcomment).execute()
    
    token = data.get("userToken")
    users = Users.select().where((Users.user_token == token)).first()
    iduser = users.id
    idrecipe = data.get('idrecipe')
    user = DislikeComment(id_comment = idcomment,id_user = iduser, id_recipe = idrecipe,created_at = date.today(), modified_at = date.today())
    user.save()
    return '', 204 

@app.route('/deleteLike', methods=['POST'])
def deleteLike():
    data = request.get_json()
    idcomment = data.get("idcomment")
    LikesComment.delete().where(LikesComment.id_comment == idcomment).execute()
    return '', 204 

@app.route('/deleteDisLike', methods=['POST'])
def deleteDisLike():
    data = request.get_json()
    idcomment = data.get("idcomment")
    DislikeComment.delete().where(DislikeComment.id_comment == idcomment).execute()
    return '', 204 

@app.route('/send-email', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        msg = Message(
            subject=f"Nuevo mensaje de contacto de {name}",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}"
        )
        mail.send(msg)
        return jsonify({"message": "Correo enviado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

