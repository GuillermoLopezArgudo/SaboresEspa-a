"""Proxy a la API de tienda online (catálogo + búsqueda Algolia) para precios."""

from __future__ import annotations

import os
import time
from threading import Lock
from urllib.parse import urlencode

import requests
from flask import Blueprint, jsonify, request

from app.rate_limit import rate_limit

mercadona_bp = Blueprint("mercadona", __name__)

MERCADONA_BASE = "https://tienda.mercadona.es/api"
# Credenciales de solo lectura embebidas en el frontend de la tienda (Algolia)
ALGOLIA_APP_ID = "7UZJKL1DJ0"
ALGOLIA_API_KEY = "9d8f2e39e90df472b4f2e559a116fe17"
ALGOLIA_WAREHOUSE = os.getenv("MERCADONA_WH", "mad1")
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


def _algolia_hit_payload(hit: dict) -> dict:
    price_info = hit.get("price_instructions") or {}
    return {
        "id": hit.get("id"),
        "display_name": hit.get("display_name"),
        "thumbnail": hit.get("thumbnail"),
        "price": price_info.get("unit_price") or price_info.get("bulk_price"),
        "bulk_price": price_info.get("bulk_price"),
        "unit_size": price_info.get("unit_size"),
        "size_format": price_info.get("size_format"),
        "packaging": hit.get("packaging"),
    }


def _algolia_search(query: str, limit: int = 40) -> tuple[list[dict], int]:
    """Búsqueda de catálogo vía Algolia (misma que usa la tienda online)."""
    q = (query or "").strip()
    if not q:
        return [], 400
    limit = max(1, min(int(limit or 40), 50))
    index = f"products_prod_{ALGOLIA_WAREHOUSE}_es"
    cache_key = f"algolia:{ALGOLIA_WAREHOUSE}:{_normalize(q)}:{limit}"
    now = time.time()
    with _lock:
        hit = _cache.get(cache_key)
        if hit and now - hit[0] < CACHE_TTL:
            return hit[1], 200

    url = (
        f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{index}/query"
        f"?x-algolia-application-id={ALGOLIA_APP_ID}"
        f"&x-algolia-api-key={ALGOLIA_API_KEY}"
    )
    params = urlencode({"query": q, "hitsPerPage": str(limit)})
    try:
        resp = requests.post(
            url,
            headers={**HEADERS, "Content-Type": "application/json"},
            json={"params": params},
            timeout=20,
        )
        if resp.status_code >= 400:
            return [{"error": f"Búsqueda respondió {resp.status_code}"}], resp.status_code
        hits = resp.json().get("hits") or []
        products = [_algolia_hit_payload(h) for h in hits if h.get("display_name")]
        with _lock:
            _evict_cache(now)
            _cache[cache_key] = (now, products)
        return products, 200
    except requests.Timeout:
        return [{"error": "Timeout en la búsqueda"}], 504
    except requests.RequestException as exc:
        return [{"error": str(exc)}], 502


def _merge_products(*lists: list[dict], limit: int = 60) -> list[dict]:
    seen = set()
    out = []
    for lst in lists:
        for p in lst or []:
            if not isinstance(p, dict) or p.get("error"):
                continue
            pid = p.get("id") or p.get("display_name")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            out.append(p)
            if len(out) >= limit:
                return out
    return out


def _search_category_local(query: str, category_id: int) -> list[dict]:
    data, status = _cached_get(f"/categories/{category_id}")
    if status != 200 or not isinstance(data, dict):
        return []
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
    return products


@mercadona_bp.post("/searchIngredient")
@rate_limit(max_calls=60, window_seconds=60, prefix="mercadona")
def search_ingredient():
    """Busca productos por texto en todo el catálogo (Algolia) y opcionalmente por categoría."""
    body = request.get_json(silent=True) or {}
    query = (body.get("q") or body.get("ingredient") or "").strip()
    category_id = body.get("category_id")
    if not query:
        return jsonify(error="Falta el ingrediente"), 400

    # 1) Búsqueda global (frase completa)
    primary, status = _algolia_search(query, limit=40)
    if status != 200:
        # Si Algolia falla y hay categoría, intentar solo categoría
        if category_id:
            try:
                cid = int(category_id)
            except (TypeError, ValueError):
                return jsonify(error="category_id inválido"), 400
            local = _search_category_local(query, cid)
            return jsonify(ingredient=query, products=local, count=len(local), source="category")
        err = primary[0] if primary and isinstance(primary[0], dict) else {"error": "Búsqueda fallida"}
        return jsonify(err), status

    # 2) Ampliar con tokens sueltos (pan, cheddar, carne…) para cestas / frases largas
    token_lists = []
    tokens = [
        t
        for t in _normalize(query).replace("/", " ").replace("-", " ").split()
        if len(t) > 3
    ]
    # Evitar repetir la frase completa
    for token in tokens[:4]:
        if token == _normalize(query):
            continue
        extra, st = _algolia_search(token, limit=12)
        if st == 200:
            token_lists.append(extra)

    # 3) Si el usuario forzó categoría, mezclar también ese filtro local
    local = []
    if category_id:
        try:
            cid = int(category_id)
            local = _search_category_local(query, cid)
        except (TypeError, ValueError):
            pass

    products = _merge_products(primary, *token_lists, local, limit=60)
    return jsonify(
        ingredient=query,
        products=products,
        count=len(products),
        source="catalog",
    )