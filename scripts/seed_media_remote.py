"""Añade imagen principal, vídeo e imágenes de pasos a las recetas demo en Render."""
from __future__ import annotations

import base64
import io
import sys
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

API = "https://sabores-espana-api.onrender.com"
PASS = "DemoPass123"

# Cuentas del seed anterior
ACCOUNTS = {
    "ana.cocina.49665@demo.sabores.es": [1, 2],
    "carlos.chef.49665@demo.sabores.es": [3, 4, 5],
    "lucia.fogones.49665@demo.sabores.es": [6, 7, 8],
}

# Colores por receta (RGB)
COLORS = {
    1: ((245, 180, 70), "Tortilla"),
    2: ((220, 70, 50), "Gazpacho"),
    3: ((90, 140, 200), "Pulpo"),
    4: ((240, 200, 60), "Paella"),
    5: ((250, 220, 120), "Crema"),
    6: ((70, 120, 180), "Bacalao"),
    7: ((230, 120, 50), "Bravas"),
    8: ((200, 60, 50), "Pimientos"),
}

STEP_COLORS = ((180, 100, 60), (120, 150, 80), (90, 110, 160))


def png_b64(color: tuple[int, int, int], label: str, size=(640, 400)) -> dict:
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    # franja inferior
    draw.rectangle([0, size[1] - 70, size[0], size[1]], fill=(30, 20, 10))
    try:
        font = ImageFont.truetype("arial.ttf", 36)
        small = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
        small = font
    draw.text((24, size[1] - 55), label, fill=(255, 255, 255), font=font)
    draw.text((24, 20), "Sabores Espana", fill=(255, 255, 255), font=small)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return {
        "name": f"{label.replace(' ', '_').lower()}.png",
        "base64": base64.b64encode(buf.getvalue()).decode("ascii"),
    }


def ensure_sample_mp4() -> dict | None:
    """Descarga un MP4 corto de ejemplo o usa cache local."""
    cache = Path(__file__).resolve().parent / "_sample.mp4"
    if not cache.exists() or cache.stat().st_size < 1000:
        urls = [
            # clip corto público de pruebas
            "https://filesamples.com/samples/video/mp4/sample_640x360.mp4",
            "https://www.w3schools.com/html/mov_bbb.mp4",
        ]
        for url in urls:
            try:
                print(f"descargando video de {url} ...")
                r = requests.get(url, timeout=120)
                r.raise_for_status()
                if len(r.content) > 1000 and r.content[4:8] == b"ftyp":
                    cache.write_bytes(r.content)
                    break
            except Exception as exc:
                print(f"  fallo: {exc}")
        if not cache.exists():
            return None
    data = cache.read_bytes()
    return {
        "name": "demo.mp4",
        "base64": base64.b64encode(data).decode("ascii"),
    }


def login(email: str) -> str:
    r = requests.post(
        f"{API}/login",
        json={"email": email, "password": PASS},
        timeout=90,
    )
    r.raise_for_status()
    return r.json()["userToken"]


def get_recipe(token: str, recipe_id: int) -> dict:
    # viewRecipe is public for visible recipes; still send auth
    r = requests.post(
        f"{API}/viewRecipe",
        headers={"Authorization": f"Bearer {token}"},
        json={"idrecipe": recipe_id},
        timeout=90,
    )
    r.raise_for_status()
    return r.json()


def update_recipe(token: str, recipe_id: int, video: dict | None) -> None:
    data = get_recipe(token, recipe_id)
    info = data["recipe_list"][0]
    ingredients = [i["ingredients"] for i in data.get("ingredient_list") or []]
    quantities = [i["quantity"] for i in data.get("ingredient_list") or []]

    color, label = COLORS[recipe_id]
    main_img = png_b64(color, label)

    steps_out = []
    for idx, step in enumerate(data.get("step_list") or []):
        sc = STEP_COLORS[idx % len(STEP_COLORS)]
        step_img = png_b64(sc, f"Paso {idx + 1}: {step.get('title') or ''}", size=(480, 300))
        steps_out.append(
            {
                "title": step.get("title") or f"Paso {idx + 1}",
                "description": step.get("description") or "",
                "image": step_img,
            }
        )

    # filtros actuales
    filters = data.get("filters_list") or []
    typeeat = next((f["type"] for f in filters if f["category"] == "typeeat"), "")
    ccaa = next((f["type"] for f in filters if f["category"] == "ccaa"), "")
    time = next((f["type"] for f in filters if f["category"] == "time"), "")
    proteins = [f["type"] for f in filters if f["category"] == "protein"]

    payload = {
        "idrecipe": recipe_id,
        "title": info["title"],
        "description": info.get("description") or "",
        "visibility": bool(info.get("visibility", True)),
        "image": main_img,
        "ingredients": ingredients,
        "quantities": quantities,
        "steps": steps_out,
        "typeeat": typeeat,
        "ccaa": ccaa,
        "time": time,
        "proteins": proteins,
    }
    if video:
        payload["video"] = video

    r = requests.post(
        f"{API}/editRecipe",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=180,
    )
    if r.status_code >= 400:
        print(f"FAIL recipe {recipe_id}: {r.status_code} {r.text[:300]}")
        r.raise_for_status()
    print(f"OK recipe {recipe_id} ({info['title']}) media updated")


def main() -> int:
    video = ensure_sample_mp4()
    if not video:
        print("AVISO: no hay vídeo de muestra; solo imágenes")
    else:
        print(f"video listo ({len(video['base64']) // 1024} KB base64)")

    for email, ids in ACCOUNTS.items():
        print(f"\n== {email} ==")
        token = login(email)
        for rid in ids:
            update_recipe(token, rid, video)
    # verificar
    allr = requests.post(f"{API}/viewAll", json={"all": True}, timeout=90).json()
    for rec in allr.get("recipes_list") or []:
        img = rec.get("image") or ""
        print(f" - {rec['id']}: {rec['title']} | image={img[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
