"""Ownership, comentarios en privadas, logout/revoke, uploads."""

import base64
import uuid

from app.models import Recipe, RecipeComment, Users
from app.security import hash_password


def _register(client, email=None, password="password123"):
    email = email or f"u-{uuid.uuid4().hex[:8]}@example.com"
    res = client.post(
        "/register",
        json={"name": "User", "email": email, "password": password},
    )
    assert res.status_code == 200
    data = res.get_json()
    return {
        "headers": {"Authorization": f"Bearer {data['userToken']}"},
        "id": data["iduser"],
        "email": email,
        "token": data["userToken"],
    }


def _make_recipe(owner_id, *, visibility=True, title="R"):
    return Recipe.create(
        recipe_title=title,
        recipe_image=None,
        recipe_description="d",
        recipe_visibility=visibility,
        recipe_video=None,
        id_user=owner_id,
    )


def test_delete_recipe_forbidden_for_other_user(client):
    owner = _register(client)
    other = _register(client)
    recipe = _make_recipe(owner["id"])
    res = client.post(
        "/deleteRecipe",
        headers=other["headers"],
        json={"idrecipe": recipe.id},
    )
    assert res.status_code == 403
    assert Recipe.get_or_none(Recipe.id == recipe.id) is not None


def test_delete_recipe_ok_for_owner(client):
    owner = _register(client)
    recipe = _make_recipe(owner["id"])
    res = client.post(
        "/deleteRecipe",
        headers=owner["headers"],
        json={"idrecipe": recipe.id},
    )
    assert res.status_code == 200
    assert Recipe.get_or_none(Recipe.id == recipe.id) is None


def test_private_recipe_comments_hidden(client):
    owner = _register(client)
    stranger = _register(client)
    recipe = _make_recipe(owner["id"], visibility=False)
    RecipeComment.create(
        comment_text="secreto",
        id_recipe=recipe.id,
        id_user=owner["id"],
    )
    denied = client.post(
        "/viewComment",
        headers=stranger["headers"],
        json={"idrecipe": recipe.id},
    )
    assert denied.status_code == 403

    ok = client.post(
        "/viewComment",
        headers=owner["headers"],
        json={"idrecipe": recipe.id},
    )
    assert ok.status_code == 200
    assert len(ok.get_json()["comment_list"]) == 1


def test_logout_revokes_token(client):
    user = _register(client)
    res = client.post("/logout", headers=user["headers"])
    assert res.status_code == 200
    blocked = client.post("/viewProfile", headers=user["headers"], json={})
    assert blocked.status_code == 401


def test_upload_rejects_fake_image(client):
    user = _register(client)
    fake = base64.b64encode(b"not-an-image-content-xxx").decode()
    res = client.post(
        "/changeImage",
        headers=user["headers"],
        json={"image": {"base64": fake, "name": "evil.jpg"}},
    )
    assert res.status_code == 400


def test_edit_recipe_alias_works(client):
    owner = _register(client)
    recipe = _make_recipe(owner["id"], title="Old")
    res = client.post(
        "/editRecipe",
        headers=owner["headers"],
        json={
            "idrecipe": recipe.id,
            "title": "New",
            "description": "d",
            "visibility": True,
            "ingredients": [],
            "quantities": [],
            "steps": [],
            "proteins": [],
        },
    )
    assert res.status_code == 200
    recipe = Recipe.get_by_id(recipe.id)
    assert recipe.recipe_title == "New"
