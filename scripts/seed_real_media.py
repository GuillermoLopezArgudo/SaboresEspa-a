"""Sube imágenes/vídeos reales a las recetas demo (Unsplash + Pexels → Cloudinary vía API)."""
from __future__ import annotations

import base64
import sys
from pathlib import Path

import requests

API = "https://sabores-espana-api.onrender.com"
PASS = "DemoPass123"
CACHE = Path(__file__).resolve().parent / "_media_cache"
CACHE.mkdir(exist_ok=True)

ACCOUNTS = {
    "ana.cocina.49665@demo.sabores.es": [1, 2],
    "carlos.chef.49665@demo.sabores.es": [3, 4, 5],
    "lucia.fogones.49665@demo.sabores.es": [6, 7, 8],
}

# Fotos reales (Unsplash) + vídeos cortos (Pexels) libres para demo
MEDIA = {
    1: {  # Tortilla
        "image": "https://images.unsplash.com/photo-1604908176997-43116b137a95?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1498654071233-5abbef0b1f51?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/3195394/3195394-sd_640_360_25fps.mp4",
    },
    2: {  # Gazpacho / tomato soup
        "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1568158879083-c42860933ed7?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/4253593/4253593-sd_640_360_30fps.mp4",
    },
    3: {  # Pulpo / seafood
        "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1615141982883-c7adbf2f93c3?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/3571264/3571264-sd_640_360_30fps.mp4",
    },
    4: {  # Paella
        "image": "https://images.unsplash.com/photo-1534080564583-6be25764b25f?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1516684669134-de6f7c973a1f?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1515443961218-a59527a01999?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/3325989/3325989-sd_640_360_24fps.mp4",
    },
    5: {  # Crema / dessert
        "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1563805042-7684c019e1cd?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/3768580/3768580-sd_640_360_24fps.mp4",
    },
    6: {  # Bacalao / fish
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1580959375944-abd7e991f971?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1559847844-5315695dadae?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/3044127/3044127-sd_640_360_30fps.mp4",
    },
    7: {  # Bravas / fries
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1623238913973-21e45cced554?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/4253536/4253536-sd_640_360_30fps.mp4",
    },
    8: {  # Pimientos / peppers salad
        "image": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?auto=format&fit=crop&w=1200&q=80",
        "steps": [
            "https://images.unsplash.com/photo-1592419044706-39796d40f98c?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
        ],
        "video": "https://videos.pexels.com/video-files/3209822/3209822-sd_640_360_25fps.mp4",
    },
}

VIDEO_FALLBACKS = [
    "https://videos.pexels.com/video-files/3571264/3571264-sd_640_360_30fps.mp4",
    "https://videos.pexels.com/video-files/3195394/3195394-sd_640_360_25fps.mp4",
    "https://www.w3schools.com/html/mov_bbb.mp4",
]

IMAGE_FALLBACKS = [
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=900&q=80",
]


def _download(url: str, name: str, max_mb: float = 7.5) -> dict | None:
    path = CACHE / name
    if path.exists() and path.stat().st_size > 2000:
        data = path.read_bytes()
    else:
        try:
            print(f"  DL {url[:85]}...")
            r = requests.get(
                url,
                timeout=120,
                headers={"User-Agent": "Mozilla/5.0 SaboresEspanaSeed/1.0"},
                allow_redirects=True,
            )
            r.raise_for_status()
            data = r.content
            if len(data) < 2000:
                print(f"  too small ({len(data)})")
                return None
            if len(data) > max_mb * 1024 * 1024:
                print(f"  too big ({len(data)})")
                return None
            path.write_bytes(data)
        except Exception as exc:
            print(f"  fail: {exc}")
            return None

    if data.startswith(b"\x89PNG"):
        ext = ".png"
    elif data[:3] == b"\xff\xd8\xff":
        ext = ".jpg"
    elif len(data) > 8 and data[4:8] == b"ftyp":
        ext = ".mp4"
    elif name.endswith(".mp4"):
        ext = ".mp4"
    else:
        ext = ".jpg"

    return {
        "name": f"{Path(name).stem}{ext}",
        "base64": base64.b64encode(data).decode("ascii"),
    }


