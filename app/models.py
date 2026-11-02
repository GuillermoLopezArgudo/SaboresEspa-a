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
    user_token = TextField()  # JWT completo (puede superar 512)
    user_image = CharField(max_length=1024)  # Cloudinary URLs
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class Recipe(BaseModel):
    recipe_title = CharField(max_length=255)
    recipe_image = CharField(max_length=1024, null=True)
    recipe_description = TextField(null=True)
    recipe_visibility = BooleanField(default=True)
    recipe_video = CharField(max_length=1024, null=True)
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

    class Meta:
        indexes = ((("id_user", "id_recipe"), True),)


class UserFavorite(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="favorites")
    id_user = ForeignKeyField(Users, backref="favorites")
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = ((("id_user", "id_recipe"), True),)


class RecipeIngredient(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="ingredients")
    id_user = ForeignKeyField(Users, backref="ingredients")
    ingredients_text = TextField(null=True)
    quantity_unit = CharField(max_length=50, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class StepImage(BaseModel):
    id_user = ForeignKeyField(Users, backref="step_images")
    step_image = CharField(max_length=1024)
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


def _widen_url_columns():
    """Amplía columnas de media a 1024 en Postgres si venían de VARCHAR(255)."""
    # Solo Postgres (Neon/Render). SQLite ignora o falla sin impacto.
    try:
        backend = type(db).__name__.lower()
    except Exception:
        return
    if "postgres" not in backend and "postgresql" not in backend:
        return

    alters = [
        'ALTER TABLE "users" ALTER COLUMN "user_image" TYPE VARCHAR(1024)',
        'ALTER TABLE "users" ALTER COLUMN "user_token" TYPE TEXT',
        'ALTER TABLE "recipe" ALTER COLUMN "recipe_image" TYPE VARCHAR(1024)',
        'ALTER TABLE "recipe" ALTER COLUMN "recipe_video" TYPE VARCHAR(1024)',
        'ALTER TABLE "stepimage" ALTER COLUMN "step_image" TYPE VARCHAR(1024)',
    ]
    for sql in alters:
        try:
            db.execute_sql(sql)
        except Exception:
            pass


def _dedupe_user_recipe_rows(model):
    """Elimina duplicados (user, recipe) dejando el id más bajo."""
    seen = set()
    for row in model.select().order_by(model.id):
        key = (row.id_user_id, row.id_recipe_id)
        if key in seen:
            row.delete_instance()
        else:
            seen.add(key)


def _ensure_unique_fav_review_indexes():
    """Dedupe + índice único en favoritos y reviews (SQLite/Postgres)."""
    try:
        _dedupe_user_recipe_rows(UserFavorite)
        _dedupe_user_recipe_rows(RecipeReview)
    except Exception as exc:
        print(f"[warn] dedupe fav/review: {exc}")

    statements = [
        'CREATE UNIQUE INDEX IF NOT EXISTS "uq_userfavorite_user_recipe" '
        'ON "userfavorite" ("id_user_id", "id_recipe_id")',
        'CREATE UNIQUE INDEX IF NOT EXISTS "uq_recipereview_user_recipe" '
        'ON "recipereview" ("id_user_id", "id_recipe_id")',
    ]
    for sql in statements:
        try:
            db.execute_sql(sql)
        except Exception:
            pass


def create_tables():
    with db:
        db.create_tables(ALL_MODELS)
        _widen_url_columns()
        _ensure_unique_fav_review_indexes()
