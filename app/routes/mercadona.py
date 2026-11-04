"""Proxy a la API de tienda online (catálogo + búsqueda Algolia) para precios."""

from __future__ import annotations

import os
import re
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


# Palabras de receta que no ayudan a encontrar el producto en tienda
_FILLER_TOKENS = {
    "aprox",
    "aproximadamente",
    "opcional",
    "pero",
    "recomendado",
    "recomendada",
    "recomendados",
    "recomendadas",
    "fresco",
    "fresca",
    "frescos",
    "frescas",
    "limpio",
    "limpia",
    "limpios",
    "limpias",
    "trozos",
    "trozo",
    "troceado",
    "troceada",
    "troceados",
    "troceadas",
    "mediana",
    "mediano",
    "medianas",
    "medianos",
    "grande",
    "grandes",
    "pequeno",
    "pequena",
    "pequenos",
    "pequenas",
    "unidad",
    "unidades",
    "cucharadita",
    "cucharada",
    "al",
    "de",
    "del",
    "la",
    "el",
    "los",
    "las",
    "en",
    "con",
    "para",
    "por",
    "una",
    "uno",
    "unos",
    "unas",
    "sin",
    "tipo",
    "o",
    "u",
    "y",
    "etc",
}

# Alias de nombres de receta → consulta de tienda
_QUERY_ALIASES = {
    "piel de limon": "limon",
    "corteza de limon": "limon",
    "cascara de limon": "limon",
    "zest de limon": "limon",
    "yemas": "huevos",
    "yema": "huevos",
    "yema de huevo": "huevos",
    "yemas de huevo": "huevos",
    "clara": "huevos",
    "claras": "huevos",
    "claras de huevo": "huevos",
    "huevos frescos m/l": "huevos",
    "huevos frescos": "huevos",
    "huevo fresco": "huevos",
    "cebolla dulce": "cebolla",
    "pulpo limpio": "pulpo",
    "pollo en trozos": "pollo",
    "conejo en trozos": "conejo",
    # En el catálogo online no suele aparecer "bomba"; redondo/Sendra es el de paella
    "arroz bomba": "arroz redondo",
    "arroz bomba o d.o. valencia": "arroz redondo",
    "arroz bomba o do valencia": "arroz redondo",
    # Maicena / Maizena → harina de maíz del catálogo
    "maicena": "harina maiz",
    "maizena": "harina maiz",
    "fecula de maiz": "harina maiz",
    "fecula maiz": "harina maiz",
    # Cortes genéricos + especie: buscar la especie (si no, "lomos" = cerdo)
    "lomos de bacalao desalado": "lomo bacalao",
    "lomo de bacalao desalado": "lomo bacalao",
    "lomos de bacalao": "lomo bacalao",
    "lomo de bacalao": "lomo bacalao",
    "bacalao desalado": "bacalao",
    "romero fresco": "romero",
    "oregano fresco": "oregano",
    "tomillo fresco": "tomillo",
    "perejil fresco": "perejil",
    # Nunca dejar la abreviatura: AOVE = Aceite de Oliva Virgen Extra
    "aove": "aceite oliva virgen extra",
    "aceite aove": "aceite oliva virgen extra",
    "aceite de oliva aove": "aceite oliva virgen extra",
}

# Cortes / formatos: no sirven solos como búsqueda (lomo ≠ bacalao)
_SHAPE_TOKENS = {
    "lomo",
    "lomos",
    "filete",
    "filetes",
    "pechuga",
    "pechugas",
    "muslo",
    "muslos",
    "contramuslo",
    "contramuslos",
    "trozo",
    "trozos",
    "pieza",
    "piezas",
    "porcion",
    "porciones",
    "medallon",
    "medallones",
    "rodaja",
    "rodajas",
    "loncha",
    "lonchas",
    "entero",
    "entera",
    "enteros",
    "enteras",
    "migas",
    "tira",
    "tiras",
    "dado",
    "dados",
}