def fetch_image(url: str, key: str) -> dict:
    media = _download(url, f"{key}.bin")
    if media and not media["name"].endswith(".mp4"):
        return media
    for i, fb in enumerate(IMAGE_FALLBACKS):
        media = _download(fb, f"{key}.fb{i}.bin")
        if media and not media["name"].endswith(".mp4"):
            return media
    raise RuntimeError(f"No image for {key}")


def fetch_video(url: str, key: str) -> dict | None:
    media = _download(url, f"{key}.mp4", max_mb=7.5)
    if media and media["name"].endswith(".mp4"):
        return media
    for i, fb in enumerate(VIDEO_FALLBACKS):
        media = _download(fb, f"{key}.fb{i}.mp4", max_mb=7.5)
        if media and media["name"].endswith(".mp4"):
            return media
    return None


def login(email: str) -> str:
    r = requests.post(f"{API}/login", json={"email": email, "password": PASS}, timeout=90)
    r.raise_for_status()
    return r.json()["userToken"]


def get_recipe(token: str, recipe_id: int) -> dict:
    r = requests.post(
        f"{API}/viewRecipe",
        headers={"Authorization": f"Bearer {token}"},
        json={"idrecipe": recipe_id},
        timeout=90,
    )
    r.raise_for_status()
    return r.json()


def update_recipe(token: str, recipe_id: int) -> None:
    meta = MEDIA[recipe_id]
    data = get_recipe(token, recipe_id)
    info = data["recipe_list"][0]
    ingredients = [i["ingredients"] for i in data.get("ingredient_list") or []]
    quantities = [i["quantity"] for i in data.get("ingredient_list") or []]
    filters = data.get("filters_list") or []
    typeeat = next((f["type"] for f in filters if f["category"] == "typeeat"), "")
    ccaa = next((f["type"] for f in filters if f["category"] == "ccaa"), "")
    time_v = next((f["type"] for f in filters if f["category"] == "time"), "")
    proteins = [f["type"] for f in filters if f["category"] == "protein"]

    print(f"\nRecipe {recipe_id}: {info['title']}")
    main_img = fetch_image(meta["image"], f"r{recipe_id}_main")
    video = fetch_video(meta["video"], f"r{recipe_id}_vid")

    steps_out = []
    existing = data.get("step_list") or []
    for idx, step in enumerate(existing):
        step_url = (
            meta["steps"][idx]
            if idx < len(meta["steps"])
            else IMAGE_FALLBACKS[idx % len(IMAGE_FALLBACKS)]
        )
        step_img = fetch_image(step_url, f"r{recipe_id}_s{idx}")
        steps_out.append(
            {
                "title": step.get("title") or f"Paso {idx + 1}",
                "description": step.get("description") or "",
                "image": step_img,
            }
        )

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
        "time": time_v,
        "proteins": proteins,
    }
    if video:
        payload["video"] = video
    else:
        print("  (sin video)")

    r = requests.post(
        f"{API}/editRecipe",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=300,
    )
    if r.status_code >= 400:
        print(f"FAIL {recipe_id}: {r.status_code} {r.text[:400]}")
        r.raise_for_status()

    again = get_recipe(token, recipe_id)
    img = again["recipe_list"][0].get("image") or ""
    vid = again["recipe_list"][0].get("video") or ""
    print(f"  image={'CLOUD' if 'cloudinary.com' in img else 'LOCAL'} {img[:100]}")
    print(f"  video={'CLOUD' if 'cloudinary.com' in vid else 'LOCAL/NONE'} {vid[:100]}")
    for i, s in enumerate(again.get("step_list") or []):
        si = s.get("image") or ""
        print(f"  step{i+1}={'CLOUD' if 'cloudinary.com' in si else 'LOCAL'} {si[:80]}")


def main() -> int:
    for email, ids in ACCOUNTS.items():
        print(f"\n== {email} ==")
        token = login(email)
        for rid in ids:
            update_recipe(token, rid)
    print("\nDONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
