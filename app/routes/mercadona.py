"""Proxy a la API pública de tienda.mercadona.es para precios de ingredientes."""

from __future__ import annotations

import time
from threading import Lock

import requests
from flask import Blueprint, jsonify, request

mercadona_bp = Blueprint("mercadona", __name__)

MERCADONA_BASE = "https://tienda.mercadona.es/api"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "es-ES,es;q=0.9",
}

_cache: dict[str, tuple[float, dict]] = {}
_lock = Lock()
CACHE_TTL = 60 * 30  # 30 min


def _cached_get(path: str) -> tuple[dict | list, int]:
    url = f"{MERCADONA_BASE}{path}"
    now = time.time()
    with _lock:
        hit = _cache.get(url)
        if hit and now - hit[0] < CACHE_TTL:
            return hit[1], 200

    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code >= 400:
            return {"error": f"Mercadona respondió {resp.status_code}"}, resp.status_code
        data = resp.json()
        with _lock:
            _cache[url] = (now, data)
        return data, 200
    except requests.Timeout:
        return {"error": "Timeout al contactar con Mercadona"}, 504
    except requests.RequestException as exc:
        return {"error": str(exc)}, 502


@mercadona_bp.get("/categories")
def get_categories():
    data, status = _cached_get("/categories/")
    return jsonify(data), status


@mercadona_bp.post("/productos")
def get_productos():
    body = request.get_json(silent=True) or {}
    category_id = body.get("id") or request.args.get("id")
    if not category_id:
        return jsonify(error='Falta el parámetro "id" de categoría'), 400
    try:
        category_id = int(category_id)
    except (TypeError, ValueError):
        return jsonify(error="id de categoría inválido"), 400

    data, status = _cached_get(f"/categories/{category_id}")
    return jsonify(data), status


@mercadona_bp.post("/searchIngredient")
def search_ingredient():
    """Atajo: recibe texto de ingrediente y devuelve productos candidatos."""
    body = request.get_json(silent=True) or {}
    query = (body.get("q") or body.get("ingredient") or "").strip()
    category_id = body.get("category_id")
    if not query:
        return jsonify(error="Falta el ingrediente"), 400
    if not category_id:
        return jsonify(error="Falta category_id"), 400
    try:
        category_id = int(category_id)
    except (TypeError, ValueError):
        return jsonify(error="category_id inválido"), 400

    data, status = _cached_get(f"/categories/{category_id}")
    if status != 200 or not isinstance(data, dict):
        return jsonify(data), status

    q = query.lower()
    variants = {
        q,
        q[:-1] if len(q) > 3 else q,
        query[:1].upper() + query[1:].lower(),
    }
    products = []
    for category in data.get("categories") or []:
        for product in category.get("products") or []:
            name = (product.get("display_name") or "").lower()
            if any(v and v.lower() in name for v in variants):
                products.append(
                    {
                        "id": product.get("id"),
                        "display_name": product.get("display_name"),
                        "thumbnail": product.get("thumbnail"),
                        "price": (product.get("price_instructions") or {}).get(
                            "unit_price"
                        )
                        or (product.get("price_instructions") or {}).get("bulk_price"),
                        "bulk_price": (product.get("price_instructions") or {}).get(
                            "bulk_price"
                        ),
                        "unit_size": (product.get("price_instructions") or {}).get(
                            "unit_size"
                        ),
                        "size_format": (product.get("price_instructions") or {}).get(
                            "size_format"
                        ),
                        "packaging": product.get("packaging"),
                    }
                )
    return jsonify(ingredient=query, products=products, count=len(products))
