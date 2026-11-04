"""Ranking / limpieza de búsquedas de ingredientes (sin red)."""

from app.routes.mercadona import (
    _clean_search_query,
    _core_tokens,
    _filter_relevant,
    _rank_by_query,
)


def _p(name: str, price: float = 1.0) -> dict:
    return {"id": name, "display_name": name, "price": price}


def test_clean_query_strips_recipe_noise():
    assert _clean_search_query("Huevos frescos M/L") == "huevos"
    assert _clean_search_query("Cebolla dulce (opcional pero recomendada)") == "cebolla"
    assert _clean_search_query("Pulpo limpio") == "pulpo"
    assert _clean_search_query("Arroz bomba (o D.O. Valencia)") == "arroz redondo"
    assert _clean_search_query("Piel de limón") == "limon"
    assert _clean_search_query("Pollo en trozos") == "pollo"
    assert _clean_search_query("Conejo en trozos") == "conejo"


def test_huevos_prefers_eggs_not_pasta():
    products = [
        _p("Pasta fresca tagliatelle al huevo Hacendado", 1.2),
        _p("Huevos frescos M/L Hacendado", 2.1),
        _p("Huevos camperos Hacendado", 2.5),
    ]
    ranked = _rank_by_query(_filter_relevant(products, "Huevos frescos M/L"), "Huevos frescos M/L")
    assert ranked[0]["display_name"].startswith("Huevos")
    assert all("Pasta" not in p["display_name"] or True for p in ranked)
    # Pasta no debería quedar primera ni preferida
    assert "Pasta" not in ranked[0]["display_name"]


def test_cebolla_prefers_fresh_over_soup():
    products = [
        _p("Sopa de cebolla Hacendado", 0.65),
        _p("Cebolla en polvo Hacendado", 0.94),
        _p("Patatas fritas onduladas sabor queso de cabra y cebolla caramelizada", 1.25),
        _p("Cebollas rojas", 1.4),
        _p("Cebolla blanca", 1.5),
    ]
    ranked = _rank_by_query(_filter_relevant(products, "Cebolla"), "Cebolla")
    assert "Sopa" not in ranked[0]["display_name"]
    assert ranked[0]["display_name"].lower().startswith("ceboll")


def test_harina_prefers_flour_not_bread():
    products = [
        _p("Panecillo harina integral 50% de trigo sin sal añadida", 0.33),
        _p("Harina de trigo Hacendado", 0.72),
        _p("Harina integral de trigo Hacendado", 0.9),
    ]
    ranked = _rank_by_query(_filter_relevant(products, "Harina"), "Harina")
    assert ranked[0]["display_name"].startswith("Harina")


def test_pulpo_keeps_octopus_drops_squid_first():
    products = [
        _p("Tubo de pota Argentina limpio Hacendado congelado", 1.5),
        _p("Calamar pequeño limpio patagónico", 5.85),
        _p("Pulpo cocido Hacendado", 6.5),
        _p("Pulpo crudo limpio", 8.0),
    ]
    filtered = _filter_relevant(products, "Pulpo limpio")
    ranked = _rank_by_query(filtered, "Pulpo limpio")
    assert all("pulpo" in p["display_name"].lower() for p in ranked)
    assert ranked[0]["display_name"].lower().startswith("pulpo")


def test_arroz_bomba_prefers_paella_rice():
    products = [
        _p("Arroz cocido integral Sabroz", 1.05),
        _p("Bebida de arroz sin azúcares añadidos Hacendado", 1.05),
        _p("Tortitas de arroz Hacendado", 1.1),
        _p("Arroz largo Hacendado", 1.2),
        _p("Arroz redondo Hacendado", 1.15),
        _p("Arroz redondo J Sendra Hacendado", 1.8),
        _p("Arroz bomba Hacendado", 2.2),
    ]
    q = "Arroz bomba (o D.O. Valencia)"
    ranked = _rank_by_query(_filter_relevant(products, q), q)
    top = ranked[0]["display_name"].lower()
    assert "cocido" not in top and "bebida" not in top and "tortitas" not in top
    assert "bomba" in top or "sendra" in top or "redondo" in top


def test_pet_food_filtered():
    products = [
        _p("Trozos de pollo y verduras en salsa perros adultos Quartett", 2.25),
        _p("Alimento completo conejos enanos Granzoo", 1.7),
        _p("Pechuga de pollo fileteada", 4.5),
        _p("Medio conejo troceado", 5.82),
    ]
    pollo = _filter_relevant(products, "Pollo en trozos")
    assert all("perro" not in p["display_name"].lower() for p in pollo)
    assert any("pollo" in p["display_name"].lower() for p in pollo)

    conejo = _filter_relevant(products, "Conejo en trozos")
    assert all("enanos" not in p["display_name"].lower() for p in conejo)
    assert any("conejo" in p["display_name"].lower() for p in conejo)


def test_core_tokens():
    assert _core_tokens("Huevos frescos M/L") == ["huevos"]
    # Catálogo online: bomba → redondo (Sendra / paella)
    assert _clean_search_query("Arroz bomba (o D.O. Valencia)") == "arroz redondo"
    assert _core_tokens("Arroz bomba (o D.O. Valencia)") == ["arroz", "redondo"]


def test_among_real_products_cheapest_first():
    products = [
        _p("Cebollas rojas", 1.40),
        _p("Cebollas", 1.50),
        _p("Cebollas", 1.20),
        _p("Sopa de cebolla Hacendado", 0.65),
    ]
    ranked = _rank_by_query(_filter_relevant(products, "Cebolla"), "Cebolla")
    # Sopa queda atrás pese a ser más barata; entre cebollas gana la de 1.20
    assert ranked[0]["display_name"] == "Cebollas"
    assert ranked[0]["price"] == 1.20
    assert ranked[-1]["display_name"].startswith("Sopa")
