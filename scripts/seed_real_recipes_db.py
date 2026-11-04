"""Seed directo a Postgres/SQLite (sin API): URLs Wikimedia/YouTube + comentarios.

Carga `.env` si existe (DATABASE_URL). Uso:
  python scripts/seed_real_recipes_db.py
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Cargar .env sin imprimir secretos
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)

import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "seed_real_recipes",
    Path(__file__).with_name("seed_real_recipes.py"),
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_mod)
AUTHORS = _mod.AUTHORS
COMMENTERS = _mod.COMMENTERS
PASS = _mod.PASS
RECIPES = _mod.RECIPES

from app.db import db  # noqa: E402
from app.models import (  # noqa: E402
    Recipe,
    RecipeComment,
    RecipeFilter,
    RecipeIngredient,
    RecipeStep,
    RecipeStepImage,
    StepImage,
    Users,
    create_tables,
)
from app.security import hash_password  # noqa: E402


def ensure_user(name: str, email: str) -> Users:
    user = Users.get_or_none(Users.user_email == email)
    if user:
        return user
    user = Users.create(
        user_name=name,
        user_email=email,
        user_password=hash_password(PASS),
        user_type="user",
        user_token="",
        user_image="/static/images/NonPerfil.webp",
        created_at=date.today(),
        modified_at=date.today(),
    )
    return user


def ensure_recipe(author: Users, key: str, data: dict) -> Recipe:
    existing = (
        Recipe.select()
        .where(
            (Recipe.id_user == author.id)
            & (Recipe.recipe_title == data["title"])
        )
        .first()
    )
    if existing:
        print(f"  ya existe id={existing.id}")
        return existing

    with db.atomic():
        recipe = Recipe.create(
            recipe_title=data["title"],
            recipe_visibility=True,
            recipe_image=data.get("image"),
            recipe_description=data.get("description"),
            recipe_video=data.get("video"),
            id_user=author.id,
            created_at=date.today(),
            modified_at=date.today(),
        )
        for name, qty in data.get("ingredients") or []:
            RecipeIngredient.create(
                id_recipe=recipe.id,
                id_user=author.id,
                ingredients_text=name,
                quantity_unit=(qty or "")[:50],
                created_at=date.today(),
                modified_at=date.today(),
            )
        for step in data.get("steps") or []:
            rs = RecipeStep.create(
                id_recipe=recipe.id,
                id_user=author.id,
                step_title=step["title"],
                step_description=step.get("description") or "",
                created_at=date.today(),
                modified_at=date.today(),
            )
            if step.get("image"):
                img = StepImage.create(
                    id_user=author.id,
                    step_image=step["image"],
                    created_at=date.today(),
                    modified_at=date.today(),
                )
                RecipeStepImage.create(id_step=rs.id, id_image=img.id)

        mapping = [
            (data.get("typeeat"), "typeeat"),
            (data.get("ccaa"), "ccaa"),
            (data.get("time"), "time"),
        ]
        for value, category in mapping:
            if value:
                RecipeFilter.create(
                    id_recipe=recipe.id,
                    type=value,
                    category=category,
                    created_at=date.today(),
                    modified_at=date.today(),
                )
        for protein in data.get("proteins") or []:
            RecipeFilter.create(
                id_recipe=recipe.id,
                type=protein,
                category="protein",
                created_at=date.today(),
                modified_at=date.today(),
            )

    print(f"  creada id={recipe.id}" + (" +youtube" if data.get("video") else ""))
    return recipe


def ensure_comments(recipe: Recipe, users_by_email: dict[str, Users], threads):
    for email, text in threads:
        user = users_by_email.get(email)
        if not user:
            continue
        exists = (
            RecipeComment.select()
            .where(
                (RecipeComment.id_recipe == recipe.id)
                & (RecipeComment.id_user == user.id)
                & (RecipeComment.comment_text == text)
            )
            .exists()
        )
        if exists:
            continue
        RecipeComment.create(
            comment_text=text,
            id_recipe=recipe.id,
            id_user=user.id,
            created_at=date.today(),
            modified_at=date.today(),
        )
        print(f"  comment ok ({email.split('@')[0]})")


def main() -> int:
    if not os.getenv("DATABASE_URL") and not os.getenv("USE_SQLITE"):
        print("Falta DATABASE_URL en .env (o USE_SQLITE=1)", file=sys.stderr)
        return 1

    db.connect(reuse_if_open=True)
    create_tables()

    users: dict[str, Users] = {}
    for person in AUTHORS + COMMENTERS:
        print(f"user {person['email']}")
        users[person["email"]] = ensure_user(person["name"], person["email"])

    created: dict[str, Recipe] = {}
    for author in AUTHORS:
        for key in author["recipes"]:
            data = RECIPES[key]
            print(f"\n== {data['title']} ==")
            created[key] = ensure_recipe(users[author["email"]], key, data)

    print("\n== comentarios ==")
    for key, recipe in created.items():
        print(f"\n{RECIPES[key]['title']} ({recipe.id})")
        ensure_comments(recipe, users, RECIPES[key].get("comments") or [])

    print("\nDONE")
    print("Password demo:", PASS)
    if not db.is_closed():
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
