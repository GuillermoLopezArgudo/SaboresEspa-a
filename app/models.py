import datetime

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

from app.db import db


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_name = CharField(max_length=255)
    user_email = CharField(max_length=255, unique=True)
    user_password = CharField(max_length=255)
    user_type = CharField(max_length=50)
    user_token = CharField(max_length=512)
    user_image = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class Recipe(BaseModel):
    recipe_title = CharField(max_length=255)
    recipe_image = CharField(max_length=255, null=True)
    recipe_description = TextField(null=True)
    recipe_visibility = BooleanField(default=True)
    recipe_video = CharField(max_length=255, null=True)
    id_user = ForeignKeyField(Users, backref="recipes")
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeComment(BaseModel):
    comment_text = TextField()
    id_recipe = ForeignKeyField(Recipe, backref="comments")
    id_user = ForeignKeyField(Users, backref="comments")
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeReview(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="reviews")
    id_user = ForeignKeyField(Users, backref="reviews")
    recipe_review_item_value = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class UserFavorite(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="favorites")
    id_user = ForeignKeyField(Users, backref="favorites")
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeIngredient(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="ingredients")
    id_user = ForeignKeyField(Users, backref="ingredients")
    ingredients_text = TextField(null=True)
    quantity_unit = CharField(max_length=50, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class StepImage(BaseModel):
    id_user = ForeignKeyField(Users, backref="step_images")
    step_image = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeStep(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="steps")
    id_user = ForeignKeyField(Users, backref="steps")
    step_title = CharField(max_length=255)
    step_description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeStepImage(BaseModel):
    id_step = ForeignKeyField(RecipeStep, backref="step_images")
    id_image = ForeignKeyField(StepImage, backref="step_images")


class RecipeFilter(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="filters")
    type = CharField(max_length=50)
    category = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


ALL_MODELS = [
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
]


def create_tables():
    with db:
        db.create_tables(ALL_MODELS)
