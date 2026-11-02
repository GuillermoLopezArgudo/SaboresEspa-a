"""Proxy a la API pública de tienda.mercadona.es para precios de ingredientes."""

from __future__ import annotations

import time
from threading import Lock

import requests
from flask import Blueprint, jsonify, request

from app.rate_limit import rate_limit

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
CACHE_MAX_KEYS = 200


def _evict_cache(now: float) -> None:
    """Quita entradas caducadas y recorta si hay demasiadas claves."""
    expired = [k for k, (ts, _) in _cache.items() if now - ts >= CACHE_TTL]
    for k in expired:
        _cache.pop(k, None)
    if len(_cache) <= CACHE_MAX_KEYS:
        return
    # Más antiguas primero
    ordered = sorted(_cache.items(), key=lambda item: item[1][0])
    overflow = len(_cache) - CACHE_MAX_KEYS
    for k, _ in ordered[:overflow]:
        _cache.pop(k, None)


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
            _evict_cache(now)
            _cache[url] = (now, data)
        return data, 200
    except requests.Timeout:
        return {"error": "Timeout al contactar con Mercadona"}, 504
    except requests.RequestException as exc:
        return {"error": str(exc)}, 502


@mercadona_bp.get("/categories")
@rate_limit(max_calls=60, window_seconds=60, prefix="mercadona")
def get_categories():
    data, status = _cached_get("/categories/")
    return jsonify(data), status


@mercadona_bp.post("/productos")
@rate_limit(max_calls=60, window_seconds=60, prefix="mercadona")
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


def _normalize(text: str) -> str:
    import unicodedata

    raw = (text or "").lower().strip()
    decomposed = unicodedata.normalize("NFD", raw)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _variants(query: str) -> set[str]:
    base = _normalize(query)
    out = {base}
    for token in base.replace("/", " ").replace("-", " ").split():
        if len(token) > 2:
            out.add(token)
    if base.endswith("es") and len(base) > 4:
        out.add(base[:-2])
    elif base.endswith("s") and len(base) > 3:
        out.add(base[:-1])
    return {v for v in out if v}


def _product_payload(product: dict) -> dict:
    price_info = product.get("price_instructions") or {}
    return {
        "id": product.get("id"),
        "display_name": product.get("display_name"),
        "thumbnail": product.get("thumbnail"),
        "price": price_info.get("unit_price") or price_info.get("bulk_price"),
        "bulk_price": price_info.get("bulk_price"),
        "unit_size": price_info.get("unit_size"),
        "size_format": price_info.get("size_format"),
        "packaging": product.get("packaging"),
    }


@mercadona_bp.post("/searchIngredient")
@rate_limit(max_calls=60, window_seconds=60, prefix="mercadona")
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

    variants = _variants(query)
    products = []
    seen = set()
    for category in data.get("categories") or []:
        for product in category.get("products") or []:
            name = _normalize(product.get("display_name") or "")
            if any(v in name for v in variants):
                pid = product.get("id") or product.get("display_name")
                if pid in seen:
                    continue
                seen.add(pid)
                products.append(_product_payload(product))
    return jsonify(ingredient=query, products=products, count=len(products))