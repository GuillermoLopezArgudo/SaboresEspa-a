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


class SubRecipe(BaseModel):
    """Subreceta independiente (ej. Alioli, Salsa brava) dentro de una receta."""

    id_recipe = ForeignKeyField(Recipe, backref="sub_recipes")
    id_user = ForeignKeyField(Users, backref="owned_sub_recipes")
    title = CharField(max_length=255)
    sort_order = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class SubRecipeIngredient(BaseModel):
    id_sub_recipe = ForeignKeyField(SubRecipe, backref="ingredients")
    id_user = ForeignKeyField(Users, backref="sub_recipe_ingredients")
    ingredients_text = TextField(null=True)
    quantity_unit = CharField(max_length=50, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class SubRecipeStep(BaseModel):
    id_sub_recipe = ForeignKeyField(SubRecipe, backref="steps")
    id_user = ForeignKeyField(Users, backref="sub_recipe_steps")
    step_title = CharField(max_length=255)
    step_description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class SubStepImage(BaseModel):
    id_user = ForeignKeyField(Users, backref="sub_step_images")
    step_image = CharField(max_length=1024)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField(default=datetime.datetime.now)


class RecipeSubStepImage(BaseModel):
    id_step = ForeignKeyField(SubRecipeStep, backref="step_images")
    id_image = ForeignKeyField(SubStepImage, backref="step_links")


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
    SubRecipe,
    SubRecipeIngredient,
    SubRecipeStep,
    SubStepImage,
    RecipeSubStepImage,
]


def _is_postgres() -> bool:
    try:
        return "postgres" in type(db).__name__.lower()
    except Exception:
        return False


def _pg_exec(sql: str) -> None:
    """Ejecuta SQL y hace rollback si falla (Postgres aborta toda la tx tras un error)."""
    try:
        db.execute_sql(sql)
    except Exception as exc:
        print(f"[warn] migration SQL failed: {exc}")
        try:
            db.rollback()
        except Exception:
            pass


def _widen_url_columns():
    """Amplía columnas de media a 1024 en Postgres si venían de VARCHAR(255)."""
    if not _is_postgres():
        return

    alters = [
        'ALTER TABLE "users" ALTER COLUMN "user_image" TYPE VARCHAR(1024)',
        'ALTER TABLE "users" ALTER COLUMN "user_token" TYPE TEXT',
        'ALTER TABLE "recipe" ALTER COLUMN "recipe_image" TYPE VARCHAR(1024)',
        'ALTER TABLE "recipe" ALTER COLUMN "recipe_video" TYPE VARCHAR(1024)',
        'ALTER TABLE "stepimage" ALTER COLUMN "step_image" TYPE VARCHAR(1024)',
        'ALTER TABLE "substepimage" ALTER COLUMN "step_image" TYPE VARCHAR(1024)',
    ]
    for sql in alters:
        _pg_exec(sql)


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
        try:
            db.rollback()
        except Exception:
            pass

    fav = UserFavorite._meta.table_name
    rev = RecipeReview._meta.table_name
    statements = [
        f'CREATE UNIQUE INDEX IF NOT EXISTS "uq_userfavorite_user_recipe" '
        f'ON "{fav}" ("id_user_id", "id_recipe_id")',
        f'CREATE UNIQUE INDEX IF NOT EXISTS "uq_recipereview_user_recipe" '
        f'ON "{rev}" ("id_user_id", "id_recipe_id")',
    ]
    for sql in statements:
        _pg_exec(sql)


def _migrate_named_subrecipes():
    """Si quedaron tablas planas (id_recipe), las recrea con SubRecipe nombrada."""
    try:
        cols = [row[1] for row in db.execute_sql("PRAGMA table_info(subrecipeingredient)")]
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
        # Postgres u otra BD sin esa tabla aún
        try:
            rows = list(
                db.execute_sql(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_name = 'subrecipeingredient'"
                )
            )
            cols = [r[0] for r in rows]
        except Exception:
            try:
                db.rollback()
            except Exception:
                pass
            return

    if not cols:
        return
    # Esquema nuevo ya ok
    if "id_sub_recipe_id" in cols or "id_sub_recipe" in cols:
        return
    # Esquema viejo plano → recrear tablas de subreceta
    if "id_recipe_id" in cols or "id_recipe" in cols:
        print("[migrate] recreating named subrecipe tables")
        try:
            db.drop_tables(
                [
                    RecipeSubStepImage,
                    SubRecipeIngredient,
                    SubRecipeStep,
                    SubStepImage,
                    SubRecipe,
                ],
                safe=True,
            )
        except Exception as exc:
            print(f"[warn] drop old subrecipe tables: {exc}")
            try:
                db.rollback()
            except Exception:
                pass
        db.create_tables(
            [
                SubRecipe,
                SubRecipeIngredient,
                SubRecipeStep,
                SubStepImage,
                RecipeSubStepImage,
            ]
        )


def create_tables():
    # Cada paso aislado: un fallo de migración no debe dejar la conexión en estado aborted
    db.connect(reuse_if_open=True)
    try:
        db.create_tables(ALL_MODELS)
        _migrate_named_subrecipes()
        _widen_url_columns()
        _ensure_unique_fav_review_indexes()
    finally:
        if not db.is_closed():
            db.close()


def ping_database() -> tuple[bool, str]:
    """Comprueba SELECT 1. Devuelve (ok, motivo_corto)."""
    try:
        if db.is_closed():
            db.connect(reuse_if_open=True)
        db.execute_sql("SELECT 1")
        return True, "ok"
    except Exception as exc:
        try:
            db.close()
        except Exception:
            pass
        try:
            db.connect()
            db.execute_sql("SELECT 1")
            return True, "ok-reconnect"
        except Exception as exc2:
            msg = str(exc2 or exc)
            # Sin secretos: solo tipo de error
            short = msg.split("\n")[0][:160]
            return False, short or "db-error"
