from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import create_tables,Users, Recipe, RecipeComment, RecipeReview, UserFavorite, RecipeIngredient, StepImage, RecipeStep, RecipeStepImage
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
    file_data = base64.b64decode(base64_data.split(',')[1])
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'wb') as file:
        file.write(file_data)
    return file_path

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
    if video:  # Si el video está presente en base64
        video_url = save_base64_file(video['base64'], video['name'], app.config['UPLOAD_FOLDER_VIDEOS'])
    description = data.get("description")
    ingredients = data.get("ingredients")
    quantities = data.get("quantities")
    if not quantities:
        quantities = []
    if not ingredients:
        ingredients = []
    token = data.get("token")
    if Users.select().where((Users.user_token == token)).exists():
        user = Users.select(Users.id).where((Users.user_token == token)).get()
        recipe = Recipe(recipe_title = title,recipe_image = image_url,recipe_description = description, recipe_video = video_url, id_user_id = user.id, created_at = date.today(), modified_at = date.today())
        recipe.save() 
        for i in range(len(ingredients)):        
            quantity = quantities[i] if i < len(quantities) else ''
            recipe_ingredient = RecipeIngredient(id_recipe_id = recipe.id, id_user_id = user.id,ingredients_text=ingredients[i],quantity_unit=quantity, created_at = date.today(), modified_at = date.today())
            recipe_ingredient.save()
        
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
    if iduser:
        favorites = UserFavorite.select().where(UserFavorite.id_user_id ==iduser)
        favorites_list = [{"id_recipe": favorite.id_recipe_id} for favorite in favorites]
        return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list,favorites_list=favorites_list)
    return jsonify(recipe_list=recipe_list, ingredient_list=ingredient_list)

@app.route('/viewComment', methods=['POST'])
def viewComment(): 
    data = request.get_json()
    idrecipe = data.get("idrecipe") 
    comments = RecipeComment.select().where(RecipeComment.id_recipe_id ==idrecipe)
    comment_list = [{"id":comment.id,"comment":comment.comment_text,"iduser":comment.id_user_id} for comment in comments]
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
    RecipeIngredient.delete().where(RecipeIngredient.id_recipe == idrecipe).execute()
    RecipeComment.delete().where(RecipeComment.id_recipe == idrecipe).execute()
    UserFavorite.delete().where(UserFavorite.id_recipe == idrecipe).execute()
    RecipeReview.delete().where(RecipeReview.id_recipe == idrecipe).execute()
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
    return jsonify(message="a")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


"""
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL,
    user_token VARCHAR(255) NOT NULL,
    user_image VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL
);

CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_title VARCHAR(255) NOT NULL,
    recipe_description TEXT NOT NULL,
    recipe_video VARCHAR(255) DEFAULT NULL,
    id_user INT NOT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE recipe_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment_text TEXT NOT NULL,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_recipe) REFERENCES recipe(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE recipe_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL,
    recipe_review_item_value INT NOT NULL CHECK (recipe_review_item_value BETWEEN 1 AND 5),
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_recipe) REFERENCES recipe(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE user_favorite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_recipe) REFERENCES recipe(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE recipe_ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL,
    ingredients_text TEXT DEFAULT NULL,
    quantities_num INT DEFAULT NULL,
    quantity_unit VARCHAR(50) DEFAULT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_recipe) REFERENCES recipe(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE steps_image (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    image VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE recipe_steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL,
    step_description TEXT NOT NULL,  -- Descripción del paso
    created_at DATETIME NOT NULL,
    modified_at DATETIME NOT NULL,
    FOREIGN KEY (id_recipe) REFERENCES recipe(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE recipe_step_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_step INT NOT NULL,
    id_image INT NOT NULL,
    FOREIGN KEY (id_step) REFERENCES recipe_steps(id),
    FOREIGN KEY (id_image) REFERENCES steps_image(id)
);


"""
