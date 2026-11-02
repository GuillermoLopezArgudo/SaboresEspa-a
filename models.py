import datetime

# PyMySQL como drop-in de MySQLdb (local/docker, sin compilar mysqlclient)
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from peewee import (
    Model,
    CharField,
    TextField,
    BooleanField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    MySQLDatabase,
    PostgresqlDatabase,
)

from config import Config, _parse_database_url


def _build_db():
    if Config.DATABASE_URL:
        info = _parse_database_url(Config.DATABASE_URL)
        kwargs = {}
        if info.get("sslmode"):
            kwargs["sslmode"] = info["sslmode"]
        return PostgresqlDatabase(
            info["name"],
            user=info["user"],
            password=info["password"],
            host=info["host"],
            port=info["port"],
            **kwargs,
        )

    return MySQLDatabase(
        Config.MYSQL_DB,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
    )


db = _build_db()


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

    def __str__(self):
        return f"{self.user_name} - {self.user_email}"


class Recipe(BaseModel):
    recipe_title = CharField(max_length=255)
    recipe_image = CharField(max_length=255, null=True)
    recipe_description = TextField(null=True)
    recipe_visibility = BooleanField(default=True)
    recipe_video = CharField(max_length=255, null=True)
    id_user = ForeignKeyField(Users, backref="recipes")
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.recipe_title


class RecipeComment(BaseModel):
    comment_text = TextField()
    id_recipe = ForeignKeyField(Recipe, backref="comments")
    id_user = ForeignKeyField(Users, backref="comments")
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeReview(BaseModel):
    id_recipe = ForeignKeyField(Recipe, backref="reviews")
    id_user = ForeignKeyField(Users, backref="reviews")
    # Sin CHECK SQL: MySQL/Postgres difieren y Peewee ya valida en la app.
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


def create_tables():
    with db:
        db.create_tables(
            [
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
        )


if __name__ == "__main__":
    create_tables()