# Higiene / no-comida frecuente en resultados de especias
_NOISE_NONFOOD = (
    "alcohol de",
    "corporal",
    "champu",
    "shampoo",
    "gel de ducha",
    "colonia",
    "desodorante",
    "crema de manos",
    "after shave",
    "aftershave",
)

# Ruido genérico (procesados / mascotas) cuando buscamos el ingrediente “de verdad”
_NOISE_ALWAYS = (
    "perro",
    "perros",
    "gato",
    "gatos",
    "mascota",
    "mascotas",
    "enano",
    "enanos",
    "pienso",
    "granzoo",
    "quartett",
    "alimento completo",
    "para perros",
    "para gatos",
    "para conejos",
    "lavavajillas",
    "limpiador",
    "detergente",
    "ambientador",
    "lejia",
    "suavizante",
)

_NOISE_PROCESSED = (
    "sopa ",
    "sopa de",
    "crema de",
    "en polvo",
    "frita",
    "fritas",
    "frito",
    "fritos",
    "snack",
    "chips",
    "panecillo",
    "pan ",
    "bolleria",
    "bollería",
    "tortitas",
    "bebida de",
    "bebida ",
    "cocido",
    "cocida",
    "precocido",
    "precocida",
    "ultracongelad",
    "deshidratad",
    "instantane",
    "sobre ",
    "pasta ",
    "tagliatelle",
    "fideos",
    "macarron",
    "espagueti",
    "helado",
    "yogur",
    "galleta",
    "galletas",
    "patatas fritas",
    "onduladas",
    "sabor ",
    "aromatizad",
    "refresco",
    "fanta",
    "gaseosa",
    "teriyaki",
    "curry",
    "nugget",
    "croqueta",
    "empanado",
    "fiambre",
    "loncha",
    "lonchas",
    "plato preparado",
)

_PAREN_RE = re.compile(r"\([^)]*\)")
_SIZE_RE = re.compile(r"\b[mlsxl](?:\s*/\s*[mlsxl])+\b", re.I)
_QTY_RE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:g|kg|ml|l|cl|ud|uds|unidades?|cucharadas?|cucharaditas?)?\b",
    re.I,
)


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


