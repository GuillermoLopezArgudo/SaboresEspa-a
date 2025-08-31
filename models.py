from dotenv import load_dotenv
import os

load_dotenv()
from peewee import *
import datetime
from config import Config  # Importa la configuración
import hashlib
from flask_jwt_extended import create_access_token

# Configura la conexión a la base de datos MySQL usando los valores de Config
db = MySQLDatabase(
    Config.MYSQL_DB, 
    user=Config.MYSQL_USER, 
    password=Config.MYSQL_PASSWORD, 
    host=Config.MYSQL_HOST, 
    port=3306
)

class BaseModel(Model):
    class Meta:
        database = db

# Modelo para la tabla 'users'
class Users(BaseModel):
    user_name = CharField(max_length=255)
    user_email = CharField(max_length=255, unique=True)
    user_password = CharField(max_length=255)
    user_type = CharField(max_length=50)
    user_token = CharField(max_length=512)
    user_image = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.user_name} - {self.user_email}"

# Modelo para la tabla 'recipe'
class Recipe(BaseModel):
    recipe_title = CharField(max_length=255)
    recipe_image = CharField(max_length=255)
    recipe_description = TextField()
    recipe_visibility = BooleanField()
    recipe_video = CharField(max_length=255, null=True)
    id_user = ForeignKeyField(Users, backref='recipes', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.recipe_title

# Modelo para la tabla 'recipe_comment'
class RecipeComment(BaseModel):
    comment_text = TextField()
    id_recipe = ForeignKeyField(Recipe, backref='comments', on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='comments', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Comment by {self.id_user.user_name} on {self.id_recipe.recipe_title}"

# Modelo para la tabla 'recipe_reviews'
class RecipeReview(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='reviews', on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='reviews', on_delete='CASCADE')
    recipe_review_item_value = IntegerField(constraints=[Check('recipe_review_item_value BETWEEN 1 AND 5')])
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Review by {self.id_user.user_name} for {self.id_recipe.recipe_title}"

# Modelo para la tabla 'user_favorite'
class UserFavorite(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='favorites', on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='favorites', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.id_user.user_name} favorite for {self.id_recipe.recipe_title}"

# Modelo para la tabla 'recipe_ingredients'
class RecipeIngredient(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='ingredients', on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='ingredients', on_delete='CASCADE')
    ingredients_text = TextField(null=True)
    quantity_unit = CharField(max_length=50, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Ingredient for {self.id_recipe.recipe_title}"

# Modelo para la tabla 'steps_image'
class StepImage(BaseModel):
    id_user = ForeignKeyField(Users, backref='step_images', on_delete='CASCADE')
    step_image = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Image by {self.id_user.user_name}"

# Modelo para la tabla 'recipe_steps'
class RecipeStep(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='steps', on_delete='CASCADE')    
    id_user = ForeignKeyField(Users, backref='steps', on_delete='CASCADE')
    step_title = CharField(max_length=255)
    step_description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Step for {self.id_recipe.recipe_title}"

# Modelo para la tabla 'recipe_step_images'
class RecipeStepImage(BaseModel):
    id_step = ForeignKeyField(RecipeStep, backref='step_images', on_delete='CASCADE')
    id_image = ForeignKeyField(StepImage, backref='step_images', on_delete='CASCADE')

    def __str__(self):
        return f"Image for step {self.id_step.id} of recipe {self.id_step.id_recipe.recipe_title}"

# Modelo para la tabla 'recipe_filter'
class RecipeFilter(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='filters', on_delete='CASCADE')
    type = CharField(max_length=50)
    category = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Filter '{self.type}' for recipe {self.id_recipe.recipe_title}"

# Modelo para la tabla 'sub_recipe_steps'
class SubRecipeStep(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='steps', on_delete='CASCADE')    
    id_user = ForeignKeyField(Users, backref='steps', on_delete='CASCADE')
    step_title = CharField(max_length=255)
    step_description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

# Modelo para la tabla 'sub_recipe_ingredients'
class SubRecipeIngredient(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref='ingredients', on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='ingredients', on_delete='CASCADE')
    ingredients_text = TextField(null=True)
    quantity_unit = CharField(max_length=50, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)
    
# Modelo para la tabla 'sub_steps_image'
class SubStepImage(BaseModel):
    id_user = ForeignKeyField(Users, backref='step_images', on_delete='CASCADE')
    step_image = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Image by {self.id_user.user_name}"

# Modelo para la tabla 'recipe_sub_step_images'
class RecipeSubStepImage(BaseModel):
    id_step = ForeignKeyField(SubRecipeStep, backref='step_images', on_delete='CASCADE')
    id_image = ForeignKeyField(SubStepImage, backref='step_images', on_delete='CASCADE')

    def __str__(self):
        return f"Image for step {self.id_step.id} of recipe {self.id_step.id_recipe.recipe_title}"

    
# Tabla de likes a comentarios 
class LikesComment(BaseModel):
    id_comment = ForeignKeyField(RecipeComment, backref='likes',on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='liked_comments',on_delete='CASCADE')
    id_recipe = ForeignKeyField(Recipe, backref='comment_likes',on_delete='CASCADE') 
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)
    
# Tabla de dislikes a comentarios 
class DislikeComment(BaseModel):
    id_comment = ForeignKeyField(RecipeComment, backref='dislikes',on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='disliked_comments',on_delete='CASCADE')
    id_recipe = ForeignKeyField(Recipe, backref='comment_dislikes',on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)
    
    
# Tabla de subcomentarios de los comentarios
class RecipeSubComment(BaseModel):
    id_comment = ForeignKeyField(RecipeComment, backref='subcomments',on_delete='CASCADE')
    id_recipe = ForeignKeyField(Recipe, backref='subcomments',on_delete='CASCADE')
    id_user = ForeignKeyField(Users, backref='subcomments',on_delete='CASCADE')
    comment_text = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Subcomment by {self.id_user.user_name} on {self.id_recipe.recipe_title}"

# Para crear las tablas si no existen
def create_tables():
    with db:
        db.create_tables([Users, Recipe, RecipeComment, RecipeReview, UserFavorite, RecipeIngredient, StepImage, RecipeStep, RecipeStepImage, RecipeFilter,SubRecipeStep,SubRecipeIngredient,RecipeSubStepImage,SubStepImage,LikesComment,DislikeComment,RecipeSubComment])
    if not Users.select().where(Users.user_email == os.getenv("MAIL_ADMIN")).exists():
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("MAIL_ADMIN")
        token = create_access_token(identity=email)
        Users.create(
            user_name="admin",
            user_email=email,
            user_password=hashlib.sha256(password.encode('utf-8')).hexdigest(),
            user_type="admin",
            user_token=token,
            user_image="/static/images/NonPerfil.webp"
        )

if __name__ == '__main__':
    create_tables()
