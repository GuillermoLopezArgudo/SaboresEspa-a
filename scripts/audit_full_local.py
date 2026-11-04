"""Barrido local: estructura de recetas/subrecetas + relevancia de precios Mercadona.

Uso:
  python scripts/audit_full_local.py
  python scripts/audit_full_local.py --api http://127.0.0.1:5000
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
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

from app.models import (  # noqa: E402
    Recipe,
    RecipeIngredient,
    RecipeStep,
    SubRecipe,
    SubRecipeIngredient,
    SubRecipeStep,
    create_tables,
)

# Señales típicas de producto irrelevante en el top
_BAD_TOP_HINTS = (
    "papilla",
    "paté",
    "pate ",
    "comida para perro",
    "comida para gato",
    "adulto perro",
    "adulto gato",
    "gyoza",
    "pan rallado",
)


def _post(api: str, path: str, body: dict, timeout: float = 45.0, retries: int = 5) -> dict:
    raw = json.dumps(body).encode("utf-8")
    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(
            api.rstrip("/") + path,
            data=raw,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code in (429, 503) and attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            raise
    assert last_exc is not None
    raise last_exc


def audit_structure() -> dict:
    create_tables()
    issues = []
    empty_main_ings = []
    empty_main_steps = []
    empty_sub_ings = []
    empty_sub_steps = []
    orphan_subs = 0

    recipes = list(Recipe.select())
    for r in recipes:
        n_ing = RecipeIngredient.select().where(RecipeIngredient.id_recipe == r.id).count()
        n_step = RecipeStep.select().where(RecipeStep.id_recipe == r.id).count()
        if n_ing == 0:
            empty_main_ings.append(r.recipe_title)
        if n_step == 0:
            empty_main_steps.append(r.recipe_title)
        for sub in SubRecipe.select().where(SubRecipe.id_recipe == r.id):
            si = SubRecipeIngredient.select().where(
                SubRecipeIngredient.id_sub_recipe == sub.id
            ).count()
            ss = SubRecipeStep.select().where(SubRecipeStep.id_sub_recipe == sub.id).count()
            if si == 0:
                empty_sub_ings.append(f"{r.recipe_title} → {sub.title}")
            if ss == 0:
                empty_sub_steps.append(f"{r.recipe_title} → {sub.title}")
            if not (sub.title or "").strip():
                issues.append(f"Subreceta sin nombre en «{r.recipe_title}»")

    # Subrecetas huérfanas (no debería haber)
    for sub in SubRecipe.select():
        if not Recipe.get_or_none(Recipe.id == sub.id_recipe_id):
            orphan_subs += 1

    # Duplicados de título
    titles = defaultdict(int)
    for r in recipes:
        titles[r.recipe_title] += 1
    dupes = sorted([t for t, c in titles.items() if c > 1])

    return {
        "recipes": len(recipes),
        "subrecipes": SubRecipe.select().count(),
        "main_ings": RecipeIngredient.select().count(),
        "sub_ings": SubRecipeIngredient.select().count(),
        "empty_main_ings": empty_main_ings,
        "empty_main_steps": empty_main_steps,
        "empty_sub_ings": empty_sub_ings,
        "empty_sub_steps": empty_sub_steps,
        "orphan_subs": orphan_subs,
        "duplicate_titles": dupes,
        "issues": issues,
    }


def collect_unique_ingredients() -> list[str]:
    create_tables()
    names: set[str] = set()
    for row in RecipeIngredient.select(RecipeIngredient.ingredients_text):
        t = (row.ingredients_text or "").strip()
        if t:
            names.add(t)
    for row in SubRecipeIngredient.select(SubRecipeIngredient.ingredients_text):
        t = (row.ingredients_text or "").strip()
        if t:
            names.add(t)
    return sorted(names, key=lambda s: s.casefold())


def _looks_bad_top(query: str, display: str) -> str | None:
    q = query.casefold()
    n = display.casefold()
    for hint in _BAD_TOP_HINTS:
        if hint in n and hint not in q:
            return f"top dudoso («{hint}»)"
    # Caldo/vinagre/paté si no se buscan
    if "caldo" in n and "caldo" not in q and "fumet" not in q:
        return "top es caldo sin pedirlo"
    if "vinagre" in n and "vinagre" not in q and "vino" in q:
        return "vino → vinagre"
    if ("paté" in n or "pate " in n) and "paté" not in q and "pate" not in q:
        return "top es paté"
    return None


def audit_products(api: str, ingredients: list[str], sleep: float = 0.35) -> dict:
    ok = []
    empty = []
    bad = []
    errors = []

    for i, name in enumerate(ingredients, 1):
        try:
            data = _post(api, "/searchIngredient", {"ingredient": name})
            products = data.get("products") or []
            if not products:
                empty.append(name)
            else:
                top = products[0]
                display = top.get("display_name") or top.get("name") or ""
                reason = _looks_bad_top(name, display)
                tier = top.get("_match_tier", top.get("match_tier"))
                # Preferir is_best_match del tier 0
                best = [p for p in products if p.get("is_best_match")]
                sample = best[0] if best else top
                sample_name = sample.get("display_name") or sample.get("name") or display
                if reason:
                    bad.append(
                        {
                            "ingredient": name,
                            "top": sample_name,
                            "reason": reason,
                            "tier": tier,
                        }
                    )
                else:
                    ok.append(name)
        except urllib.error.HTTPError as exc:
            errors.append({"ingredient": name, "error": f"HTTP {exc.code}"})
        except Exception as exc:  # noqa: BLE001
            errors.append({"ingredient": name, "error": str(exc)[:160]})
        if i % 25 == 0:
            print(f"  … productos {i}/{len(ingredients)}")
        time.sleep(sleep)

    return {
        "total": len(ingredients),
        "ok": len(ok),
        "empty": empty,
        "bad": bad,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default="http://127.0.0.1:5000")
    parser.add_argument("--skip-products", action="store_true")
    args = parser.parse_args()

    print("=== ESTRUCTURA ===")
    struct = audit_structure()
    print(
        f"Recetas={struct['recipes']} Subrecetas={struct['subrecipes']} "
        f"IngMain={struct['main_ings']} IngSub={struct['sub_ings']}"
    )
    print(f"Main sin ingredientes: {len(struct['empty_main_ings'])}")
    print(f"Main sin pasos: {len(struct['empty_main_steps'])}")
    print(f"Sub sin ingredientes: {len(struct['empty_sub_ings'])}")
    for x in struct["empty_sub_ings"][:20]:
        print(f"  - {x}")
    print(f"Sub sin pasos: {len(struct['empty_sub_steps'])}")
    for x in struct["empty_sub_steps"][:20]:
        print(f"  - {x}")
    print(f"Huérfanas: {struct['orphan_subs']}")
    print(f"Títulos duplicados: {len(struct['duplicate_titles'])}")
    for t in struct["duplicate_titles"][:15]:
        print(f"  - {t}")

    if args.skip_products:
        return 0

    ings = collect_unique_ingredients()
    print(f"\n=== PRODUCTOS ({len(ings)} únicos) vía {args.api} ===")
    prod = audit_products(args.api, ings)
    print(
        f"Total={prod['total']} OK={prod['ok']} "
        f"Vacío={len(prod['empty'])} Malos={len(prod['bad'])} Err={len(prod['errors'])}"
    )
    if prod["empty"]:
        print("Vacío:")
        for n in prod["empty"][:40]:
            print(f"  - {n}")
    if prod["bad"]:
        print("Malos:")
        for row in prod["bad"][:40]:
            print(f"  - {row['ingredient']} → {row['top']} [{row['reason']}]")
    if prod["errors"]:
        print("Errores:")
        for row in prod["errors"][:20]:
            print(f"  - {row['ingredient']}: {row['error']}")

    struct_ok = (
        not struct["empty_main_ings"]
        and not struct["empty_sub_ings"]
        and not struct["orphan_subs"]
        and not struct["issues"]
    )
    prod_ok = not prod["empty"] and not prod["bad"] and not prod["errors"]
    print("\n=== VEREDICTO ===")
    print(f"Estructura: {'OK' if struct_ok else 'REVISAR'}")
    print(f"Productos: {'OK' if prod_ok else 'REVISAR'}")
    print("Main: no tocado (solo cuando lo pidas).")
    return 0 if struct_ok and prod_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