def _strip_recipe_noise(query: str) -> str:
    raw = _normalize(query)
    raw = _PAREN_RE.sub(" ", raw)
    raw = _SIZE_RE.sub(" ", raw)
    raw = _QTY_RE.sub(" ", raw)
    raw = raw.replace("/", " ").replace("-", " ")
    raw = re.sub(r"[^a-z0-9.\s]", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def _raw_meaningful_tokens(query: str) -> list[str]:
    raw = _strip_recipe_noise(query)
    return [
        t
        for t in raw.replace(".", " ").split()
        if t and t not in _FILLER_TOKENS and t not in {"d", "do"} and len(t) > 1
    ]


def _is_shape_token(token: str) -> bool:
    if not token:
        return False
    if token in _SHAPE_TOKENS:
        return True
    # plural simple
    if token.endswith("es") and token[:-2] in _SHAPE_TOKENS:
        return True
    if token.endswith("s") and token[:-1] in _SHAPE_TOKENS:
        return True
    return False


def _singular_shape(token: str) -> str:
    if token.endswith("es") and len(token) > 4 and token[:-2] in _SHAPE_TOKENS:
        return token[:-2]
    if token.endswith("s") and len(token) > 3 and token[:-1] in _SHAPE_TOKENS:
        return token[:-1]
    return token


def _anchor_tokens(query: str) -> list[str]:
    """Tokens que identifican el alimento (bacalao), no el corte (lomo)."""
    return [t for t in _raw_meaningful_tokens(query) if not _is_shape_token(t)]


def _shape_tokens_in_query(query: str) -> list[str]:
    return [_singular_shape(t) for t in _raw_meaningful_tokens(query) if _is_shape_token(t)]


def _clean_search_query(query: str) -> str:
    """Reduce texto de receta a lo que conviene buscar en el catálogo."""
    raw = _strip_recipe_noise(query)

    if raw in _QUERY_ALIASES:
        return _QUERY_ALIASES[raw]

    for alias, target in sorted(_QUERY_ALIASES.items(), key=lambda x: -len(x[0])):
        if raw == alias or raw.startswith(alias + " "):
            return target

    tokens = _raw_meaningful_tokens(query)
    cleaned = " ".join(tokens).strip()
    if cleaned in _QUERY_ALIASES:
        return _QUERY_ALIASES[cleaned]

    anchors = [t for t in tokens if not _is_shape_token(t)]
    shapes = [_singular_shape(t) for t in tokens if _is_shape_token(t)]

    # "lomos de bacalao desalado" → buscar "lomo bacalao" (no "lomos" solo)
    if anchors and shapes:
        return f"{shapes[0]} {anchors[0]}"
    if anchors:
        return " ".join(anchors)
    return cleaned or raw


def _core_tokens(query: str) -> list[str]:
    """Tokens que DEBEN aparecer en el producto (ancla alimentaria, no el corte)."""
    cleaned = _clean_search_query(query)
    cleaned_tokens = [
        t
        for t in cleaned.replace(".", " ").split()
        if t and t not in _FILLER_TOKENS and t not in {"d", "do"} and len(t) > 1
    ]
    anchors = _anchor_tokens(query)
    # Anclas que siguen en la búsqueda (bacalao sí; desalado si el alias lo quitó, no)
    required = [a for a in anchors if a in cleaned_tokens]
    if required:
        for t in cleaned_tokens:
            if not _is_shape_token(t) and t not in required:
                required.append(t)
        return required
    non_shape = [t for t in cleaned_tokens if not _is_shape_token(t)]
    return non_shape or cleaned_tokens


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

    search_q = _clean_search_query(query)
    cores = _core_tokens(query)
    anchors = _anchor_tokens(query) or cores
    shapes = _shape_tokens_in_query(query)
    algolia_q = search_q or query

    primary, status = _algolia_search(algolia_q, limit=48)
    # Segunda pasada SOLO con ancla alimentaria (nunca "lomos"/"filetes" solos)
    secondary: list[dict] = []
    anchor_q = anchors[0] if anchors else ""
    if anchor_q and anchor_q != algolia_q and (status != 200 or len(primary) < 6):
        sec, sec_status = _algolia_search(anchor_q, limit=36)
        if sec_status == 200:
            secondary = sec

    local: list[dict] = []
    if category_id not in (None, "", False):
        try:
            cid = int(category_id)
        except (TypeError, ValueError):
            return jsonify(error="category_id inválido"), 400
        local = _search_category_local(algolia_q, cid)
        if anchor_q and anchor_q != algolia_q:
            local = _merge_products(local, _search_category_local(anchor_q, cid), limit=80)

    if status != 200 and not local:
        err = primary[0] if primary and isinstance(primary[0], dict) else {"error": "Búsqueda fallida"}
        return jsonify(err), status

    catalog = primary if status == 200 else []
    products = _merge_products(local, catalog, secondary, limit=80)
    products = _filter_relevant(products, query)
    if not products and (catalog or local or secondary):
        # Soft: exige la ancla (bacalao / maiz), nunca el corte genérico
        soft_q = anchor_q or (cores[0] if cores else algolia_q)
        products = _filter_relevant(
            _merge_products(local, catalog, secondary, limit=80),
            soft_q,
            soft=True,
        )
    products = _rank_by_query(products, query)
    return jsonify(
        ingredient=query,
        search_q=algolia_q,
        anchors=anchors,
        shapes=shapes,
        products=products,
        count=len(products),
        source="category+catalog" if local else "catalog",
    )


def _query_tokens(query: str) -> list[str]:
    return _core_tokens(query)


def _token_in_name(token: str, name: str) -> bool:
    """Palabra completa; admite plural simple (canela/canelas), no prefijos (canelones)."""
    if not token or not name:
        return False
    # Singularizar token de consulta para cubrir huevos→huevo y al revés
    forms = {token}
    if token.endswith("es") and len(token) > 4:
        forms.add(token[:-2])
    elif token.endswith("s") and len(token) > 3:
        forms.add(token[:-1])
    for form in forms:
        pat = rf"(?<![a-z0-9]){re.escape(form)}(?:es|s)?(?![a-z0-9])"
        if re.search(pat, name):
            return True
    return False


def _is_pet_or_noise(name: str) -> bool:
    return any(n in name for n in _NOISE_ALWAYS) or any(n in name for n in _NOISE_NONFOOD)


_HERB_ANCHORS = {
    "romero",
    "oregano",
    "tomillo",
    "perejil",
    "albahaca",
    "laurel",
    "cilantro",
    "hierbabuena",
    "menta",
}
_HERB_NOISE = (
    "hamburguesa",
    "cracker",
    "crackers",
    "alcohol",
    "corporal",
    "salsa",
    "snack",
    "patatas fritas",
)
_FRUIT_NOISE = (
    "granizado",
    "mantecado",
    "refresco",
    "fanta",
    "helado",
    "galleta",
    "golosina",
    "gominola",
    "yogur",
    "batido",
)


def _filter_relevant(products: list[dict], query: str, *, soft: bool = False) -> list[dict]:
    """Exige el núcleo del ingrediente y descarta mascotas / ruido claro."""
    cores = _core_tokens(query)
    if not cores:
        cores = _anchor_tokens(query) or [t for t in _normalize(query).split() if len(t) > 2]
    # Nunca filtrar solo por corte genérico
    cores = [t for t in cores if not _is_shape_token(t)] or cores
    head = cores[0] if cores else ""
    out = []
    for p in products:
        name = _normalize(p.get("display_name") or "")
        if not name or _is_pet_or_noise(name):
            continue
        if head in _HERB_ANCHORS and any(n in name for n in _HERB_NOISE):
            continue
        if head.startswith("limon") and any(n in name for n in _FRUIT_NOISE):
            continue
        if cores:
            need = cores[:1] if soft else cores
            if not all(_token_in_name(t, name) for t in need):
                continue
        out.append(p)
    return out


def _name_starts_with_ingredient(name: str, anchors: list[str], phrase: str) -> bool:
    if phrase and name.startswith(phrase):
        return True
    first = name.split(" ", 1)[0] if name else ""
    # Empezar por el alimento (huevos, cebollas), no por "lomo" genérico
    return bool(anchors and _token_in_name(anchors[0], first))


def _product_price(p: dict) -> float:
    raw = p.get("price")
    if raw is None:
        raw = p.get("bulk_price")
    try:
        n = float(raw)
    except (TypeError, ValueError):
        return float("inf")
    return n if n >= 0 else float("inf")


def _rank_by_query(products: list[dict], query: str) -> list[dict]:
    """Grupo de producto real primero; dentro del grupo, el más barato."""
    phrase = _clean_search_query(query)
    cores = _core_tokens(query)
    anchors = _anchor_tokens(query) or cores
    shapes = _shape_tokens_in_query(query)
    original = _normalize(query)

    def score(p: dict) -> tuple:
        name = _normalize(p.get("display_name") or "")
        price = _product_price(p)
        # Menor es mejor
        s = 100
        if _is_pet_or_noise(name):
            return (9, price, 10_000, 99, name)

        if phrase and phrase in name:
            s -= 60
        if original and original != phrase and original in name:
            s -= 40
        if cores and all(_token_in_name(t, name) for t in cores):
            s -= 40
        elif anchors and _token_in_name(anchors[0], name):
            s -= 20
        else:
            s += 90

        # Corte pedido (lomo) suma; corte solo sin ancla ya está filtrado
        if shapes and any(_token_in_name(sh, name) for sh in shapes):
            s -= 25
        if "desalad" in original and "desalad" in name:
            s -= 20

        if _name_starts_with_ingredient(name, anchors, phrase):
            s -= 45

        word_count = len([w for w in name.split() if w])
        s += max(0, word_count - 3) * 4

        for noise in _NOISE_PROCESSED:
            n = noise.strip()
            if n and n in name and n not in phrase and n not in original:
                bump = 55
                if n in {"ultracongelad", "deshidratad"}:
                    bump = 12
                s += bump

        head = (anchors[0] if anchors else (cores[0] if cores else "")) or ""
        if head.startswith("huev") and ("pasta" in name or "tagliatelle" in name or "fideo" in name):
            s += 120
        if "harina" in phrase or head.startswith("harin") or "maiz" in phrase:
            if "panecillo" in name or name.startswith("pan "):
                s += 120
            # Maicena / harina de maíz
            if "maiz" in phrase or "maicen" in original or "maizen" in original:
                if "maiz" in name:
                    s -= 40
                if "fina" in name:
                    s -= 15
            elif head.startswith("harin") or phrase.startswith("harina"):
                if "trigo" in name:
                    s -= 30
                specialties = ("arroz", "garbanzo", "almendra", "coco", "fuerza", "maiz")
                if any(x in name for x in specialties) and not any(x in phrase for x in specialties):
                    s += 18
        if head.startswith("ceboll") and ("sopa" in name or "patatas fritas" in name or "sabor" in name):
            s += 100
        if head.startswith("arroz") and (
            "bebida" in name or "tortitas" in name or "cocido" in name or "leche" in name
        ):
            s += 100
        if "bomba" in original:
            if "sendra" in name:
                s -= 75
            elif "bomba" in name:
                s -= 70
            elif "redondo" in name and "cocido" not in name:
                s -= 40
            if "cocido" in name:
                s += 50
            if any(x in name for x in ("basmati", "largo", "vaporizado", "microondas", "verduras")):
                s += 35
        if head.startswith("limon") or head.startswith("limones"):
            if name.startswith("limon") or name.startswith("limones"):
                s -= 45
            if any(
                x in name
                for x in (
                    "refresco",
                    "fanta",
                    "ambientador",
                    "golosina",
                    "gominola",
                    "helado",
                    "lavavajillas",
                    "limpiador",
                    "mantecado",
                    "granizado",
                    "galleta",
                )
            ):
                s += 100
        if head.startswith("pulp") and any(x in name for x in ("pota", "calamar", "sepia")):
            s += 90
        if head.startswith("bacala"):
            # Nunca carne disfrazada de "lomo"
            if any(x in name for x in ("cerdo", "vacuno", "iberico", "ibérico", "anojo", "añojo", "cebo")):
                s += 200
            if "salmon" in name:
                s += 80
            if "piquillo" in name or "relleno" in name or "dorado con" in name:
                s += 50
            if "lomo" in name and "bacalao" in name:
                s -= 35
        if head.startswith("romer") or head in {"oregano", "tomillo", "perejil", "albahaca", "laurel"}:
            if any(x in name for x in ("hamburguesa", "cracker", "alcohol", "corporal", "aceite corporal")):
                s += 120
            if name.startswith(head) or name.startswith(head.rstrip("o") + "os"):
                s -= 40
        if head.startswith("poll"):
            if any(
                x in name
                for x in (
                    "teriyaki",
                    "curry",
                    "fiambre",
                    "loncha",
                    "nugget",
                    "croqueta",
                    "asado",
                    "relleno",
                )
            ):
                s += 70
            if any(x in name for x in ("pechuga", "muslo", "filete", "contramuslo", "entero", "troceado")) and (
                "asado" not in name and "curry" not in name
            ):
                s -= 40
        if head.startswith("conej"):
            if "enano" in name or "alimento" in name:
                s += 200
            if "troceado" in name or "entero" in name:
                s -= 30

        # Tier grueso: 0 = producto pedido, luego derivados.
        # Dentro del mismo tier → precio (más barato primero).
        has_anchor = bool(anchors) and all(_token_in_name(a, name) for a in anchors[:1])
        has_shape = bool(shapes) and any(_token_in_name(sh, name) for sh in shapes)
        if s >= 180 or not has_anchor:
            tier = 3
        elif shapes:
            # "lomos de bacalao" → primero los lomos de bacalao; luego otro bacalao
            tier = 0 if has_shape else 1
            if s >= 120:
                tier = max(tier, 2)
        else:
            if s <= 55:
                tier = 0
            elif s <= 100:
                tier = 1
            else:
                tier = 2

        return (tier, price, s, word_count, name)

    return sorted(products, key=score)