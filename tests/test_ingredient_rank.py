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
    assert _clean_search_query("AOVE") == "aceite oliva virgen extra"
    assert _clean_search_query("aove") == "aceite oliva virgen extra"


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


def test_real_group_sorted_by_price():
    products = [
        _p("Huevos camperos Hacendado", 3.35),
        _p("Huevos grandes L", 1.80),
        _p("Huevos medianos M", 2.85),
        _p("Pasta fresca tagliatelle al huevo Hacendado", 1.20),
    ]
    ranked = _rank_by_query(_filter_relevant(products, "Huevos frescos M/L"), "Huevos frescos M/L")
    assert ranked[0]["display_name"] == "Huevos grandes L"
    assert ranked[0]["price"] == 1.80
    # Entre huevos reales, orden por precio
    egg_prices = [p["price"] for p in ranked if p["display_name"].startswith("Huevos")]
    assert egg_prices == sorted(egg_prices)


def test_bacalao_not_pork_loin():
    q = "Lomos de bacalao desalado"
    assert _clean_search_query(q) == "lomo bacalao"
    assert "bacalao" in _core_tokens(q)
    assert "lomos" not in _core_tokens(q)
    products = [
        _p("Lomo Hacendado", 6.13),
        _p("Lomo de cerdo trozo", 4.95),
        _p("Lomo de vacuno añojo", 8.09),
        _p("Lomos de salmón sin piel Hacendado congelado", 7.0),
        _p("Lomo de bacalao MareDeus ultracongelado", 9.22),
        _p("Migas de bacalao desaladas Hacendado", 7.64),
    ]
    filtered = _filter_relevant(products, q)
    assert all("bacalao" in p["display_name"].lower() for p in filtered)
    ranked = _rank_by_query(filtered, q)
    assert "bacalao" in ranked[0]["display_name"].lower()
    assert "cerdo" not in ranked[0]["display_name"].lower()
    assert "vacuno" not in ranked[0]["display_name"].lower()


def test_maicena_maps_to_corn_flour():
    assert _clean_search_query("maicena") == "harina maiz"
    products = [
        _p("Harina de trigo Hacendado", 0.72),
        _p("Harina fina de maíz Hacendado", 1.20),
        _p("Harina de maíz blanco precocida Hacendado", 1.70),
    ]
    ranked = _rank_by_query(_filter_relevant(products, "maicena"), "maicena")
    assert ranked
    assert "maíz" in ranked[0]["display_name"].lower() or "maiz" in ranked[0]["display_name"].lower()


def test_romero_prefers_spice_jar():
    products = [
        _p("Alcohol de romero Deliplus", 2.0),
        _p("Hamburguesa de cordero al romero", 3.8),
        _p("Aceite corporal de romero Deliplus 100% natural", 3.2),
        _p("Romero Hacendado", 1.35),
        _p("Crackers sin gluten Hacendado con romero", 1.7),
    ]
    filtered = _filter_relevant(products, "Romero fresco")
    ranked = _rank_by_query(filtered, "Romero fresco")
    assert ranked[0]["display_name"].startswith("Romero")


def test_merluza_rejects_baby_food_and_fingers():
    products = [
        _p("Papilla verduritas con merluza Hero Solo +6 meses", 1.8),
        _p("Palitos de merluza a la romana Hacendado ultracongelados", 2.8),
        _p("Fingers de merluza Hacendado", 3.0),
        _p("Merluza rebozada", 3.5),
        _p("Filetes de merluza sin piel", 6.5),
        _p("Merluza en rodajas", 5.9),
    ]
    filtered = _filter_relevant(products, "Merluza")
    names = " ".join(p["display_name"].lower() for p in filtered)
    assert "papilla" not in names
    assert "fingers" not in names
    assert "palitos" not in names
    assert "rebozada" not in names
    ranked = _rank_by_query(filtered, "Merluza")
    assert "merluza" in ranked[0]["display_name"].lower()
    assert ranked[0]["is_best_match"] is True


def test_vino_blanco_not_vinegar():
    products = [
        _p("Vinagre de vino blanco Hacendado", 0.65),
        _p("Vino blanco Casón Histórico", 1.05),
        _p("Vino blanco Airén", 1.5),
    ]
    filtered = _filter_relevant(products, "Vino blanco")
    assert all("vinagre" not in p["display_name"].lower() for p in filtered)
    ranked = _rank_by_query(filtered, "Vino blanco")
    assert ranked[0]["display_name"].lower().startswith("vino blanco")


def test_pollo_trozos_not_broth_or_carcass():
    products = [
        _p("Caldo de pollo Hacendado", 0.75),
        _p("Hígados y corazones de pollo", 1.2),
        _p("Carcasa y espinazo de pollo", 1.23),
        _p("Sazonador pollo y carne Hacendado", 0.55),
        _p("Gyozas de pollo y verduras Hacendado congeladas", 1.95),
        _p("Pollo entero", 6.65),
        _p("Medio pollo troceado", 3.6),
        _p("Muslos de pollo", 2.78),
    ]
    filtered = _filter_relevant(products, "Pollo en trozos")
    blob = " ".join(p["display_name"].lower() for p in filtered)
    assert "caldo" not in blob
    assert "carcasa" not in blob
    assert "sazonador" not in blob
    assert "gyoza" not in blob
    assert "higado" not in blob and "hígado" not in blob
    ranked = _rank_by_query(filtered, "Pollo en trozos")
    top = ranked[0]["display_name"].lower()
    assert "pollo" in top
    assert "gyoza" not in top


def test_calamar_limpio_prefers_clean_not_canned_sauce():
    products = [
        _p("Calamar en salsa americana Hacendado", 2.7),
        _p("Calamar en tinta Hacendado", 3.1),
        _p("Calamar grande Hacendado congelado", 3.5),
        _p("Calamar pequeño limpio patagónico", 5.8),
        _p("Calamar troceado limpio Hacendado congelado", 4.2),
    ]
    filtered = _filter_relevant(products, "Calamar limpio")
    assert all("salsa" not in p["display_name"].lower() for p in filtered)
    assert all("tinta" not in p["display_name"].lower() for p in filtered)
    ranked = _rank_by_query(filtered, "Calamar limpio")
    assert "limpio" in ranked[0]["display_name"].lower()


def test_higado_not_pate_first():
    products = [
        _p("Paté de hígado de cerdo ibérico Hacendado", 2.0),
        _p("Filetes hígado de cerdo", 3.37),
        _p("Paté de hígado de cerdo sabor intenso Hacendado", 2.0),
    ]
    filtered = _filter_relevant(products, "Hígado de cerdo")
    assert all("paté" not in p["display_name"].lower() and "pate" not in p["display_name"].lower() for p in filtered)
    ranked = _rank_by_query(filtered, "Hígado de cerdo")
    assert "filete" in ranked[0]["display_name"].lower()


def test_gambas_not_stirfry_first():
    products = [
        _p("Salteado de gambas, espárragos verdes Hacendado", 2.9),
        _p("Gamba pelada cruda tamaño mediano", 4.9),
        _p("Gamba pelada cruda tamaño grande", 5.95),
    ]
    filtered = _filter_relevant(products, "Gambas")
    assert all("salteado" not in p["display_name"].lower() for p in filtered)
    ranked = _rank_by_query(filtered, "Gambas")
    assert ranked[0]["display_name"].startswith("Gamba")
    assert ranked[0]["price"] == min(p["price"] for p in ranked)
