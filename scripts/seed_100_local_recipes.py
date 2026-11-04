"""Crea 100 recetas locales muy variadas (SQLite/Postgres) para probar precios/ingredientes.

Uso (con API local o solo DB):
  python scripts/seed_100_local_recipes.py
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

from app.db import db  # noqa: E402
from app.models import (  # noqa: E402
    Recipe,
    RecipeComment,
    RecipeFilter,
    RecipeIngredient,
    RecipeStep,
    SubRecipe,
    SubRecipeIngredient,
    SubRecipeStep,
    Users,
    create_tables,
)
from app.security import hash_password  # noqa: E402

PASS = "DemoPass123!"
AOVE = "Aceite de Oliva Virgen Extra"

# Salsas/caldos/mojos caseros → subrecetas independientes nombradas
_PREPARED_ING_RE = re.compile(
    r"^(caldo\b|fumet\b|mojo\b|salsa\b|mayonesa\b|alioli\b|mahonesa\b|tomate frito\b)",
    re.I,
)
_SUB_STEP_TITLES = {
    "caldo",
    "salsa",
    "salsas",
    "mojo",
    "mojo verde",
    "mojo rojo",
    "alioli",
    "mahonesa",
    "mayonesa",
    "brava",
    "fumet",
}

_SUB_EXPANSIONS: dict[str, list[tuple[str, str]]] = {
    "caldo de pescado": [
        ("Espinas y cabezas de pescado", "500 g"),
        ("Cebolla", "1"),
        ("Puerro", "1"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "caldo de verduras": [
        ("Zanahoria", "2"),
        ("Cebolla", "1"),
        ("Puerro", "1"),
        ("Apio", "2 tallos"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "caldo de pollo": [
        ("Carcasa o trozos de pollo", "800 g"),
        ("Cebolla", "1"),
        ("Zanahoria", "1"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "caldo de pollo o agua": [
        ("Carcasa o trozos de pollo", "800 g"),
        ("Cebolla", "1"),
        ("Zanahoria", "1"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "caldo de puchero": [
        ("Hueso de jamón", "1 trozo"),
        ("Garbanzos cocidos", "200 g"),
        ("Zanahoria", "1"),
        ("Puerro", "1"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "caldo de carne": [
        ("Huesos de ternera", "800 g"),
        ("Cebolla", "1"),
        ("Zanahoria", "1"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "mojo verde": [
        ("Cilantro fresco", "1 manojo"),
        ("Perejil fresco", "1/2 manojo"),
        ("Ajo", "3 dientes"),
        ("Comino molido", "1/2 cucharadita"),
        ("Vinagre de vino", "2 cucharadas"),
        (AOVE, "100 ml"),
        ("Sal fina", "al gusto"),
    ],
    "mojo rojo": [
        ("Pimentón dulce", "1 cucharada"),
        ("Pimentón picante", "1/2 cucharadita"),
        ("Ajo", "3 dientes"),
        ("Comino molido", "1/2 cucharadita"),
        ("Vinagre de vino", "2 cucharadas"),
        (AOVE, "100 ml"),
        ("Sal fina", "al gusto"),
    ],
    "alioli": [
        ("Ajo", "2 dientes"),
        ("Huevos frescos M/L", "1 yema"),
        (AOVE, "150 ml"),
        ("Sal fina", "al gusto"),
    ],
    "mayonesa": [
        ("Huevos frescos M/L", "1 yema"),
        (AOVE, "150 ml"),
        ("Limón", "unas gotas"),
        ("Sal fina", "al gusto"),
    ],
    "mahonesa": [
        ("Huevos frescos M/L", "1 yema"),
        (AOVE, "150 ml"),
        ("Limón", "unas gotas"),
        ("Sal fina", "al gusto"),
    ],
    "caldo": [
        ("Zanahoria", "2"),
        ("Cebolla", "1"),
        ("Puerro", "1"),
        ("Apio", "2 tallos"),
        ("Agua", "1,5 l"),
        ("Sal fina", "al gusto"),
    ],
    "mojo": [
        ("Ajo", "3 dientes"),
        ("Comino molido", "1/2 cucharadita"),
        ("Pimentón dulce", "1 cucharadita"),
        ("Vinagre de vino", "2 cucharadas"),
        ("Cilantro o perejil fresco", "1 manojo"),
        (AOVE, "100 ml"),
        ("Sal fina", "al gusto"),
    ],
    "salsa": [
        ("Ajo", "2 dientes"),
        (AOVE, "3 cucharadas"),
        ("Sal fina", "al gusto"),
    ],
    "salsa brava": [
        ("Tomate frito", "150 g"),
        ("Pimentón dulce", "1 cucharadita"),
        ("Pimentón picante", "1/2 cucharadita"),
        ("Ajo", "1 diente"),
        (AOVE, "2 cucharadas"),
        ("Sal fina", "al gusto"),
    ],
}


def _norm_ing(name: str) -> str:
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def _pretty_sub_title(key: str, original: str) -> str:
    mapping = {
        "tomate frito": "Salsa brava",
        "alioli": "Alioli",
        "mayonesa": "Mayonesa",
        "mahonesa": "Mahonesa",
        "mojo verde": "Mojo verde",
        "mojo rojo": "Mojo rojo",
    }
    if key in mapping:
        return mapping[key]
    return original.strip() or key.title()


def _ensure_sub(bucket: dict[str, dict], key: str, title: str) -> dict:
    if key not in bucket:
        bucket[key] = {
            "title": title,
            "ingredients": [],
            "steps": [],
            "_seen": set(),
        }
    return bucket[key]


def _split_subrecipe(
    ings: list[tuple[str, str]],
    steps: list[tuple[str, str]],
    subings: list[tuple[str, str]] | None = None,
    substeps: list[tuple[str, str]] | None = None,
    subrecipes: list[dict] | None = None,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[dict]]:
    """Separa salsas/caldos/mojos en N subrecetas nombradas e independientes."""
    main_ings: list[tuple[str, str]] = []
    main_steps: list[tuple[str, str]] = []
    named: dict[str, dict] = {}

    # Subrecetas explícitas del autor del seed
    for sub in subrecipes or []:
        title = (sub.get("title") or "Subreceta").strip()
        key = _norm_ing(title)
        row = _ensure_sub(named, key, title)
        for name, qty in sub.get("ingredients") or []:
            nk = _norm_ing(name)
            if nk not in row["_seen"]:
                row["ingredients"].append((name, qty))
                row["_seen"].add(nk)
        for title_s, desc in sub.get("steps") or []:
            row["steps"].append((title_s, desc))

    # Legacy plano → una sola si no hay named aún
    if subings or substeps:
        row = _ensure_sub(named, "subreceta", "Subreceta")
        for name, qty in subings or []:
            nk = _norm_ing(name)
            if nk not in row["_seen"]:
                row["ingredients"].append((name, qty))
                row["_seen"].add(nk)
        for title_s, desc in substeps or []:
            row["steps"].append((title_s, desc))

    for name, qty in ings:
        key = _norm_ing(name)
        if _PREPARED_ING_RE.search(key):
            title = _pretty_sub_title(key, name)
            row = _ensure_sub(named, _norm_ing(title), title)
            expanded = _SUB_EXPANSIONS.get(key) or _SUB_EXPANSIONS.get(_norm_ing(title))
            if expanded:
                for ename, eqty in expanded:
                    ek = _norm_ing(ename)
                    if ek not in row["_seen"]:
                        row["ingredients"].append((ename, eqty))
                        row["_seen"].add(ek)
            else:
                if key not in row["_seen"]:
                    row["ingredients"].append((name, qty))
                    row["_seen"].add(key)
        else:
            main_ings.append((name, qty))

    for title, desc in steps:
        tkey = _norm_ing(title)
        if tkey in _SUB_STEP_TITLES:
            # Emparejar con subreceta existente o crear una con ese nombre
            match = None
            for k, row in named.items():
                if tkey in k or k in tkey or tkey == _norm_ing(row["title"]):
                    match = row
                    break
            if match is None and tkey == "salsas":
                # Paso genérico "Salsas": no duplicar; repartir hint en cada salsa si ya hay
                if named:
                    for row in named.values():
                        if not row["steps"]:
                            row["steps"].append((row["title"], desc))
                    continue
            if match is None:
                pretty = title if title.lower() != "salsas" else "Salsas"
                match = _ensure_sub(named, tkey, pretty)
            match["steps"].append((title, desc))
        else:
            main_steps.append((title, desc))

    # Si una subreceta tiene pasos pero no ingredientes → rellenar desde expansión
    # y sacar de la principal los que coincidan (ajo, yema, AOVE del alioli, etc.)
    for key, row in named.items():
        if row["ingredients"]:
            continue
        exp = _SUB_EXPANSIONS.get(key) or _SUB_EXPANSIONS.get(_norm_ing(row["title"]))
        if not exp:
            continue
        exp_keys = {_norm_ing(n) for n, _ in exp}
        # Preferir cantidades de la lista principal si ya estaban ahí
        moved: list[tuple[str, str]] = []
        kept_main: list[tuple[str, str]] = []
        for name, qty in main_ings:
            nk = _norm_ing(name)
            # Match exacto o "Huevos..." ↔ expansión huevos
            hit = nk in exp_keys or any(
                nk.startswith(ek) or ek.startswith(nk.split()[0]) for ek in exp_keys
            )
            # AOVE / aceite de oliva virgen extra
            if "aceite de oliva" in nk and any("aceite de oliva" in ek for ek in exp_keys):
                hit = True
            if hit:
                moved.append((name, qty))
                row["_seen"].add(nk)
            else:
                kept_main.append((name, qty))
        main_ings = kept_main
        if moved:
            row["ingredients"] = moved
        else:
            for ename, eqty in exp:
                ek = _norm_ing(ename)
                if ek not in row["_seen"]:
                    row["ingredients"].append((ename, eqty))
                    row["_seen"].add(ek)

    result_subs: list[dict] = []
    for row in named.values():
        if not row["ingredients"] and not row["steps"]:
            continue
        if row["ingredients"] and not row["steps"]:
            row["steps"].append(
                (
                    f"Preparar {row['title'].lower()}",
                    f"Prepara el {row['title'].lower()} con sus ingredientes y reserva "
                    f"para la receta principal.",
                )
            )
        result_subs.append(
            {
                "title": row["title"],
                "ingredients": row["ingredients"],
                "steps": _steps(*row["steps"]),
            }
        )

    return main_ings, main_steps, result_subs

AUTHORS = [
    ("Ana Cocina Local", "ana.100@local.sabores.es"),
    ("Carlos Chef Local", "carlos.100@local.sabores.es"),
    ("Lucía Fogones Local", "lucia.100@local.sabores.es"),
    ("Miguel Tapas Local", "miguel.100@local.sabores.es"),
    ("Sofía Mesa Local", "sofia.100@local.sabores.es"),
]

COMMENTERS = [
    ("Pedro Horno Local", "pedro.100@local.sabores.es"),
    ("Elena Mercado Local", "elena.100@local.sabores.es"),
    ("Javier Fogón Local", "javier.100@local.sabores.es"),
]


def _about(title: str, region: str, idea: str, tip: str) -> str:
    return (
        f"{title} es un plato representativo de {region}. {idea}\n\n"
        f"En esta versión de casa buscamos sabor limpio, tiempos realistas y "
        f"productos que puedas encontrar en el súper. Usa siempre {AOVE} cuando "
        f"pidamos sofrito o aliño en crudo: marca la diferencia frente a aceites "
        f"neutros.\n\n"
        f"Truco: {tip} Sirve caliente o a temperatura ambiente según indiquen los "
        f"pasos. Las cantidades son orientativas para 4 raciones; ajusta sal al final."
    )


def _steps(*pairs: tuple[str, str]) -> list[dict]:
    return [{"title": t, "description": d} for t, d in pairs]


# 100 platos: título, ccaa, typeeat, time, proteins, about_bits, ingredients, steps
def build_recipes() -> list[dict]:
    R: list[dict] = []

    def add(
        title,
        ccaa,
        typeeat,
        time,
        proteins,
        region,
        idea,
        tip,
        ings,
        steps,
        subings=None,
        substeps=None,
        subrecipes=None,
    ):
        main_ings, main_steps, named_subs = _split_subrecipe(
            ings, steps, subings, substeps, subrecipes
        )
        R.append(
            {
                "title": title,
                "ccaa": ccaa,
                "typeeat": typeeat,
                "time": time,
                "proteins": proteins,
                "description": _about(title, region, idea, tip),
                "ingredients": main_ings,
                "steps": _steps(*main_steps),
                "subrecipes": named_subs,
            }
        )

    # ——— Tortillas / huevo ———
    add(
        "Tortilla de patatas con cebolla",
        "castillaleon",
        "maindishes",
        "30a60",
        ["huevo", "vegetariana"],
        "Castilla y León",
        "Patata pochada despacio y huevo jugoso en el centro.",
        "Escurre muy bien la patata antes de mezclar con el huevo.",
        [
            ("Patatas monalisa", "700 g"),
            ("Huevos frescos M/L", "6 unidades"),
            ("Cebolla dulce", "1 mediana"),
            (AOVE, "250 ml para pochar"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Preparar", "Pela y corta las patatas en láminas de 2–3 mm y la cebolla en juliana."),
            ("Pochar", f"Pocha patata y cebolla en {AOVE} a fuego medio-bajo 20 min. Escurre."),
            ("Cuajar", "Mezcla con huevos batidos, cuaja en sartén y da la vuelta con un plato."),
        ],
    )
    add(
        "Tortilla de chorizo asturiano",
        "asturias",
        "maindishes",
        "15a30",
        ["huevo", "cerdo"],
        "Asturias",
        "Huevo cuajado con chorizo sofrito, ideal de tapa.",
        "No pases el chorizo: solo que suelte grasa y aroma.",
        [
            ("Huevos frescos M/L", "5 unidades"),
            ("Chorizo asturiano", "150 g"),
            (AOVE, "1 cucharada"),
            ("Sal fina", "una pizca"),
        ],
        [
            ("Sofrito", f"Dora el chorizo en rodajas con un hilo de {AOVE}."),
            ("Huevo", "Bate huevos, mezcla con el chorizo y cuaja a fuego medio-bajo."),
            ("Servir", "Cuaja al punto jugoso y sirve en triángulos."),
        ],
    )
    add(
        "Revuelto de setas y ajo",
        "castillaleon",
        "maindishes",
        "menos15",
        ["huevo", "vegetariana"],
        "Castilla y León",
        "Revuelto cremoso de setas salteadas con ajo laminado.",
        "Retira del fuego antes de que el huevo se seque del todo.",
        [
            ("Huevos frescos M/L", "4 unidades"),
            ("Champiñones", "300 g"),
            ("Ajo", "2 dientes"),
            (AOVE, "2 cucharadas"),
            ("Perejil fresco", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Setas", f"Saltea champiñones y ajo en {AOVE} hasta que suelten agua."),
            ("Revuelto", "Añade huevos batidos, remueve en crema y espolvorea perejil."),
        ],
    )

    # ——— Sopas / fríos ———
    add(
        "Gazpacho andaluz clásico",
        "andalucia",
        "soups",
        "menos15",
        ["vegana", "vegetariana"],
        "Andalucía",
        "Sopa fría de tomate, pimiento, pepino y ajo.",
        "Enfría al menos 1 hora; rectifica vinagre y sal en frío.",
        [
            ("Tomates maduros", "1 kg"),
            ("Pimiento verde italiano", "1"),
            ("Pepino", "1/2"),
            ("Ajo", "1 diente"),
            ("Pan de barra", "40 g"),
            (AOVE, "80 ml"),
            ("Vinagre de Jerez", "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Triturar", f"Tritura verduras, pan, {AOVE}, vinagre y sal hasta fineza."),
            ("Reposar", "Pasa por chino, enfría y sirve con picadillo."),
        ],
    )
    add(
        "Salmorejo cordobés",
        "andalucia",
        "soups",
        "menos15",
        ["huevo"],
        "Córdoba",
        "Crema fría espesa de tomate y pan, con huevo y jamón.",
        "El pan debe estar bien remojado para emulsionar.",
        [
            ("Tomates maduros", "1 kg"),
            ("Pan de barra", "200 g"),
            ("Ajo", "1 diente"),
            (AOVE, "100 ml"),
            ("Vinagre de Jerez", "1 cucharada"),
            ("Huevos frescos M/L", "2 cocidos"),
            ("Jamón serrano", "80 g"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Emulsión", f"Tritura tomate, pan, ajo, vinagre, sal y {AOVE} hasta crema."),
            ("Montaje", "Sirve frío con huevo picado y jamón en tiras."),
        ],
    )
    add(
        "Ajoblanco malagueño",
        "andalucia",
        "soups",
        "menos15",
        ["vegana", "vegetariana"],
        "Málaga",
        "Crema fría de almendras, ajo y pan, con uvas.",
        "Si queda espeso, aligera con agua muy fría.",
        [
            ("Almendras crudas", "150 g"),
            ("Pan de barra", "80 g"),
            ("Ajo", "1 diente"),
            (AOVE, "80 ml"),
            ("Vinagre de Jerez", "1 cucharada"),
            ("Uvas blancas", "12 unidades"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Triturar", f"Hydrata pan, tritura con almendras, ajo, {AOVE}, vinagre y sal."),
            ("Servir", "Enfría y corona con uvas frescas."),
        ],
    )

    # ——— Arroces ———
    add(
        "Paella valenciana de pollo y conejo",
        "comunidadvalenciana",
        "maindishes",
        "mas60",
        ["pollo", "conejo"],
        "Comunidad Valenciana",
        "Arroz seco en paella con pollo, conejo y bajo.",
        "No remuevas el arroz tras añadir el caldo.",
        [
            ("Arroz bomba (o D.O. Valencia)", "400 g"),
            ("Pollo en trozos", "400 g"),
            ("Conejo en trozos", "300 g"),
            ("Judía verde", "150 g"),
            ("Garrofón", "100 g"),
            ("Tomate natural", "1 rallado"),
            (AOVE, "80 ml"),
            ("Azafrán", "una pizca"),
            ("Sal fina", "al gusto"),
            ("Agua", "1,2 l"),
        ],
        [
            ("Dorar", f"Dora pollo y conejo en {AOVE}. Sofríe judía, garrofón y tomate."),
            ("Caldo", "Cubre con agua, sazona y cuece 20 min. Incorpora azafrán."),
            ("Arroz", "Añade arroz en cruz, distribuye y cuece 18 min sin remover. Reposa."),
        ],
    )
    add(
        "Arroz a banda alicantino",
        "comunidadvalenciana",
        "maindishes",
        "30a60",
        ["pescado"],
        "Alicante",
        "Arroz seco con fumet de pescado y ñora.",
        "El caldo debe estar muy sabroso antes del arroz.",
        [
            ("Arroz bomba (o D.O. Valencia)", "350 g"),
            ("Caldo de pescado", "1 l"),
            ("Ñora", "1"),
            ("Ajo", "2 dientes"),
            ("Tomate natural", "1/2 rallado"),
            (AOVE, "60 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe ajo y carne de ñora en {AOVE}, añade tomate."),
            ("Arroz", "Incorpora arroz, sofríe 1 min y cubre con caldo hirviendo 18 min."),
        ],
    )
    add(
        "Arroz negro con calamar",
        "cataluna",
        "maindishes",
        "30a60",
        ["pescado"],
        "Cataluña / Levante",
        "Arroz con tinta de calamar y sofrito suave.",
        "Añade la tinta disuelta en un poco de caldo.",
        [
            ("Arroz bomba (o D.O. Valencia)", "350 g"),
            ("Calamar limpio", "400 g"),
            ("Tinta de calamar", "2 sobres"),
            ("Cebolla", "1"),
            ("Tomate natural", "1"),
            (AOVE, "60 ml"),
            ("Ajo", "2 dientes"),
            ("Caldo de pescado", "1 l"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla y ajo en {AOVE}, añade tomate y calamar."),
            ("Arroz", "Añade arroz y tinta, cubre con caldo y cuece 18 min."),
        ],
    )
    add(
        "Risotto de setas al estilo español",
        "cataluna",
        "maindishes",
        "30a60",
        ["vegetariana"],
        "cocina de fusión casera",
        "Arroz cremoso con setas y un toque de {AOVE}.".format(AOVE=AOVE),
        "Añade el caldo en cacitos removiendo.",
        [
            ("Arroz bomba (o D.O. Valencia)", "300 g"),
            ("Champiñones", "250 g"),
            ("Cebolla", "1/2"),
            ("Caldo de verduras", "1 l"),
            (AOVE, "3 cucharadas"),
            ("Mantequilla", "20 g"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Setas", f"Saltea setas y reserva. Sofríe cebolla en {AOVE}."),
            ("Cremoso", "Tuesta arroz, añade caldo poco a poco. Termina con setas y mantequilla."),
        ],
    )

    # ——— Pescados / mariscos ———
    add(
        "Pulpo a la gallega",
        "galicia",
        "maindishes",
        "mas60",
        ["pescado"],
        "Galicia",
        "Pulpo tierno con cachelos, pimentón y aceite.",
        "Congela el pulpo antes o cuécelo tras un ‘asustado’.",
        [
            ("Pulpo limpio", "1,5 kg"),
            ("Patatas", "800 g"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Pimentón picante", "1/2 cucharadita"),
            ("Sal gruesa", "al gusto"),
            (AOVE, "chorro generoso"),
        ],
        [
            ("Cocción", "Cuece el pulpo 40–50 min. Cuece patatas en la misma agua."),
            ("Emplatado", f"Corta pulpo, monta con patata, sal, pimentón y {AOVE} en crudo."),
        ],
    )
    add(
        "Bacalao al pil-pil",
        "paisvasco",
        "maindishes",
        "30a60",
        ["pescado"],
        "País Vasco",
        "Bacalao confitado emulsionando el aceite con la gelatina del pescado.",
        "El fuego debe ser muy suave al emulsionar.",
        [
            ("Lomos de bacalao desalado", "4"),
            ("Ajo", "4 dientes"),
            ("Guindilla", "1"),
            (AOVE, "250 ml"),
        ],
        [
            ("Confitado", f"Dora ajos y guindilla en {AOVE}, confita el bacalao piel abajo."),
            ("Emulsión", "Retira el bacalao y mueve la cazuela en círculos hasta ligar el pil-pil."),
        ],
    )
    add(
        "Merluza en salsa verde",
        "paisvasco",
        "maindishes",
        "30a60",
        ["pescado"],
        "País Vasco",
        "Merluza con salsa de perejil, ajo y un toque de vino.",
        "No hiervas la salsa a lo loco: debe espesar suave.",
        [
            ("Merluza", "4 rodajas"),
            ("Ajo", "3 dientes"),
            ("Perejil fresco", "1 manojo"),
            ("Harina de trigo", "1 cucharada"),
            ("Vino blanco", "100 ml"),
            (AOVE, "4 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Salsa", f"Sofríe ajo en {AOVE}, añade harina, vino y perejil picado."),
            ("Pescado", "Pocha la merluza en la salsa 8–10 min y sirve con cucharón."),
        ],
    )
    add(
        "Sardinas a la plancha con limón",
        "galicia",
        "maindishes",
        "menos15",
        ["pescado"],
        "costa atlántica",
        "Sardinas plancha con piel crujiente y limón.",
        "La plancha debe estar muy caliente y las sardinas secas.",
        [
            ("Sardinas frescas", "1 kg"),
            ("Limón", "2"),
            (AOVE, "2 cucharadas"),
            ("Sal gruesa", "al gusto"),
            ("Perejil fresco", "al gusto"),
        ],
        [
            ("Plancha", f"Unta sardinas con {AOVE} y sal. Hazlas 2–3 min por lado."),
            ("Aliño", "Sirve con limón en gajos y perejil."),
        ],
    )
    add(
        "Mejillones al vapor con vino blanco",
        "galicia",
        "starters",
        "menos15",
        ["pescado"],
        "Galicia",
        "Mejillones abiertos al vapor con cebolla y vino.",
        "Descarta los que no se abran.",
        [
            ("Mejillones", "1,5 kg"),
            ("Cebolla", "1"),
            ("Ajo", "2 dientes"),
            ("Vino blanco", "150 ml"),
            (AOVE, "2 cucharadas"),
            ("Perejil fresco", "2 cucharadas"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla y ajo en {AOVE}, añade vino y mejillones."),
            ("Vapor", "Tapa 5–7 min, espolvorea perejil y sirve."),
        ],
    )
    add(
        "Gambas al ajillo",
        "castillalamancha",
        "starters",
        "menos15",
        ["pescado"],
        "Castilla-La Mancha / Madrid",
        "Gambas salteadas con ajo y guindilla en cazuelita.",
        "No pases las gambas: 1–2 minutos bastan.",
        [
            ("Gambas", "400 g"),
            ("Ajo", "6 dientes"),
            ("Guindilla", "1"),
            (AOVE, "100 ml"),
            ("Sal fina", "al gusto"),
            ("Pan de barra", "para acompañar"),
        ],
        [
            ("Ajillo", f"Calienta {AOVE} con ajo y guindilla sin quemar."),
            ("Gambas", "Añade gambas, saltea 2 min y sirve hirviendo con pan."),
        ],
    )
    add(
        "Calamares a la romana",
        "madrid",
        "starters",
        "15a30",
        ["pescado"],
        "Madrid",
        "Anillas rebozadas crujientes con limón.",
        "La masa debe quedar ligera; fríe en aceite caliente.",
        [
            ("Calamar limpio", "600 g"),
            ("Harina de trigo", "150 g"),
            ("Huevos frescos M/L", "2"),
            ("Limón", "1"),
            ("Aceite de oliva suave", "para freír"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Rebozado", "Pasa anillas por harina y huevo batido."),
            ("Fritura", "Fríe en tandas, escurre y sirve con limón."),
        ],
    )
    add(
        "Boquerones en vinagre",
        "andalucia",
        "starters",
        "mas60",
        ["pescado"],
        "Andalucía",
        "Boquerones marinados en vinagre con ajo y perejil.",
        "El marinaje pide horas en nevera.",
        [
            ("Boquerones limpios", "500 g"),
            ("Vinagre de vino", "250 ml"),
            ("Ajo", "3 dientes"),
            ("Perejil fresco", "2 cucharadas"),
            (AOVE, "80 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Marinar", "Cubre boquerones con vinagre y sal 3–4 h en frío."),
            ("Aliñar", f"Escurre, aliña con ajo, perejil y {AOVE}."),
        ],
    )

    # ——— Carnes ———
    add(
        "Pollo al ajillo castellano",
        "castillaleon",
        "maindishes",
        "30a60",
        ["pollo"],
        "Castilla y León",
        "Pollo dorado con ajos enteros y vino blanco.",
        "Dora bien la piel antes de añadir líquidos.",
        [
            ("Pollo en trozos", "1,2 kg"),
            ("Ajo", "1 cabeza"),
            ("Vino blanco", "150 ml"),
            (AOVE, "4 cucharadas"),
            ("Laurel", "2 hojas"),
            ("Sal fina", "al gusto"),
            ("Pimienta negra", "al gusto"),
        ],
        [
            ("Dorar", f"Dora el pollo en {AOVE}. Añade ajos enteros y laurel."),
            ("Brasear", "Riega con vino, tapa y cuece 25–30 min a fuego medio."),
        ],
    )
    add(
        "Conejo al ajillo",
        "castillalamancha",
        "maindishes",
        "30a60",
        ["conejo"],
        "Castilla-La Mancha",
        "Conejo guisado con ajo y un toque de guindilla.",
        "Sella bien las piezas para que no se sequen.",
        [
            ("Conejo en trozos", "1 conejo"),
            ("Ajo", "8 dientes"),
            ("Guindilla", "1"),
            ("Vino blanco", "100 ml"),
            (AOVE, "4 cucharadas"),
            ("Perejil fresco", "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sellar", f"Dora el conejo en {AOVE}. Añade ajo y guindilla."),
            ("Guiso", "Riega con vino, tapa 30 min y termina con perejil."),
        ],
    )
    add(
        "Chuletón a la brasa con pimientos",
        "paisvasco",
        "maindishes",
        "15a30",
        ["vacuno"],
        "País Vasco",
        "Chuletón a la parrilla con pimientos asados.",
        "Sala después de la brasa, no antes.",
        [
            ("Chuletón de vacuno", "1 kg"),
            ("Pimientos rojos", "3"),
            (AOVE, "2 cucharadas"),
            ("Sal gruesa", "al gusto"),
        ],
        [
            ("Pimientos", f"Asa pimientos, pela y aliña con {AOVE} y sal."),
            ("Carne", "Haz el chuletón a la brasa al punto, sala y reposa 5 min."),
        ],
    )
    add(
        "Albóndigas en salsa de almendras",
        "comunidadvalenciana",
        "maindishes",
        "30a60",
        ["vacuno", "cerdo"],
        "Comunidad Valenciana",
        "Albóndigas jugosas con picada de almendra y pan.",
        "La picada se añade al final para espesar.",
        [
            ("Carne picada mixta", "500 g"),
            ("Huevos frescos M/L", "1"),
            ("Pan rallado", "40 g"),
            ("Almendras crudas", "50 g"),
            ("Ajo", "2 dientes"),
            ("Tomate frito", "200 g"),
            (AOVE, "3 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Albóndigas", "Mezcla carne, huevo, pan y sal; forma bolas y dora."),
            ("Salsa", f"Sofríe ajo en {AOVE}, añade tomate y albóndigas. Ligar con almendra picada."),
        ],
    )
    add(
        "Callos a la madrileña",
        "madrid",
        "maindishes",
        "mas60",
        ["vacuno"],
        "Madrid",
        "Guiso largo de callos con chorizo y morcilla.",
        "Paciencia: el colágeno necesita tiempo.",
        [
            ("Callos de ternera", "1 kg"),
            ("Chorizo", "150 g"),
            ("Morcilla", "150 g"),
            ("Cebolla", "1"),
            ("Pimentón dulce", "1 cucharada"),
            ("Tomate natural", "1"),
            (AOVE, "3 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla en {AOVE}, añade pimentón y tomate."),
            ("Guiso", "Incorpora callos y embutidos; cuece suave 2–3 h."),
        ],
    )
    add(
        "Cordero asado al estilo de Aranda",
        "castillaleon",
        "maindishes",
        "mas60",
        ["cordero"],
        "Castilla y León",
        "Cuarto de cordero asado lento con agua y manteca/aceite.",
        "Horno moderado y bandeja con un dedo de agua.",
        [
            ("Pierna de cordero", "1,5 kg"),
            ("Manteca de cerdo", "40 g"),
            ("Agua", "200 ml"),
            ("Sal fina", "al gusto"),
            ("Romero fresco", "2 ramitas"),
        ],
        [
            ("Preparar", "Sala el cordero, unta manteca y pon romero."),
            ("Asar", "Horno 160–170 ºC unas 2 h, regando el jugo."),
        ],
    )
    add(
        "Carrillada ibérica al vino tinto",
        "extremadura",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Extremadura",
        "Carrilleras melosas braseadas con vino y verduras.",
        "El punto final es que se partan con cuchara.",
        [
            ("Carrilleras ibéricas", "800 g"),
            ("Cebolla", "2"),
            ("Zanahoria", "2"),
            ("Vino tinto", "400 ml"),
            (AOVE, "4 cucharadas"),
            ("Harina de trigo", "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sellar", f"Enharina y sella carrilleras en {AOVE}. Reserva."),
            ("Brasear", "Pocha verduras, añade vino y carne; 2 h a fuego suave."),
        ],
    )

    # ——— Verduras / legumbres ———
    add(
        "Pisto manchego",
        "castillalamancha",
        "maindishes",
        "30a60",
        ["vegetariana", "vegana"],
        "Castilla-La Mancha",
        "Verduras confitadas en aceite: calabacín, pimiento, tomate y cebolla.",
        "Cada verdura se añade en su tiempo para no hacer puré.",
        [
            ("Calabacín", "2"),
            ("Pimiento rojo", "1"),
            ("Pimiento verde", "1"),
            ("Cebolla", "1"),
            ("Tomate natural", "4"),
            ("Ajo", "2 dientes"),
            (AOVE, "100 ml"),
            ("Sal fina", "al gusto"),
            ("Huevos frescos M/L", "opcionales para servir"),
        ],
        [
            ("Sofrito", f"Pochar cebolla y ajo en {AOVE}. Añade pimientos y calabacín."),
            ("Tomate", "Incorpora tomate y reduce 20–25 min. Sirve con huevo frito si quieres."),
        ],
    )
    add(
        "Escalivada catalana",
        "cataluna",
        "starters",
        "30a60",
        ["vegana", "vegetariana"],
        "Cataluña",
        "Berenjena, pimiento y cebolla asados y aliñados.",
        "Asar hasta piel chamuscada para pelar fácil.",
        [
            ("Berenjenas", "2"),
            ("Pimientos rojos", "3"),
            ("Cebollas", "2"),
            (AOVE, "4 cucharadas"),
            ("Vinagre de vino", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Asar", "Asa verduras enteras 45–60 min a 200 ºC."),
            ("Aliñar", f"Pela, corta en tiras y aliña con {AOVE}, vinagre y sal."),
        ],
    )
    add(
        "Espínacas con garbanzos a la andaluza",
        "andalucia",
        "maindishes",
        "30a60",
        ["vegana", "vegetariana"],
        "Andalucía",
        "Garbanzos con espinacas, ajo y pimentón.",
        "El pan frito en la salsa da cuerpo.",
        [
            ("Garbanzos cocidos", "400 g"),
            ("Espinacas frescas", "300 g"),
            ("Ajo", "3 dientes"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Comino", "1/2 cucharadita"),
            ("Pan de barra", "2 rebanadas"),
            (AOVE, "4 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Majado", f"Dora pan y ajo en {AOVE}, majá con pimentón y comino."),
            ("Guiso", "Añade garbanzos y espinacas; reduce 10 min."),
        ],
    )
    add(
        "Lentejas estofadas con chorizo",
        "castillaleon",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Castilla y León",
        "Lentejas con verdura de cuchara y chorizo.",
        "No añadas sal al principio si el chorizo es muy curado.",
        [
            ("Lentejas", "400 g"),
            ("Chorizo", "150 g"),
            ("Cebolla", "1"),
            ("Zanahoria", "2"),
            ("Patata", "1"),
            ("Pimentón dulce", "1 cucharadita"),
            (AOVE, "2 cucharadas"),
            ("Laurel", "1 hoja"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe verduras y chorizo en {AOVE}, añade pimentón."),
            ("Cocción", "Cubre lentejas con agua y cuece 45–60 min."),
        ],
    )
    add(
        "Fabada asturiana",
        "asturias",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Asturias",
        "Fabes mantecosas con compango (chorizo, morcilla, tocino).",
        "Remojo de fabes y cocción muy suave sin romperlas.",
        [
            ("Fabes de la Granja", "500 g"),
            ("Chorizo asturiano", "2"),
            ("Morcilla asturiana", "2"),
            ("Tocino", "150 g"),
            ("Cebolla", "1"),
            ("Azafrán", "una hebra"),
            ("Sal fina", "al final"),
        ],
        [
            ("Cocer", "Cuece fabes con cebolla y tocino a fuego mínimo."),
            ("Compango", "Añade chorizo y morcilla a media cocción; 2–3 h total."),
        ],
    )
    add(
        "Potaje de vigilia con bacalao",
        "madrid",
        "maindishes",
        "mas60",
        ["pescado", "vegetariana"],
        "Madrid",
        "Garbanzos con espinacas y bacalao desalado.",
        "Desala el bacalao con cambios de agua previos.",
        [
            ("Garbanzos", "400 g"),
            ("Lomos de bacalao desalado", "300 g"),
            ("Espinacas frescas", "200 g"),
            ("Cebolla", "1"),
            ("Tomate natural", "1"),
            ("Pimentón dulce", "1 cucharadita"),
            (AOVE, "3 cucharadas"),
            ("Huevos frescos M/L", "2 cocidos"),
        ],
        [
            ("Base", f"Sofríe cebolla y tomate en {AOVE}, añade pimentón y garbanzos."),
            ("Bacalao", "Incorpora bacalao y espinacas 15 min. Sirve con huevo."),
        ],
    )
    add(
        "Patatas a la importancia",
        "castillaleon",
        "maindishes",
        "30a60",
        ["vegetariana", "huevo"],
        "Castilla y León",
        "Patatas rebozadas en salsa de ajo y vino blanco.",
        "La salsa debe ligar sin romper las patatas.",
        [
            ("Patatas", "1 kg"),
            ("Huevos frescos M/L", "2"),
            ("Harina de trigo", "80 g"),
            ("Ajo", "3 dientes"),
            ("Vino blanco", "100 ml"),
            ("Caldo de verduras", "400 ml"),
            (AOVE, "para freír y sofrito"),
            ("Perejil fresco", "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Rebozar", "Corta patatas en rodajas, pasa por harina y huevo; fríe."),
            ("Salsa", f"Sofríe ajo, añade vino, caldo y patatas; 15 min con perejil."),
        ],
    )
    add(
        "Patatas bravas con alioli",
        "cataluna",
        "starters",
        "30a60",
        ["vegetariana", "huevo"],
        "Barcelona / Madrid",
        "Patatas fritas con salsa brava y alioli suave.",
        "Doble fritura: primero a 150 ºC y luego a 180 ºC.",
        [
            ("Patatas", "1 kg"),
            ("Aceite de oliva suave", "para freír"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Patatas", "Corta en dados, fríe en dos tiempos y sala. Sirve con las salsas aparte."),
        ],
        subrecipes=[
            {
                "title": "Salsa brava",
                "ingredients": [
                    ("Tomate frito", "150 g"),
                    ("Pimentón dulce", "1 cucharadita"),
                    ("Pimentón picante", "1/2 cucharadita"),
                    ("Ajo", "1 diente"),
                    (AOVE, "2 cucharadas"),
                    ("Sal fina", "al gusto"),
                ],
                "steps": [
                    (
                        "Brava",
                        f"Sofríe el ajo en {AOVE}, añade tomate y pimentones; reduce 5 min y sala.",
                    ),
                ],
            },
            {
                "title": "Alioli",
                "ingredients": [
                    ("Ajo", "2 dientes"),
                    ("Huevos frescos M/L", "1 yema"),
                    (AOVE, "150 ml"),
                    ("Sal fina", "al gusto"),
                ],
                "steps": [
                    (
                        "Emulsión",
                        f"Machaca el ajo con sal, incorpora la yema y emulsioná con {AOVE} en hilo fino.",
                    ),
                ],
            },
        ],
    )
    add(
        "Pimientos del piquillo rellenos de bacalao",
        "navarra",
        "maindishes",
        "30a60",
        ["pescado"],
        "Navarra",
        "Piquillos rellenos con brandada suave de bacalao.",
        "Escurre bien los pimientos de bote.",
        [
            ("Pimientos del piquillo", "12"),
            ("Lomos de bacalao desalado", "300 g"),
            ("Cebolla", "1"),
            ("Harina de trigo", "2 cucharadas"),
            ("Leche", "200 ml"),
            (AOVE, "3 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Relleno", f"Pochar cebolla en {AOVE}, añade bacalao desmenuzado y bechamel ligera."),
            ("Horno", "Rellena piquillos, napar con salsa y gratinar 10 min."),
        ],
    )

    # ——— Pan / harinas / postres ———
    add(
        "Torrijas de Semana Santa",
        "madrid",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "Madrid",
        "Pan empapado en leche, rebozado y frito con canela.",
        "El pan del día anterior absorbe mejor sin romperse.",
        [
            ("Pan de molde brioche o barra", "1 barra"),
            ("Leche entera", "750 ml"),
            ("Azúcar", "120 g"),
            ("Canela", "1 rama + molida"),
            ("Piel de limón", "1"),
            ("Huevos frescos M/L", "3"),
            ("Aceite de oliva suave", "para freír"),
        ],
        [
            ("Leche", "Hierve leche con azúcar, canela y piel de limón; enfría un poco."),
            ("Freír", "Empapa pan, pasa por huevo y fríe. Espolvorea azúcar y canela."),
        ],
    )
    add(
        "Crema catalana",
        "cataluna",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "Cataluña",
        "Crema pastelera aromatizada con limón y canela, azúcar quemado.",
        "No hiervas tras añadir yemas o cortarás la crema.",
        [
            ("Leche entera", "500 ml"),
            ("Yemas de huevo", "4"),
            ("Azúcar", "100 g + para gratinar"),
            ("Maicena", "20 g"),
            ("Piel de limón", "1"),
            ("Canela", "1 rama"),
        ],
        [
            ("Infusionar", "Hierve leche con limón y canela; retira."),
            ("Crema", "Liga yemas, azúcar y maicena; cuece suave. Gratina el azúcar al servir."),
        ],
    )
    add(
        "Flan de huevo casero",
        "comunidadvalenciana",
        "desserts",
        "mas60",
        ["vegetariana", "huevo"],
        "toda España",
        "Flan al baño María con caramelo.",
        "Horno suave y baño María para textura sedosa.",
        [
            ("Huevos frescos M/L", "5"),
            ("Leche entera", "500 ml"),
            ("Azúcar", "120 g + 80 g caramelo"),
            ("Piel de limón", "opcional"),
        ],
        [
            ("Caramelo", "Hace caramelo seco y forra el molde."),
            ("Hornear", "Mezcla huevos, leche y azúcar; baño María 40–50 min a 170 ºC."),
        ],
    )
    add(
        "Arroz con leche asturiano",
        "asturias",
        "desserts",
        "mas60",
        ["vegetariana"],
        "Asturias",
        "Arroz cremoso en leche con canela y limón.",
        "Remueve a menudo para que no se pegue.",
        [
            ("Arroz redondo", "150 g"),
            ("Leche entera", "1,5 l"),
            ("Azúcar", "120 g"),
            ("Canela", "1 rama"),
            ("Piel de limón", "1"),
            ("Mantequilla", "10 g"),
        ],
        [
            ("Cocción", "Cuece arroz en leche con canela y limón a fuego bajo 1 h."),
            ("Acabar", "Añade azúcar y mantequilla; enfría con canela molida."),
        ],
    )
    add(
        "Churros con chocolate",
        "madrid",
        "desserts",
        "30a60",
        ["vegetariana"],
        "Madrid",
        "Masa de churro frita con chocolate a la taza.",
        "La masa debe estar caliente al churrera.",
        [
            ("Harina de trigo", "250 g"),
            ("Agua", "250 ml"),
            ("Sal fina", "1 pizca"),
            ("Aceite de oliva suave", "para freír"),
            ("Chocolate a la taza", "200 g"),
            ("Leche entera", "400 ml"),
            ("Azúcar", "al gusto"),
            ("Maicena", "1 cucharada"),
        ],
        [
            ("Masa", "Hierve agua con sal, añade harina de golpe y trabaja."),
            ("Freír y chocolate", "Churros en aceite caliente; chocolate con leche y maicena."),
        ],
    )
    add(
        "Bizcocho de yogur",
        "comunidadvalenciana",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "toda España",
        "Bizcocho esponjoso medido con el vasito de yogur.",
        "No abras el horno los primeros 25 minutos.",
        [
            ("Yogur natural", "1"),
            ("Huevos frescos M/L", "3"),
            ("Azúcar", "2 vasitos"),
            ("Harina de trigo", "3 vasitos"),
            ("Aceite de oliva suave", "1 vasito"),
            ("Levadura química", "1 sobre"),
            ("Piel de limón", "1"),
        ],
        [
            ("Masa", "Mezcla líquidos y luego harina con levadura y limón."),
            ("Horno", "180 ºC unos 40 min; comprueba con palillo."),
        ],
    )
    add(
        "Leche frita",
        "castillaleon",
        "desserts",
        "mas60",
        ["vegetariana", "huevo"],
        "Castilla y León",
        "Crema cuajada empanada y frita con canela.",
        "Enfría la crema bien antes de cortar.",
        [
            ("Leche entera", "750 ml"),
            ("Azúcar", "120 g"),
            ("Maicena", "80 g"),
            ("Canela", "1 rama + molida"),
            ("Piel de limón", "1"),
            ("Huevos frescos M/L", "2"),
            ("Harina de trigo", "para rebozar"),
            ("Aceite de oliva suave", "para freír"),
        ],
        [
            ("Crema", "Cuece leche, azúcar, maicena, limón y canela hasta espesar; enfría."),
            ("Freír", "Corta cuadrados, reboza en harina y huevo, fríe y espolvorea canela."),
        ],
    )

    # ——— Más variedad regional ———
    add(
        "Cocido madrileño",
        "madrid",
        "maindishes",
        "mas60",
        ["cerdo", "vacuno", "garbanzos"],
        "Madrid",
        "Tres vuelcos: sopa, garbanzos-verdura y carnes.",
        "Espuma al principio y cuece horas a fuego mínimo.",
        [
            ("Garbanzos", "400 g"),
            ("Morcillo de ternera", "400 g"),
            ("Pollo en trozos", "1/4"),
            ("Chorizo", "1"),
            ("Morcilla", "1"),
            ("Panceta", "150 g"),
            ("Patatas", "3"),
            ("Zanahoria", "2"),
            ("Repollo", "1/4"),
            ("Fideos", "80 g"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Caldo", "Cuece carnes y garbanzos 2–3 h. Añade verduras al final."),
            ("Vuelcos", "Sopa con fideos; luego garbanzos y verdura; después carnes."),
        ],
    )
    add(
        "Cachopo asturiano",
        "asturias",
        "maindishes",
        "30a60",
        ["vacuno", "cerdo"],
        "Asturias",
        "Filetes empanados rellenos de jamón y queso.",
        "Sella bordes para que no se escape el queso.",
        [
            ("Filetes de ternera", "4 finos"),
            ("Jamón serrano", "4 lonchas"),
            ("Queso semicurado", "4 lonchas"),
            ("Huevos frescos M/L", "2"),
            ("Harina de trigo", "80 g"),
            ("Pan rallado", "120 g"),
            ("Aceite de oliva suave", "para freír"),
        ],
        [
            ("Relleno", "Monta filete + jamón + queso + filete; reboza."),
            ("Fritura", "Fríe a 170 ºC hasta dorado; escurre sobre papel."),
        ],
    )
    add(
        "Empanada gallega de atún",
        "galicia",
        "maindishes",
        "mas60",
        ["pescado"],
        "Galicia",
        "Masa de pan rellena de sofrito y atún.",
        "El sofrito debe estar frío al rellenar.",
        [
            ("Harina de trigo", "500 g"),
            ("Levadura fresca", "20 g"),
            ("Atún en conserva", "400 g"),
            ("Cebolla", "3"),
            ("Pimiento rojo", "1"),
            ("Tomate natural", "2"),
            (AOVE, "100 ml"),
            ("Huevos frescos M/L", "1 para barnizar"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Masa y sofrito", f"Amasa harina y levadura. Sofríe cebolla, pimiento y tomate en {AOVE}; añade atún."),
            ("Horno", "Rellena, cierra, barniza con huevo y hornea 30–35 min a 200 ºC."),
        ],
    )
    add(
        "Empanadillas de pisto",
        "castillalamancha",
        "starters",
        "30a60",
        ["vegetariana"],
        "Castilla-La Mancha",
        "Empanadillas fritas o al horno rellenas de pisto.",
        "El relleno bien seco evita que se abran.",
        [
            ("Masa de empanadilla", "16 discos"),
            ("Calabacín", "1"),
            ("Pimiento verde", "1"),
            ("Cebolla", "1"),
            ("Tomate frito", "100 g"),
            (AOVE, "3 cucharadas"),
            ("Huevos frescos M/L", "1 para cerrar"),
        ],
        [
            ("Pisto", f"Haz pisto corto con verduras y {AOVE}; enfría."),
            ("Formar", "Rellena, sella con huevo y fríe u hornea."),
        ],
    )
    add(
        "Croquetas de jamón",
        "castillaleon",
        "starters",
        "mas60",
        ["cerdo", "huevo"],
        "toda España",
        "Bechamel firme con jamón, empanada y frita.",
        "Enfriar la masa toda la noche facilita el boleado.",
        [
            ("Jamón serrano", "150 g"),
            ("Harina de trigo", "80 g + rebozar"),
            ("Mantequilla", "80 g"),
            ("Leche entera", "750 ml"),
            ("Huevos frescos M/L", "2"),
            ("Pan rallado", "150 g"),
            ("Nuez moscada", "una pizca"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Bechamel", "Haz roux, añade leche y jamón; cuaja firme y enfría."),
            ("Freír", "Bola, reboza en harina-huevo-pan y fríe a 180 ºC."),
        ],
    )
    add(
        "Gazpachuelo malagueño",
        "andalucia",
        "soups",
        "30a60",
        ["pescado", "huevo"],
        "Málaga",
        "Sopa de pescado con mayonesa ligera al final.",
        "Templa la mayonesa con caldo para no cortarla.",
        [
            ("Merluza", "300 g"),
            ("Patatas", "3"),
            ("Huevos frescos M/L", "2"),
            (AOVE, "150 ml"),
            ("Limón", "1"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Caldo", "Cuece patata y merluza; reserva caldo y lascas."),
            ("Ligazón", f"Monta mayonesa con huevo, {AOVE} y limón; mezcla con caldo templado."),
        ],
    )
    add(
        "Marmitako de bonito",
        "paisvasco",
        "maindishes",
        "30a60",
        ["pescado"],
        "País Vasco",
        "Guiso de bonito con patata y pimiento.",
        "Añade el bonito al final para que no se seque.",
        [
            ("Bonito del norte", "600 g"),
            ("Patatas", "800 g"),
            ("Cebolla", "1"),
            ("Pimiento verde", "1"),
            ("Tomate natural", "1"),
            ("Ñora", "1"),
            (AOVE, "4 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Guiso", f"Sofríe verduras en {AOVE}, añade patata ‘chasqueada’ y agua."),
            ("Bonito", "Cuando la patata esté, incorpora bonito 5–8 min."),
        ],
    )
    add(
        "Txangurro a la donostiarra",
        "paisvasco",
        "maindishes",
        "30a60",
        ["pescado"],
        "San Sebastián",
        "Carne de centollo salteada con sofrito y gratinada.",
        "Usa el caparazón limpio para gratinar.",
        [
            ("Carne de centollo", "400 g"),
            ("Cebolla", "1"),
            ("Puerro", "1"),
            ("Tomate natural", "1"),
            ("Brandy", "40 ml"),
            (AOVE, "3 cucharadas"),
            ("Pan rallado", "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe verduras en {AOVE}, añade txangurro y brandy."),
            ("Gratén", "Rellena caparazones, pan rallado y gratinar."),
        ],
    )
    add(
        "Rabo de toro cordobés",
        "andalucia",
        "maindishes",
        "mas60",
        ["vacuno"],
        "Córdoba",
        "Rabo braseado con vino generoso y verduras.",
        "Escucha el colágeno: necesita horas.",
        [
            ("Rabo de toro", "1,5 kg"),
            ("Cebolla", "2"),
            ("Zanahoria", "2"),
            ("Puerro", "1"),
            ("Vino tinto", "500 ml"),
            (AOVE, "4 cucharadas"),
            ("Harina de trigo", "2 cucharadas"),
            ("Laurel", "2 hojas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sellar", f"Enharina y dora el rabo en {AOVE}."),
            ("Brasear", "Pochar verduras, vino y carne 3 h hasta meloso."),
        ],
    )
    add(
        "Olla podrida burgalesa",
        "castillaleon",
        "maindishes",
        "mas60",
        ["cerdo", "vacuno"],
        "Burgos",
        "Alubias con carnes variadas de matanza.",
        "Remojo de alubias y cocción lenta.",
        [
            ("Alubias rojas", "500 g"),
            ("Costilla de cerdo", "300 g"),
            ("Chorizo", "1"),
            ("Morcilla", "1"),
            ("Oreja de cerdo", "1"),
            ("Cebolla", "1"),
            ("Pimentón dulce", "1 cucharadita"),
            (AOVE, "2 cucharadas"),
        ],
        [
            ("Cocido", "Cuece alubias con carnes a fuego suave 2–3 h."),
            ("Pimentón", f"Sofríe cebolla con pimentón en {AOVE} y añade al puchero."),
        ],
    )
    add(
        "Migas extremeñas",
        "extremadura",
        "maindishes",
        "30a60",
        ["cerdo"],
        "Extremadura",
        "Pan desmigado con ajo, pimentón y torreznos.",
        "El pan debe estar duro y bien desmenuzado.",
        [
            ("Pan de barra duro", "500 g"),
            ("Ajo", "6 dientes"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Torreznos o panceta", "150 g"),
            ("Pimiento verde", "1"),
            (AOVE, "80 ml"),
            ("Agua", "un vaso"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Remojo", "Rocía el pan con agua con sal y deja reposar."),
            ("Sartén", f"Dora ajo y panceta en {AOVE}, añade pimentón, pimiento y migas hasta sueltas."),
        ],
    )
    add(
        "Gachas manchegas",
        "castillalamancha",
        "maindishes",
        "30a60",
        ["cerdo"],
        "Castilla-La Mancha",
        "Harina de almortas con tropezones de cerdo.",
        "Tuesta la harina sin quemarla.",
        [
            ("Harina de almortas", "200 g"),
            ("Panceta", "100 g"),
            ("Chorizo", "100 g"),
            ("Ajo", "4 dientes"),
            ("Pimentón dulce", "1 cucharadita"),
            (AOVE, "80 ml"),
            ("Agua", "1 l"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Tropezones", f"Dora ajo, panceta y chorizo en {AOVE}."),
            ("Gacha", "Añade pimentón y harina, tuesta y vierte agua removiendo hasta crema."),
        ],
    )
    add(
        "Caldereta de cordero",
        "extremadura",
        "maindishes",
        "mas60",
        ["cordero"],
        "Extremadura",
        "Cordero guisado con pimiento y un toque de hígado majado.",
        "Sella la carne a fuego fuerte primero.",
        [
            ("Cordero en trozos", "1,2 kg"),
            ("Cebolla", "2"),
            ("Pimiento rojo", "1"),
            ("Tomate natural", "2"),
            ("Ajo", "3 dientes"),
            ("Pimentón dulce", "1 cucharadita"),
            (AOVE, "5 cucharadas"),
            ("Vino blanco", "150 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sellar", f"Dora cordero en {AOVE}. Reserva."),
            ("Guiso", "Sofríe verduras, pimentón, vino y carne 1–1,5 h."),
        ],
    )
    add(
        "Fideuà de marisco",
        "comunidadvalenciana",
        "maindishes",
        "30a60",
        ["pescado"],
        "Gandía / Valencia",
        "Fideos tostados con caldo de marisco.",
        "Tuesta los fideos en la paella antes del caldo.",
        [
            ("Fideos nº 2", "350 g"),
            ("Gambas", "200 g"),
            ("Rape", "200 g"),
            ("Calamar limpio", "200 g"),
            ("Caldo de pescado", "1,1 l"),
            ("Ñora", "1"),
            ("Ajo", "2 dientes"),
            ("Tomate natural", "1/2"),
            (AOVE, "60 ml"),
        ],
        [
            ("Sofrito", f"Sofríe marisco y ñora en {AOVE}; reserva piezas nobles."),
            ("Fideos", "Tuesta fideos, añade caldo y cuece 10–12 min. Reposa."),
        ],
    )
    add(
        "Suquet de pescado",
        "cataluna",
        "maindishes",
        "30a60",
        ["pescado"],
        "Costa Brava",
        "Guiso de pescado de roca con patata y picada.",
        "La picada de almendra densifica el caldo.",
        [
            ("Rape", "300 g"),
            ("Gallos o merluza", "300 g"),
            ("Patatas", "4"),
            ("Tomate natural", "1"),
            ("Almendras crudas", "30 g"),
            ("Ajo", "2 dientes"),
            ("Pan de barra", "1 rebanada"),
            (AOVE, "4 cucharadas"),
            ("Perejil fresco", "2 cucharadas"),
        ],
        [
            ("Caldo", f"Sofríe tomate en {AOVE}, añade patata y agua/fumet."),
            ("Pescado y picada", "Añade pescado y majado de ajo-almendra-pan-perejil."),
        ],
    )
    add(
        "Escudella i carn d’olla",
        "cataluna",
        "maindishes",
        "mas60",
        ["vacuno", "cerdo"],
        "Cataluña",
        "Caldo catalán con pelota, garbanzos y carnes.",
        "Sirve caldo con galets y después la carn d’olla.",
        [
            ("Garbanzos", "300 g"),
            ("Morcillo de ternera", "400 g"),
            ("Pollo en trozos", "400 g"),
            ("Tocino", "150 g"),
            ("Patatas", "3"),
            ("Zanahoria", "2"),
            ("Col", "1/4"),
            ("Galets", "200 g"),
            ("Carne picada", "200 g para pelota"),
            ("Huevos frescos M/L", "1"),
            ("Pan rallado", "30 g"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Caldo", "Cuece carnes y garbanzos horas; añade verduras."),
            ("Pelota y pasta", "Forma pelota con carne y huevo; cuece. Galets en el caldo."),
        ],
    )
    add(
        "Canelones de San Esteban",
        "cataluna",
        "maindishes",
        "mas60",
        ["vacuno", "cerdo"],
        "Cataluña",
        "Canelones rellenos de carne asada picada con bechamel.",
        "La bechamel debe cubrir sin ahogar.",
        [
            ("Placas de canelón", "20"),
            ("Carne asada sobrante", "400 g"),
            ("Cebolla", "1"),
            ("Tomate natural", "1"),
            ("Harina de trigo", "50 g"),
            ("Mantequilla", "50 g"),
            ("Leche entera", "700 ml"),
            ("Queso rallado", "80 g"),
            (AOVE, "2 cucharadas"),
        ],
        [
            ("Relleno", f"Sofríe cebolla y tomate en {AOVE}, mezcla carne picada."),
            ("Montaje", "Rellena, nabé bechamel, queso y gratina."),
        ],
    )
    add(
        "Trinxat de la Cerdanya",
        "cataluna",
        "maindishes",
        "30a60",
        ["cerdo", "vegetariana"],
        "Pirineo catalán",
        "Col y patata chafadas con panceta crujiente.",
        "Escurre bien la col para que no aguado.",
        [
            ("Patatas", "800 g"),
            ("Col verde", "1/2"),
            ("Panceta", "150 g"),
            ("Ajo", "2 dientes"),
            (AOVE, "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cocer", "Cuece patata y col; escurre y chafa."),
            ("Dorar", f"Dora panceta y ajo en {AOVE}, mezcla con el trinxat."),
        ],
    )
    add(
        "Sopa de ajo castellana",
        "castillaleon",
        "soups",
        "15a30",
        ["huevo"],
        "Castilla y León",
        "Sopa de pan, ajo, pimentón y huevo pochado.",
        "El pimentón no debe quemarse.",
        [
            ("Pan de barra", "200 g"),
            ("Ajo", "5 dientes"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Huevos frescos M/L", "4"),
            ("Caldo de pollo o agua", "1,2 l"),
            (AOVE, "4 cucharadas"),
            ("Jamón serrano", "50 g opcional"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Base", f"Sofríe ajo y pan en {AOVE}, añade pimentón y caldo."),
            ("Huevos", "Pochar huevos en la sopa 3 min y servir."),
        ],
    )
    add(
        "Caldo gallego",
        "galicia",
        "soups",
        "mas60",
        ["cerdo"],
        "Galicia",
        "Caldo con grelos, patata y lacón o panceta.",
        "Los grelos se añaden al final.",
        [
            ("Grelos", "1 manojo"),
            ("Patatas", "4"),
            ("Alubias blancas", "200 g"),
            ("Lacón o panceta", "200 g"),
            ("Chorizo", "1"),
            (AOVE, "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cocido", "Cuece alubias con lacón y chorizo."),
            ("Grelos", "Añade patata y grelos 20–25 min."),
        ],
    )
    add(
        "Pote asturiano",
        "asturias",
        "soups",
        "mas60",
        ["cerdo"],
        "Asturias",
        "Potaje de berza con fabes y compango.",
        "Cocción larga y suave.",
        [
            ("Fabes", "400 g"),
            ("Berza", "1/2"),
            ("Patatas", "3"),
            ("Chorizo", "1"),
            ("Morcilla", "1"),
            ("Panceta", "100 g"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Base", "Cuece fabes con panceta."),
            ("Verdura", "Añade berza, patata y embutidos hasta tierno."),
        ],
    )
    add(
        "Pipirrana jaenera",
        "andalucia",
        "starters",
        "menos15",
        ["vegana", "vegetariana"],
        "Jaén",
        "Ensalada de tomate, pimiento, cebolla y pepino con aceite.",
        "Usa tomates muy maduros y buen aceite.",
        [
            ("Tomates maduros", "4"),
            ("Pimiento verde", "1"),
            ("Cebolla dulce", "1/2"),
            ("Pepino", "1/2"),
            ("Huevos frescos M/L", "1 cocido opcional"),
            (AOVE, "4 cucharadas"),
            ("Vinagre de vino", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cortar", "Pica todo en dados pequeños."),
            ("Aliñar", f"Aliña con {AOVE}, vinagre y sal; reposa 10 min."),
        ],
    )
    add(
        "Ensaladilla rusa",
        "madrid",
        "starters",
        "30a60",
        ["huevo", "pescado"],
        "toda España",
        "Patata, zanahoria, guisante y mayonesa con atún.",
        "Enfría los ingredientes antes de mayonesar.",
        [
            ("Patatas", "4"),
            ("Zanahoria", "2"),
            ("Guisantes", "150 g"),
            ("Huevos frescos M/L", "3"),
            ("Atún en conserva", "160 g"),
            ("Aceitunas", "50 g"),
            (AOVE, "200 ml para mayonesa"),
            ("Limón", "1/2"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cocidos", "Cuece verduras y huevos; corta y mezcla con atún."),
            ("Mayonesa", f"Emulsiona yema con {AOVE} y limón; liga la ensaladilla."),
        ],
    )
    add(
        "Tosta de sobrasada y miel",
        "islasbaleares",
        "starters",
        "menos15",
        ["cerdo"],
        "Baleares",
        "Pan tostado con sobrasada y chorrito de miel.",
        "Horno fuerte solo para fundir.",
        [
            ("Pan de barra", "4 rebanadas"),
            ("Sobrasada", "120 g"),
            ("Miel", "2 cucharadas"),
            (AOVE, "1 cucharada"),
        ],
        [
            ("Tostar", f"Unta pan con {AOVE} y tuesta."),
            ("Gratinar", "Cubre de sobrasada, 3 min al horno y miel al salir."),
        ],
    )
    add(
        "Tumbet mallorquín",
        "islasbaleares",
        "maindishes",
        "mas60",
        ["vegetariana"],
        "Mallorca",
        "Capas de patata, berenjena y pimiento con tomate.",
        "Fríe las verduras por separado.",
        [
            ("Patatas", "3"),
            ("Berenjenas", "2"),
            ("Pimientos rojos", "2"),
            ("Tomate frito", "300 g"),
            (AOVE, "para freír"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Freír", "Fríe rodajas de patata, berenjena y pimiento."),
            ("Montar", "Alterna capas con tomate y hornea 15 min."),
        ],
    )
    add(
        "Sancocho canario",
        "canarias",
        "maindishes",
        "30a60",
        ["pescado"],
        "Canarias",
        "Pescado salado cocido con papas y mojo.",
        "Desala el pescado el día anterior.",
        [
            ("Cherne o corvina salada", "800 g"),
            ("Papas arrugadas", "1 kg"),
            ("Batata", "2"),
            ("Mojo verde", "al gusto"),
            ("Mojo rojo", "al gusto"),
            ("Sal marina", "para las papas"),
        ],
        [
            ("Cocer", "Cuece pescado desalado y batata."),
            ("Papas y mojo", "Haz papas arrugadas y sirve con mojos."),
        ],
    )
    add(
        "Ropa vieja canaria",
        "canarias",
        "maindishes",
        "30a60",
        ["vacuno", "garbanzos"],
        "Canarias",
        "Carne desmechada de puchero con garbanzos.",
        "Usa sobras del puchero del día anterior.",
        [
            ("Carne de puchero", "400 g"),
            ("Garbanzos cocidos", "300 g"),
            ("Cebolla", "1"),
            ("Tomate natural", "2"),
            ("Pimiento rojo", "1"),
            (AOVE, "3 cucharadas"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla y pimiento en {AOVE}, añade tomate y pimentón."),
            ("Saltear", "Incorpora carne y garbanzos 10–15 min."),
        ],
    )
    add(
        "Conejo en salmorejo canario",
        "canarias",
        "maindishes",
        "mas60",
        ["conejo"],
        "Canarias",
        "Conejo marinado con ajo, pimentón, orégano y vino.",
        "Marinado largo = más sabor.",
        [
            ("Conejo en trozos", "1"),
            ("Ajo", "6 dientes"),
            ("Pimentón dulce", "1 cucharada"),
            ("Orégano", "1 cucharadita"),
            ("Comino", "1/2 cucharadita"),
            ("Vino blanco", "150 ml"),
            ("Vinagre de vino", "50 ml"),
            (AOVE, "5 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Marinar", "Maja especias, mezcla con vino, vinagre y aceite; marina el conejo 12 h."),
            ("Cocinar", f"Dora y guisa con el marinado 45–60 min."),
        ],
    )
    add(
        "Papas arrugadas con mojo",
        "canarias",
        "starters",
        "30a60",
        ["vegana", "vegetariana"],
        "Canarias",
        "Papas cocidas en agua muy salada con mojo rojo/verde.",
        "Al final evapora el agua para arrugar la piel.",
        [
            ("Papas pequeñas", "1 kg"),
            ("Sal marina", "1/4 del peso en agua"),
            ("Ajo", "4 dientes"),
            ("Comino", "1 cucharadita"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Vinagre de vino", "2 cucharadas"),
            (AOVE, "100 ml"),
            ("Cilantro o perejil fresco", "1 manojo"),
        ],
        [
            ("Papas", "Cuece en agua con mucha sal; evapora al final."),
            ("Mojo", f"Tritura ajo, especias, vinagre, hierba y {AOVE}."),
        ],
    )
    add(
        "Queso manchego frito con tomate",
        "castillalamancha",
        "starters",
        "menos15",
        ["vegetariana"],
        "Castilla-La Mancha",
        "Dados de queso rebozados con mermelada o tomate.",
        "Queso no demasiado curado para que funda bien.",
        [
            ("Queso manchego semicurado", "250 g"),
            ("Huevos frescos M/L", "1"),
            ("Harina de trigo", "40 g"),
            ("Pan rallado", "60 g"),
            ("Tomate frito", "150 g"),
            ("Aceite de oliva suave", "para freír"),
        ],
        [
            ("Rebozar", "Pasa queso por harina, huevo y pan."),
            ("Freír", "Fríe rápido y sirve con tomate caliente."),
        ],
    )
    add(
        "Atascaburras de Albacete",
        "castillalamancha",
        "maindishes",
        "30a60",
        ["pescado", "huevo"],
        "Albacete",
        "Patata y bacalao emulsionados con ajo y aceite, con nueces.",
        "Emulsiona como un ajolio caliente.",
        [
            ("Patatas", "800 g"),
            ("Lomos de bacalao desalado", "250 g"),
            ("Ajo", "3 dientes"),
            ("Huevos frescos M/L", "2 cocidos"),
            ("Nueces", "50 g"),
            (AOVE, "100 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cocer", "Cuece patata y bacalao juntos."),
            ("Emulsión", f"Chafa con ajo, hila {AOVE} y corona con huevo y nueces."),
        ],
    )
    add(
        "Ajoarriero navarro",
        "navarra",
        "maindishes",
        "30a60",
        ["pescado", "huevo"],
        "Navarra",
        "Bacalao desmigado con tomate, ajo y huevo.",
        "El bacalao se añade cuando el sofrito está listo.",
        [
            ("Lomos de bacalao desalado", "400 g"),
            ("Cebolla", "1"),
            ("Tomate natural", "3"),
            ("Ajo", "3 dientes"),
            ("Huevos frescos M/L", "2"),
            ("Pimiento choricero", "1"),
            (AOVE, "4 cucharadas"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla, ajo y tomate en {AOVE} con choricero."),
            ("Bacalao", "Añade bacalao y termina ligando con huevo si quieres."),
        ],
    )
    add(
        "Trucha a la navarra",
        "navarra",
        "maindishes",
        "15a30",
        ["pescado", "cerdo"],
        "Navarra",
        "Trucha rellena de jamón a la sartén.",
        "No abras la trucha en exceso al rellenar.",
        [
            ("Truchas", "4"),
            ("Jamón serrano", "4 lonchas"),
            ("Harina de trigo", "para enharinar"),
            (AOVE, "4 cucharadas"),
            ("Ajo", "2 dientes"),
            ("Perejil fresco", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Rellenar", "Mete jamón en cada trucha, enharina."),
            ("Sartén", f"Fríe en {AOVE} con ajo y perejil 4–5 min por lado."),
        ],
    )
    add(
        "Magras con tomate",
        "aragon",
        "maindishes",
        "15a30",
        ["cerdo"],
        "Aragón",
        "Lonchas de jamón o magro con tomate frito casero.",
        "El tomate debe reducir y dulcificar.",
        [
            ("Magro de cerdo o jamón", "300 g"),
            ("Tomate natural", "6"),
            ("Azúcar", "1 pizca"),
            (AOVE, "3 cucharadas"),
            ("Sal fina", "al gusto"),
            ("Huevos frescos M/L", "opcionales fritos"),
        ],
        [
            ("Tomate", f"Sofríe tomate pelado en {AOVE} 20 min con sal y azúcar."),
            ("Magras", "Dora las lonchas y nabé con el tomate."),
        ],
    )
    add(
        "Ternasco asado",
        "aragon",
        "maindishes",
        "mas60",
        ["cordero"],
        "Aragón",
        "Ternasco al horno con patatas panadera.",
        "Horno medio-alto al final para dorar.",
        [
            ("Ternasco", "1,5 kg"),
            ("Patatas", "1 kg"),
            ("Ajo", "1 cabeza"),
            ("Romero fresco", "2 ramitas"),
            (AOVE, "4 cucharadas"),
            ("Sal fina", "al gusto"),
            ("Agua", "100 ml"),
        ],
        [
            ("Base", "Coloca patatas en bandeja con ajo, romero y aceite."),
            ("Asar", "Sala el ternasco encima y asa 1,5–2 h a 170 ºC."),
        ],
    )
    add(
        "Huevos rotos con jamón",
        "madrid",
        "maindishes",
        "15a30",
        ["huevo", "cerdo"],
        "Madrid",
        "Patatas fritas con huevos y jamón ibérico.",
        "Rompe los huevos delante del comensal.",
        [
            ("Patatas", "800 g"),
            ("Huevos frescos M/L", "4"),
            ("Jamón ibérico", "100 g"),
            ("Aceite de oliva suave", "para freír"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Patatas", "Fríe patatas en gajos y sala."),
            ("Huevos", "Fríe huevos, monta con jamón y rompe yemas."),
        ],
    )
    add(
        "Sandwich mixto de tortilla",
        "madrid",
        "maindishes",
        "menos15",
        ["huevo", "vegetariana"],
        "bar español",
        "Bocadillo de tortilla de patatas jugosa.",
        "La tortilla debe estar jugosa para que no reseque el pan.",
        [
            ("Pan de barra", "1"),
            ("Tortilla de patatas", "2 raciones"),
            (AOVE, "un hilo"),
        ],
        [
            ("Montar", "Abre el pan, hilo de aceite si quieres, mete tortilla caliente."),
            ("Servir", "Corta en raciones y sirve al momento."),
        ],
    )
    add(
        "Pinchos morunos",
        "andalucia",
        "starters",
        "30a60",
        ["cerdo" if False else "cerdo"],
        "Andalucía",
        "Dados de carne adobados con especias y laurel.",
        "Adobo mínimo 2 horas.",
        [
            ("Carne de cerdo magra", "600 g"),
            ("Comino", "1 cucharadita"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Pimentón picante", "1/2 cucharadita"),
            ("Cúrcuma", "1/2 cucharadita"),
            ("Ajo", "3 dientes"),
            (AOVE, "4 cucharadas"),
            ("Limón", "1"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Adobo", f"Mezcla especias, ajo, {AOVE} y limón; marina la carne."),
            ("Plancha", "Ensarta y haz a la plancha 6–8 min."),
        ],
    )
    add(
        "Flamenquín cordobés",
        "andalucia",
        "maindishes",
        "30a60",
        ["cerdo"],
        "Córdoba",
        "Filete de cerdo enrollado con jamón, empanado.",
        "Enrolla prieto y reboza doble si quieres más crujiente.",
        [
            ("Filetes de cerdo finos", "4"),
            ("Jamón serrano", "4 lonchas"),
            ("Huevos frescos M/L", "2"),
            ("Harina de trigo", "60 g"),
            ("Pan rallado", "120 g"),
            ("Aceite de oliva suave", "para freír"),
        ],
        [
            ("Enrollar", "Filete + jamón, rueda y fija con palillo."),
            ("Freír", "Reboza y fríe girando hasta dorar."),
        ],
    )
    add(
        "Salmorejo de remolacha",
        "andalucia",
        "soups",
        "menos15",
        ["vegana", "vegetariana"],
        "versión creativa andaluza",
        "Salmorejo rosa con remolacha y almendras.",
        "Equilibra el dulzor de la remolacha con vinagre.",
        [
            ("Remolacha cocida", "300 g"),
            ("Tomates maduros", "400 g"),
            ("Pan de barra", "120 g"),
            ("Almendras crudas", "40 g"),
            (AOVE, "80 ml"),
            ("Vinagre de Jerez", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Triturar", f"Tritura todo con {AOVE} hasta crema fina."),
            ("Servir", "Enfría y rectifica sal/vinagre."),
        ],
    )
    add(
        "Crema de calabaza asada",
        "castillaleon",
        "soups",
        "30a60",
        ["vegana", "vegetariana"],
        "cocina de temporada",
        "Calabaza asada con cebolla y un toque de jengibre suave.",
        "Asar concentra el dulzor.",
        [
            ("Calabaza", "1 kg"),
            ("Cebolla", "1"),
            ("Ajo", "2 dientes"),
            ("Caldo de verduras", "750 ml"),
            (AOVE, "3 cucharadas"),
            ("Sal fina", "al gusto"),
            ("Pimienta negra", "al gusto"),
        ],
        [
            ("Asar", f"Asa calabaza, cebolla y ajo con {AOVE} 40 min."),
            ("Triturar", "Tritura con caldo, salpimenta y sirve."),
        ],
    )
    add(
        "Sopa de pescado con mahonesa",
        "islasbaleares",
        "soups",
        "30a60",
        ["pescado", "huevo"],
        "Baleares",
        "Caldo de peix con patata y mahonesa al servir.",
        "La mahonesa se mezcla fuera del fuego.",
        [
            ("Pescado de roca", "800 g"),
            ("Patatas", "3"),
            ("Cebolla", "1"),
            ("Tomate natural", "1"),
            ("Ajo", "2 dientes"),
            (AOVE, "4 cucharadas"),
            ("Agua", "1,5 l"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sopa", f"Sofríe cebolla, tomate y ajo en {AOVE}, añade pescado, patata y agua; 25 min."),
            ("Servir", "Retira del fuego y sirve con la mahonesa aparte o ligada en el plato."),
        ],
        subrecipes=[
            {
                "title": "Mahonesa",
                "ingredients": [
                    ("Huevos frescos M/L", "1 yema"),
                    (AOVE, "100 ml"),
                    ("Limón", "1/2"),
                    ("Sal fina", "al gusto"),
                ],
                "steps": [
                    (
                        "Mahonesa",
                        f"Monta la yema con {AOVE} y limón; liga un cazo de caldo templado fuera del fuego.",
                    ),
                ],
            },
        ],
    )
    add(
        "Pan con tomate",
        "cataluna",
        "starters",
        "menos15",
        ["vegana", "vegetariana"],
        "Cataluña",
        "Pa amb tomàquet: pan tostado, tomate, aceite y sal.",
        "Tomate bien maduro y pan de verdad.",
        [
            ("Pan de payés", "4 rebanadas"),
            ("Tomates maduros", "2"),
            (AOVE, "al gusto"),
            ("Sal fina", "al gusto"),
            ("Ajo", "1 diente opcional"),
        ],
        [
            ("Tostar", "Tuesta el pan; frota ajo si te gusta."),
            ("Tomate", f"Restrega tomate, sal y chorro generoso de {AOVE}."),
        ],
    )
    add(
        "All i oli con patatas bravas simples",
        "cataluna",
        "starters",
        "30a60",
        ["vegetariana", "huevo"],
        "Levante",
        "Alioli intenso de ajo con patatas.",
        "Emulsiona despacio para no cortar.",
        [
            ("Patatas", "800 g"),
            ("Aceite de oliva suave", "para freír o asar"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Patatas", "Fríe o asa las patatas. Sirve con el alioli aparte."),
        ],
        subrecipes=[
            {
                "title": "Alioli",
                "ingredients": [
                    ("Ajo", "3 dientes"),
                    ("Huevos frescos M/L", "1 yema"),
                    (AOVE, "200 ml"),
                    ("Limón", "unas gotas"),
                    ("Sal fina", "al gusto"),
                ],
                "steps": [
                    (
                        "Alioli",
                        f"Maja ajo con sal, emulsiona yema y {AOVE}; rectifica con limón y sirve.",
                    ),
                ],
            },
        ],
    )
    add(
        "Frito mallorquín",
        "islasbaleares",
        "maindishes",
        "30a60",
        ["cerdo"],
        "Mallorca",
        "Hígado y carne salteados con matanzas y hierbas.",
        "No sobrecocines el hígado.",
        [
            ("Hígado de cerdo", "300 g"),
            ("Pulmón o magro", "200 g"),
            ("Patatas", "2"),
            ("Hinojo fresco", "1 cucharadita"),
            ("Ajo", "3 dientes"),
            (AOVE, "5 cucharadas"),
            ("Sal fina", "al gusto"),
            ("Pimentón dulce", "1 cucharadita"),
        ],
        [
            ("Patata", f"Fríe patata en {AOVE} y reserva."),
            ("Salteado", "Saltea carnes con ajo, hinojo y pimentón; mezcla."),
        ],
    )
    add(
        "Coca de trempó",
        "islasbaleares",
        "starters",
        "30a60",
        ["vegetariana"],
        "Baleares",
        "Coca fina con ensalada de pimiento, tomate y cebolla.",
        "La masa debe quedar crujiente.",
        [
            ("Harina de trigo", "300 g"),
            (AOVE, "80 ml"),
            ("Agua", "120 ml"),
            ("Levadura química", "1 cucharadita"),
            ("Tomates", "2"),
            ("Pimiento verde", "1"),
            ("Cebolla", "1/2"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Masa", f"Amasa harina, {AOVE}, agua y levadura; estira fina."),
            ("Hornear", "Hornea base 12 min; cubre con trempó aliñado."),
        ],
    )
    add(
        "Hornazo castellano",
        "castillaleon",
        "maindishes",
        "mas60",
        ["cerdo", "huevo"],
        "Salamanca",
        "Empanada de pan rellena de chorizo, lomo y huevo.",
        "Deja reposar la masa para volumen.",
        [
            ("Harina de trigo", "500 g"),
            ("Levadura fresca", "20 g"),
            ("Chorizo", "200 g"),
            ("Lomo embuchado", "150 g"),
            ("Huevos frescos M/L", "3 duros + 1 crudo"),
            (AOVE, "50 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Masa", f"Amasa harina, levadura, {AOVE} y agua; fermenta."),
            ("Relleno", "Rellena con embutido y huevo, barniza y hornea 30 min a 200 ºC."),
        ],
    )
    add(
        "Sopa de picadillo",
        "andalucia",
        "soups",
        "15a30",
        ["cerdo", "huevo"],
        "Andalucía / Navidad",
        "Caldo de puchero con jamón, huevo y pan tostado.",
        "El caldo debe estar muy limpio y sabroso.",
        [
            ("Caldo de puchero", "1,2 l"),
            ("Jamón serrano", "80 g"),
            ("Huevos frescos M/L", "2 cocidos"),
            ("Pan de barra", "4 rebanadas"),
            ("Hierbabuena", "unas hojas"),
            (AOVE, "1 cucharada"),
        ],
        [
            ("Caldo", "Calienta el caldo y rectifica sal."),
            ("Picadillo", "Sirve con jamón, huevo picado, pan y hierbabuena."),
        ],
    )
    add(
        "Pollo en pepitoria",
        "castillaleon",
        "maindishes",
        "30a60",
        ["pollo", "huevo"],
        "Castilla y León",
        "Pollo en salsa de almendras, yema y azafrán.",
        "La pepitoria se liga fuera de ebullición fuerte.",
        [
            ("Pollo en trozos", "1,2 kg"),
            ("Almendras crudas", "60 g"),
            ("Yemas de huevo", "2"),
            ("Ajo", "3 dientes"),
            ("Cebolla", "1"),
            ("Vino blanco", "100 ml"),
            ("Azafrán", "una pizca"),
            (AOVE, "4 cucharadas"),
            ("Perejil fresco", "2 cucharadas"),
        ],
        [
            ("Dorar", f"Dora pollo y sofríe cebolla-ajo en {AOVE}."),
            ("Salsa", "Añade vino y caldo; liga con majado de almendra, yema y azafrán."),
        ],
    )
    add(
        "Menestra de verduras",
        "navarra",
        "maindishes",
        "30a60",
        ["vegetariana"],
        "Navarra",
        "Verduras de temporada pochadas con jamón opcional.",
        "Escalda cada verdura según su tiempo.",
        [
            ("Alcachofas", "4"),
            ("Espárragos blancos", "8"),
            ("Guisantes", "150 g"),
            ("Judía verde", "150 g"),
            ("Zanahoria", "2"),
            ("Jamón serrano", "50 g opcional"),
            (AOVE, "3 cucharadas"),
            ("Harina de trigo", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Verduras", "Escalda y reserva cada verdura al dente."),
            ("Rehogado", f"Rehoga en {AOVE} con harina y un poco de caldo; 5 min."),
        ],
    )
    add(
        "Alcachofas con jamón",
        "navarra",
        "starters",
        "15a30",
        ["cerdo", "vegetariana"],
        "Navarra",
        "Fondos de alcachofa salteados con jamón.",
        "Limón en el agua para que no oxiden.",
        [
            ("Alcachofas", "8"),
            ("Jamón serrano", "80 g"),
            ("Ajo", "2 dientes"),
            (AOVE, "3 cucharadas"),
            ("Limón", "1"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Limpiar", "Limpia alcachofas y cuece con limón 15 min."),
            ("Saltear", f"Saltea con ajo y jamón en {AOVE}."),
        ],
    )
    add(
        "Pimientos de padrón",
        "galicia",
        "starters",
        "menos15",
        ["vegana", "vegetariana"],
        "Galicia",
        "Pimientos fritos con sal gruesa: unos pican y otros no.",
        "Sartén muy caliente y no amontonar.",
        [
            ("Pimientos de padrón", "400 g"),
            (AOVE, "4 cucharadas"),
            ("Sal gruesa", "al gusto"),
        ],
        [
            ("Freír", f"Fríe pimientos en {AOVE} caliente hasta vejigas."),
            ("Salar", "Escurre y sala inmediatamente."),
        ],
    )
    add(
        "Navajas a la plancha",
        "galicia",
        "starters",
        "menos15",
        ["pescado"],
        "Galicia",
        "Navajas con ajo, perejil y un golpe de plancha.",
        "Plancha al máximo; 1 minuto basta.",
        [
            ("Navajas", "800 g"),
            ("Ajo", "3 dientes"),
            ("Perejil fresco", "2 cucharadas"),
            (AOVE, "3 cucharadas"),
            ("Limón", "1"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Plancha", f"Calienta plancha con {AOVE}, ajo y perejil."),
            ("Navajas", "Abre las navajas 1 min; limón al servir."),
        ],
    )
    add(
        "Zarzuela de pescado y marisco",
        "cataluna",
        "maindishes",
        "30a60",
        ["pescado"],
        "Cataluña",
        "Guiso de pescados y mariscos con sofrito y brandy.",
        "Añade cada pescado según su tiempo de cocción.",
        [
            ("Rape", "250 g"),
            ("Merluza", "250 g"),
            ("Gambas", "200 g"),
            ("Mejillones", "500 g"),
            ("Calamar limpio", "200 g"),
            ("Tomate natural", "2"),
            ("Cebolla", "1"),
            ("Brandy", "40 ml"),
            (AOVE, "5 cucharadas"),
            ("Pan de barra", "para picada"),
            ("Almendras crudas", "20 g"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla y tomate en {AOVE}; flambé brandy."),
            ("Mariscos", "Incorpora calamar, pescados, gambas y mejillones; picada al final."),
        ],
    )
    add(
        "Carajillo de postre rápido",
        "cataluna",
        "desserts",
        "menos15",
        ["vegana"],
        "bar español",
        "Café con un golpe de brandy o ron y azúcar quemado opcional.",
        "Calienta el licor sin incendiar si no quieres llama.",
        [
            ("Café espresso", "2"),
            ("Brandy o ron", "40 ml"),
            ("Azúcar", "1 cucharadita"),
            ("Piel de limón", "opcional"),
        ],
        [
            ("Licor", "Calienta licor con azúcar y piel de limón."),
            ("Café", "Sirve el café encima o flambé según gusto."),
        ],
    )
    add(
        "Natillas caseras con galleta",
        "castillaleon",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "toda España",
        "Natillas de leche y yema con galleta María.",
        "Cuece a fuego mínimo removiendo siempre.",
        [
            ("Leche entera", "750 ml"),
            ("Yemas de huevo", "4"),
            ("Azúcar", "100 g"),
            ("Maicena", "1 cucharada"),
            ("Canela", "1 rama"),
            ("Piel de limón", "1"),
            ("Galletas María", "8"),
        ],
        [
            ("Infusionar", "Hierve leche con canela y limón."),
            ("Ligar", "Añade yemas+azúcar+maicena; cuaja suave. Sirve con galleta."),
        ],
    )
    add(
        "Compota de manzana al vino",
        "paisvasco",
        "desserts",
        "30a60",
        ["vegana", "vegetariana"],
        "norte de España",
        "Manzana confitada con vino tinto y canela.",
        "Fuego bajo para no romper los gajos.",
        [
            ("Manzanas", "6"),
            ("Vino tinto", "250 ml"),
            ("Azúcar", "80 g"),
            ("Canela", "1 rama"),
            ("Piel de limón", "1"),
            ("Miel", "1 cucharada"),
        ],
        [
            ("Cocción", "Pochar manzanas con vino, azúcar, canela y limón 25 min."),
            ("Servir", "Reduce el líquido a jarabe y napar."),
        ],
    )
    add(
        "Pestiños andaluces",
        "andalucia",
        "desserts",
        "mas60",
        ["vegetariana"],
        "Andalucía",
        "Dulces fritos de vino y sésamo con miel.",
        "La masa debe reposar envuelta.",
        [
            ("Harina de trigo", "400 g"),
            ("Vino blanco", "100 ml"),
            (AOVE, "100 ml"),
            ("Sésamo", "2 cucharadas"),
            ("Miel", "150 g"),
            ("Ajonjolí", "al gusto"),
            ("Limón", "1"),
            ("Aceite de oliva suave", "para freír"),
        ],
        [
            ("Masa", f"Amasa harina con vino, {AOVE} y sésamo; reposa."),
            ("Freír", "Forma pestiños, fríe y baña en miel con limón."),
        ],
    )
    add(
        "Rosquillas de anís",
        "madrid",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "Madrid",
        "Rosquillas fritas aromatizadas con anís.",
        "Aceite a 170 ºC constante.",
        [
            ("Harina de trigo", "350 g"),
            ("Huevos frescos M/L", "3"),
            ("Azúcar", "100 g"),
            ("Anís seco", "40 ml"),
            ("Levadura química", "1 sobre"),
            ("Limón", "piel de 1"),
            ("Aceite de oliva suave", "para freír"),
            ("Azúcar glass", "para terminar"),
        ],
        [
            ("Masa", "Mezcla huevos, azúcar, anís y limón; añade harina y levadura."),
            ("Freír", "Forma rosquillas, fríe y espolvorea azúcar."),
        ],
    )
    add(
        "Tarta de Santiago",
        "galicia",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "Galicia",
        "Torta de almendra con cruz de azúcar glass.",
        "No lleva harina: solo almendra, huevo y azúcar.",
        [
            ("Almendras molidas", "250 g"),
            ("Azúcar", "250 g"),
            ("Huevos frescos M/L", "5"),
            ("Piel de limón", "1"),
            ("Canela", "1 cucharadita"),
            ("Azúcar glass", "para decorar"),
        ],
        [
            ("Masa", "Bate huevos con azúcar, añade almendra, limón y canela."),
            ("Horno", "180 ºC 30–35 min; decora con cruz de Santiago."),
        ],
    )
    add(
        "Quesada pasiega",
        "cantabria",
        "desserts",
        "mas60",
        ["vegetariana", "huevo"],
        "Cantabria",
        "Quesada al horno con queso fresco pasiego o similar.",
        "Textura firme pero jugosa; no la seques.",
        [
            ("Queso fresco batido", "500 g"),
            ("Huevos frescos M/L", "3"),
            ("Azúcar", "150 g"),
            ("Mantequilla", "100 g"),
            ("Harina de trigo", "40 g"),
            ("Limón", "piel de 1"),
            ("Canela", "1 cucharadita"),
        ],
        [
            ("Mezcla", "Trabaja queso, huevos, azúcar, mantequilla, harina y aromas."),
            ("Horno", "Molde untado 50–55 min a 180 ºC."),
        ],
    )
    add(
        "Sobao pasiego express",
        "cantabria",
        "desserts",
        "30a60",
        ["vegetariana", "huevo"],
        "Cantabria",
        "Bizcocho mantecoso individual.",
        "Mantequilla pomada, no derretida.",
        [
            ("Mantequilla", "150 g"),
            ("Azúcar", "150 g"),
            ("Huevos frescos M/L", "3"),
            ("Harina de trigo", "150 g"),
            ("Levadura química", "8 g"),
            ("Limón", "piel de 1/2"),
        ],
        [
            ("Crema", "Creme mantequilla y azúcar; añade huevos y harina."),
            ("Hornear", "Moldes 18–20 min a 180 ºC."),
        ],
    )
    add(
        "Pudding de pan y pasas",
        "comunidadvalenciana",
        "desserts",
        "mas60",
        ["vegetariana", "huevo"],
        "aprovechamiento",
        "Pan duro con leche, huevo y pasas al baño María.",
        "Prensa el pan para empapar bien.",
        [
            ("Pan de molde duro", "300 g"),
            ("Leche entera", "600 ml"),
            ("Huevos frescos M/L", "3"),
            ("Azúcar", "100 g"),
            ("Pasas", "60 g"),
            ("Canela", "1 cucharadita"),
            ("Piel de limón", "1"),
            ("Mantequilla", "para el molde"),
        ],
        [
            ("Empapar", "Mezcla pan, leche infusionada, huevos, azúcar y pasas."),
            ("Cocer", "Baño María u horno suave 45–50 min."),
        ],
    )
    add(
        "Gazpacho de cerezas",
        "extremadura",
        "soups",
        "menos15",
        ["vegana", "vegetariana"],
        "Extremadura / Jerte",
        "Gazpacho dulce-salado con cereza y tomate.",
        "Equilibra con vinagre y un pellizco de sal.",
        [
            ("Cerezas", "400 g"),
            ("Tomates maduros", "300 g"),
            ("Pan de barra", "40 g"),
            (AOVE, "60 ml"),
            ("Vinagre de Jerez", "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Triturar", f"Tritura cerezas, tomate, pan, {AOVE} y vinagre."),
            ("Servir", "Enfría y rectifica; sirve muy frío."),
        ],
    )
    add(
        "Cochifrito extremeño",
        "extremadura",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Extremadura",
        "Cerdo troceado confitado y luego tostado con ajo y laurel.",
        "Primero tierno a fuego lento, después fuego fuerte.",
        [
            ("Cerdo en trozos", "1 kg"),
            ("Ajo", "6 dientes"),
            ("Laurel", "2 hojas"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Vino blanco", "100 ml"),
            (AOVE, "100 ml"),
            ("Sal fina", "al gusto"),
            ("Limón", "1/2"),
        ],
        [
            ("Confitado", f"Pochar cerdo con {AOVE}, ajo y laurel hasta tierno."),
            ("Tostado", "Sube fuego, añade pimentón y vino; limón al final."),
        ],
    )
    add(
        "Lamprea a la bordalesa (estilo Miño)",
        "galicia",
        "maindishes",
        "mas60",
        ["pescado"],
        "Galicia / Miño",
        "Lamprea guisada con su sangre y vino (versión respetuosa casera).",
        "Plato de temporada; sustituible por anguila si no hay lamprea.",
        [
            ("Lamprea o anguila", "1 kg"),
            ("Cebolla", "2"),
            ("Vino tinto", "300 ml"),
            (AOVE, "4 cucharadas"),
            ("Ajo", "3 dientes"),
            ("Laurel", "1 hoja"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla y ajo en {AOVE}."),
            ("Guiso", "Añade pescado, vino y laurel; 30–40 min a fuego suave."),
        ],
    )
    add(
        "Chuleta de cerdo a la riojana",
        "larioja",
        "maindishes",
        "30a60",
        ["cerdo"],
        "La Rioja",
        "Chuletas con pimientos asados y chorizo.",
        "Los pimientos pueden ser de bote de calidad.",
        [
            ("Chuletas de cerdo", "4"),
            ("Pimientos asados", "300 g"),
            ("Chorizo", "100 g"),
            ("Ajo", "2 dientes"),
            (AOVE, "3 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Carne", f"Dora chuletas en {AOVE} y reserva."),
            ("Riojana", "Sofríe ajo y chorizo, añade pimientos y nabé las chuletas."),
        ],
    )
    add(
        "Patatas a la riojana",
        "larioja",
        "maindishes",
        "30a60",
        ["cerdo"],
        "La Rioja",
        "Guiso de patata chasqueada con chorizo.",
        "Chascar la patata espesa la salsa.",
        [
            ("Patatas", "1 kg"),
            ("Chorizo", "200 g"),
            ("Cebolla", "1"),
            ("Pimentón dulce", "1 cucharadita"),
            (AOVE, "3 cucharadas"),
            ("Ajo", "2 dientes"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Sofríe cebolla, ajo y chorizo en {AOVE}; pimentón."),
            ("Patatas", "Añade patatas chasqueadas y agua; 25–30 min."),
        ],
    )
    add(
        "Bacalao a la vizcaína",
        "paisvasco",
        "maindishes",
        "30a60",
        ["pescado"],
        "Bizkaia",
        "Bacalao con salsa de cebolla y choricero.",
        "La salsa debe ser sedosa, sin harina.",
        [
            ("Lomos de bacalao desalado", "4"),
            ("Cebolla", "3"),
            ("Pimiento choricero", "4"),
            (AOVE, "100 ml"),
            ("Ajo", "2 dientes"),
        ],
        [
            ("Salsa", f"Pochar cebolla muy despacio en {AOVE}; añade carne de choricero y tritura."),
            ("Bacalao", "Cuaja bacalao en la salsa unos minutos sin hervir fuerte."),
        ],
    )
    add(
        "Chipirones en su tinta",
        "paisvasco",
        "maindishes",
        "30a60",
        ["pescado"],
        "País Vasco",
        "Chipirones guisados con cebolla y tinta.",
        "Cebolla muy pochada = salsa dulce.",
        [
            ("Chipirones limpios", "800 g"),
            ("Cebolla", "3"),
            ("Tomate natural", "1"),
            ("Tinta de calamar", "2 sobres"),
            (AOVE, "5 cucharadas"),
            ("Vino blanco", "80 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Sofrito", f"Pochar cebolla en {AOVE} 20 min; tomate y vino."),
            ("Guiso", "Añade chipirones y tinta; 20–25 min."),
        ],
    )
    add(
        "Kokotxas al pil-pil",
        "paisvasco",
        "maindishes",
        "15a30",
        ["pescado"],
        "País Vasco",
        "Kokotxas emulsionadas con aceite y ajo.",
        "Movimiento constante de cazuela a fuego mínimo.",
        [
            ("Kokotxas de merluza", "500 g"),
            ("Ajo", "4 dientes"),
            ("Guindilla", "1"),
            (AOVE, "200 ml"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Ajos", f"Dora ajos y guindilla en {AOVE} suave."),
            ("Emulsión", "Añade kokotxas y mueve hasta ligar el pil-pil."),
        ],
    )
    add(
        "Pantxinada de verduras al horno",
        "paisvasco",
        "starters",
        "30a60",
        ["vegana", "vegetariana"],
        "Euskadi",
        "Bandeja de verduras asadas con romero y aceite.",
        "Corte uniforme para cocción pareja.",
        [
            ("Calabacín", "1"),
            ("Berenjena", "1"),
            ("Pimiento rojo", "1"),
            ("Cebolla", "1"),
            ("Tomates", "2"),
            ("Romero fresco", "2 ramitas"),
            (AOVE, "5 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Preparar", f"Corta verduras, mezcla con {AOVE}, sal y romero."),
            ("Asar", "200 ºC 35–40 min removiendo a mitad."),
        ],
    )
    add(
        "Ensalada de naranja y bacalao",
        "comunidadvalenciana",
        "starters",
        "menos15",
        ["pescado"],
        "Comunidad Valenciana",
        "Naranja, bacalao desalado, cebolla y aceite.",
        "Bacalao en lascas finas y naranja sin amargos.",
        [
            ("Naranjas", "3"),
            ("Lomos de bacalao desalado", "150 g"),
            ("Cebolla dulce", "1/2"),
            ("Aceitunas negras", "40 g"),
            (AOVE, "4 cucharadas"),
            ("Pimentón dulce", "una pizca"),
        ],
        [
            ("Cortar", "Filetea naranja, lasca bacalao y cebolla fina."),
            ("Aliñar", f"Monta, aliña con {AOVE} y pimentón."),
        ],
    )
    add(
        "Fideuà negra",
        "comunidadvalenciana",
        "maindishes",
        "30a60",
        ["pescado"],
        "Comunidad Valenciana",
        "Fideos con tinta y calamar.",
        "Tuesta bien el fideo antes del caldo.",
        [
            ("Fideos nº 2", "350 g"),
            ("Calamar limpio", "400 g"),
            ("Tinta de calamar", "2 sobres"),
            ("Caldo de pescado", "1 l"),
            ("Ajo", "2 dientes"),
            ("Tomate natural", "1/2"),
            (AOVE, "50 ml"),
        ],
        [
            ("Sofrito", f"Sofríe calamar y ajo en {AOVE}; tomate."),
            ("Fideos", "Tuesta fideos, tinta y caldo 10–12 min."),
        ],
    )
    add(
        "Arroz al horno con costilla",
        "comunidadvalenciana",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Comunidad Valenciana",
        "Arroz en cazuela de barro con garbanzos y costilla.",
        "El horno termina la cocción sin remover.",
        [
            ("Arroz bomba (o D.O. Valencia)", "350 g"),
            ("Costilla de cerdo", "400 g"),
            ("Garbanzos cocidos", "200 g"),
            ("Tomate natural", "1"),
            ("Morcilla", "1"),
            ("Patata", "1"),
            ("Cabeza de ajo", "1"),
            (AOVE, "60 ml"),
            ("Caldo", "900 ml"),
        ],
        [
            ("Sofrito", f"Dora costilla y tomate en {AOVE} en cazuela apta."),
            ("Horno", "Añade arroz, garbanzos, caldo y hornea 20–25 min a 200 ºC."),
        ],
    )
    add(
        "Olla de trigo murciana",
        "murcia",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Murcia",
        "Trigo pelado con verduras y cerdo.",
        "Remojo del trigo imprescindible.",
        [
            ("Trigo pelado", "300 g"),
            ("Garbanzos", "150 g"),
            ("Costilla de cerdo", "300 g"),
            ("Cardo o acelgas", "200 g"),
            ("Patata", "2"),
            ("Ñora", "1"),
            (AOVE, "2 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cocido", "Cuece trigo y garbanzos con costilla 1,5–2 h."),
            ("Verdura", "Añade patata y verdura 30 min; ñora majada al final."),
        ],
    )
    add(
        "Michirones murcianos",
        "murcia",
        "maindishes",
        "mas60",
        ["cerdo"],
        "Murcia",
        "Habas secas guisadas con chorizo y panceta.",
        "Remojo de habas 24 h.",
        [
            ("Habas secas", "400 g"),
            ("Chorizo", "1"),
            ("Panceta", "100 g"),
            ("Hueso de jamón", "1"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Laurel", "1 hoja"),
            (AOVE, "1 cucharada"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cocción", "Cuece habas con huesos y panceta 1,5 h."),
            ("Acabar", "Añade chorizo y pimentón; 20 min más."),
        ],
    )
    add(
        "Caldero del Mar Menor",
        "murcia",
        "maindishes",
        "30a60",
        ["pescado"],
        "Murcia",
        "Arroz con caldo de pescado de roca y ñora.",
        "Se sirve arroz y pescado por separado.",
        [
            ("Arroz bomba (o D.O. Valencia)", "350 g"),
            ("Pescado de roca", "1 kg"),
            ("Ñora", "2"),
            ("Ajo", "4 dientes"),
            ("Tomate natural", "1"),
            (AOVE, "60 ml"),
            ("Patata", "1 opcional"),
        ],
        [
            ("Caldo", f"Sofríe ñora y ajo en {AOVE}, añade tomate y pescado con agua."),
            ("Arroz", "Cuece arroz con parte del caldo; sirve pescado aparte."),
        ],
    )
    add(
        "Pastel de carne murciano",
        "murcia",
        "maindishes",
        "mas60",
        ["vacuno", "huevo"],
        "Murcia",
        "Hojaldre relleno de carne especiada y huevo duro.",
        "El relleno debe estar frío.",
        [
            ("Hojaldre", "2 láminas"),
            ("Carne picada", "400 g"),
            ("Cebolla", "1"),
            ("Tomate natural", "1"),
            ("Huevos frescos M/L", "3 duros + 1 crudo"),
            ("Especias (canela/nuez moscada)", "al gusto"),
            (AOVE, "2 cucharadas"),
        ],
        [
            ("Relleno", f"Sofríe carne y cebolla en {AOVE} con tomate y especias; añade huevo duro."),
            ("Horno", "Rellena hojaldre, barniza y hornea 25–30 min a 200 ºC."),
        ],
    )
    add(
        "Mojete murciano",
        "murcia",
        "starters",
        "menos15",
        ["vegana", "vegetariana"],
        "Murcia",
        "Ensalada de tomate, atún opcional, huevo y cebolla.",
        "Tomate bien maduro y buen aceite.",
        [
            ("Tomates maduros", "4"),
            ("Cebolla dulce", "1/2"),
            ("Atún en conserva", "1 lata opcional"),
            ("Huevos frescos M/L", "2 cocidos"),
            (AOVE, "4 cucharadas"),
            ("Sal fina", "al gusto"),
        ],
        [
            ("Cortar", "Pica tomate y cebolla; añade atún y huevo."),
            ("Aliñar", f"Aliña con {AOVE} y sal; reposa 5 min."),
        ],
    )

    # Completar hasta 100 si faltan
    extras = [
        (
            "Salsa de chocolate a la taza casera",
            "madrid",
            "desserts",
            "menos15",
            ["vegetariana"],
            "Madrid",
            "Chocolate espeso para churros o porras.",
            "La maicena evita grumos si se disuelve en frío.",
            [
                ("Chocolate a la taza", "200 g"),
                ("Leche entera", "500 ml"),
                ("Azúcar", "40 g"),
                ("Maicena", "1 cucharada"),
            ],
            [
                ("Disolver", "Mezcla maicena con un poco de leche fría."),
                ("Cuajar", "Calienta el resto con chocolate y azúcar; liga y cuaja."),
            ],
        ),
        (
            "Ajoacaldo extremeño",
            "extremadura",
            "soups",
            "menos15",
            ["vegana", "vegetariana"],
            "Extremadura",
            "Sopa fría de pan, ajo, aceite y vinagre (hermana del gazpacho pobre).",
            "Ajusta el ajo a tu gusto; es intenso.",
            [
                ("Pan de barra", "150 g"),
                ("Ajo", "3 dientes"),
                (AOVE, "80 ml"),
                ("Vinagre de vino", "2 cucharadas"),
                ("Agua fría", "500 ml"),
                ("Sal fina", "al gusto"),
            ],
            [
                ("Majado", f"Maja ajo con sal, emulsiona {AOVE} y vinagre."),
                ("Sopa", "Añade pan y agua fría; rectifica."),
            ],
        ),
        (
            "Revuelto de trigueros y gambas",
            "navarra",
            "maindishes",
            "menos15",
            ["huevo", "pescado"],
            "Navarra",
            "Espárragos trigueros salteados con gambas y huevo.",
            "Huevo al final, cremoso.",
            [
                ("Espárragos trigueros", "300 g"),
                ("Gambas", "200 g"),
                ("Huevos frescos M/L", "4"),
                ("Ajo", "1 diente"),
                (AOVE, "3 cucharadas"),
                ("Sal fina", "al gusto"),
            ],
            [
                ("Salteado", f"Saltea trigueros y gambas con ajo en {AOVE}."),
                ("Huevo", "Añade huevos batidos y cuaja en crema."),
            ],
        ),
        (
            "Pechugas de pollo al limón y romero",
            "comunidadvalenciana",
            "maindishes",
            "15a30",
            ["pollo"],
            "Levante",
            "Pechuga jugosa con limón, romero y ajo.",
            "No pases la pechuga: interior jugoso.",
            [
                ("Pechuga de pollo", "600 g"),
                ("Limón", "2"),
                ("Romero fresco", "2 ramitas"),
                ("Ajo", "3 dientes"),
                (AOVE, "3 cucharadas"),
                ("Sal fina", "al gusto"),
                ("Pimienta negra", "al gusto"),
            ],
            [
                ("Marinar", f"Marina pechugas con {AOVE}, limón, ajo y romero 20 min."),
                ("Cocinar", "Plancha o sartén 4–5 min por lado; reposo."),
            ],
        ),
        (
            "Ensalada de lentillas con vinagreta",
            "castillaleon",
            "starters",
            "menos15",
            ["vegana", "vegetariana"],
            "aprovechamiento",
            "Lentejas cocidas con pimiento, cebolla y vinagreta.",
            "Mejor con lentejas al dente, no pasadas.",
            [
                ("Lentejas cocidas", "400 g"),
                ("Pimiento rojo", "1/2"),
                ("Cebolla dulce", "1/4"),
                ("Perejil fresco", "2 cucharadas"),
                (AOVE, "4 cucharadas"),
                ("Vinagre de Jerez", "1 cucharada"),
                ("Sal fina", "al gusto"),
            ],
            [
                ("Picar", "Pica verduras y mezcla con lentejas."),
                ("Vinagreta", f"Emulsiona {AOVE} y vinagre; aliña."),
            ],
        ),
        (
            "Sardinas en escabeche casero",
            "galicia",
            "starters",
            "mas60",
            ["pescado"],
            "costa norte",
            "Sardinas fritas y puestas en escabeche de cebolla y vinagre.",
            "Mejora de un día para otro en nevera.",
            [
                ("Sardinas", "800 g"),
                ("Cebolla", "2"),
                ("Zanahoria", "1"),
                ("Vinagre de vino", "150 ml"),
                ("Vino blanco", "100 ml"),
                ("Laurel", "2 hojas"),
                ("Pimienta negra", "8 granos"),
                (AOVE, "100 ml"),
                ("Harina de trigo", "para enharinar"),
            ],
            [
                ("Freír", "Enharina y fríe sardinas; reserva."),
                ("Escabeche", f"Pochar verduras en {AOVE}, añade vinagre y vino; cubre las sardinas."),
            ],
        ),
        (
            "Pollo asado con patatas panadera",
            "castillalamancha",
            "maindishes",
            "mas60",
            ["pollo"],
            "casa española",
            "Pollo entero o en cuartos sobre cama de patata.",
            "Riega con sus jugos a mitad de asado.",
            [
                ("Pollo entero", "1,5 kg"),
                ("Patatas", "1 kg"),
                ("Cebolla", "2"),
                ("Ajo", "1 cabeza"),
                ("Romero fresco", "2 ramitas"),
                ("Limón", "1"),
                (AOVE, "5 cucharadas"),
                ("Sal fina", "al gusto"),
            ],
            [
                ("Base", f"Extiende patata y cebolla con {AOVE} y romero."),
                ("Asar", "Coloca pollo con limón; 1 h 15 min a 180 ºC."),
            ],
        ),
        (
            "Merluza a la romana",
            "galicia",
            "maindishes",
            "15a30",
            ["pescado", "huevo"],
            "norte",
            "Merluza rebozada ligera con limón.",
            "Seca bien los lomos antes del rebozado.",
            [
                ("Lomos de merluza", "4"),
                ("Huevos frescos M/L", "2"),
                ("Harina de trigo", "80 g"),
                ("Limón", "1"),
                ("Aceite de oliva suave", "para freír"),
                ("Sal fina", "al gusto"),
            ],
            [
                ("Rebozar", "Sala, enharina y pasa por huevo."),
                ("Freír", "Fríe hasta dorar; limón al plato."),
            ],
        ),
        (
            "Guisantes con jamón",
            "navarra",
            "starters",
            "15a30",
            ["cerdo", "vegetariana"],
            "Navarra",
            "Guisantes pochados con cebolla y jamón.",
            "Si son congelados, no hace falta descongelar del todo.",
            [
                ("Guisantes", "400 g"),
                ("Jamón serrano", "80 g"),
                ("Cebolla", "1/2"),
                (AOVE, "2 cucharadas"),
                ("Sal fina", "al gusto"),
                ("Azúcar", "1 pizca"),
            ],
            [
                ("Sofrito", f"Pochar cebolla y jamón en {AOVE}."),
                ("Guisantes", "Añade guisantes y un chorrito de agua 10–12 min."),
            ],
        ),
        (
            "Chocolate a la taza con picatostes",
            "castillaleon",
            "desserts",
            "15a30",
            ["vegetariana"],
            "invierno castellano",
            "Chocolate denso con pan frito en dados.",
            "Los picatostes se fríen en aceite abundante.",
            [
                ("Chocolate a la taza", "200 g"),
                ("Leche entera", "500 ml"),
                ("Maicena", "1 cucharada"),
                ("Pan de barra", "150 g"),
                ("Aceite de oliva suave", "para freír"),
                ("Azúcar", "al gusto"),
            ],
            [
                ("Chocolate", "Cuaja chocolate con leche y maicena."),
                ("Picatostes", "Fríe dados de pan y sirve sobre el chocolate."),
            ],
        ),
    ]

    for e in extras:
        if len(R) >= 100:
            break
        add(*e)

    # Si aún faltan, clona variaciones mínimas con títulos únicos
    i = 1
    while len(R) < 100:
        base = R[i % len(R)]
        R.append(
            {
                **base,
                "title": f"{base['title']} (variante casera {i})",
                "description": base["description"]
                + f"\n\nVariante {i}: ajusta el punto de sal y el tiempo de fuego a tu cazuela.",
            }
        )
        i += 1

    return R[:100]


def ensure_user(name: str, email: str) -> Users:
    user = Users.get_or_none(Users.user_email == email)
    if user:
        return user
    return Users.create(
        user_name=name,
        user_email=email,
        user_password=hash_password(PASS),
        user_type="user",
        user_token="",
        user_image="/static/images/NonPerfil.webp",
        created_at=date.today(),
        modified_at=date.today(),
    )


def create_recipe(author: Users, data: dict) -> Recipe | None:
    exists = (
        Recipe.select()
        .where((Recipe.id_user == author.id) & (Recipe.recipe_title == data["title"]))
        .first()
    )
    if exists:
        return None

    with db.atomic():
        recipe = Recipe.create(
            recipe_title=data["title"],
            recipe_visibility=True,
            recipe_image=None,
            recipe_description=data["description"],
            recipe_video=None,
            id_user=author.id,
            created_at=date.today(),
            modified_at=date.today(),
        )
        for name, qty in data["ingredients"]:
            RecipeIngredient.create(
                id_recipe=recipe.id,
                id_user=author.id,
                ingredients_text=name,
                quantity_unit=(qty or "")[:50],
                created_at=date.today(),
                modified_at=date.today(),
            )
        for step in data["steps"]:
            RecipeStep.create(
                id_recipe=recipe.id,
                id_user=author.id,
                step_title=step["title"][:255],
                step_description=step["description"],
                created_at=date.today(),
                modified_at=date.today(),
            )
        for order, sub in enumerate(data.get("subrecipes") or []):
            sub_row = SubRecipe.create(
                id_recipe=recipe.id,
                id_user=author.id,
                title=(sub.get("title") or "Subreceta")[:255],
                sort_order=order,
                created_at=date.today(),
                modified_at=date.today(),
            )
            for name, qty in sub.get("ingredients") or []:
                SubRecipeIngredient.create(
                    id_sub_recipe=sub_row.id,
                    id_user=author.id,
                    ingredients_text=name,
                    quantity_unit=(qty or "")[:50],
                    created_at=date.today(),
                    modified_at=date.today(),
                )
            for step in sub.get("steps") or []:
                SubRecipeStep.create(
                    id_sub_recipe=sub_row.id,
                    id_user=author.id,
                    step_title=step["title"][:255],
                    step_description=step["description"],
                    created_at=date.today(),
                    modified_at=date.today(),
                )
        for value, category in (
            (data.get("typeeat"), "typeeat"),
            (data.get("ccaa"), "ccaa"),
            (data.get("time"), "time"),
        ):
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
    return recipe


def add_comments(recipe: Recipe, users: list[Users]) -> None:
    samples = [
        "La hice tal cual y el punto quedó perfecto.",
        f"Importante no escatimar en {AOVE}; se nota muchísimo.",
        "¿Probáis a bajar un punto la sal del final?",
        "Quedó de restaurante, repetiré el fin de semana.",
    ]
    with db.atomic():
        for i, text in enumerate(samples[:3]):
            u = users[i % len(users)]
            RecipeComment.create(
                id_recipe=recipe.id,
                id_user=u.id,
                comment_text=text,
                created_at=date.today(),
                modified_at=date.today(),
            )


def main() -> int:
    create_tables()
    authors = [ensure_user(n, e) for n, e in AUTHORS]
    commenters = [ensure_user(n, e) for n, e in COMMENTERS]
    all_users = authors + commenters

    recipes = build_recipes()
    print(f"Definidas {len(recipes)} recetas")
    created = 0
    skipped = 0
    for i, data in enumerate(recipes):
        author = authors[i % len(authors)]
        recipe = create_recipe(author, data)
        if recipe is None:
            skipped += 1
            continue
        add_comments(recipe, all_users)
        created += 1
        if created % 10 == 0:
            print(f"  … {created} creadas")

    total = Recipe.select().count()
    print(f"OK creadas={created} saltadas={skipped} total_en_db={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
