from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import Users, Recipe, RecipeComment, RecipeReview, UserFavorite, RecipeIngredient, StepImage, RecipeStep, RecipeStepImage
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import Config
from peewee import DoesNotExist
import datetime


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)
mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    users_ids = []
    for user in Users.select():
        users_ids.append(user.id)
    return jsonify(message=users_ids)
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
