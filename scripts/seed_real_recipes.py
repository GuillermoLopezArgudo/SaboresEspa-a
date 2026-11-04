"""Crea recetas españolas reales con fotos, vídeos (solo si son de esa receta) y comentarios.

Uso:
  python scripts/seed_real_recipes.py
  python scripts/seed_real_recipes.py --api https://sabores-espana-api.onrender.com
"""
from __future__ import annotations

import argparse
import base64
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(__file__).resolve().parent / "_media_cache"
CACHE.mkdir(exist_ok=True)

PASS = "DemoPass123!"

AUTHORS = [
    {
        "name": "Ana Cocina",
        "email": "ana.cocina.real@demo.sabores.es",
        "recipes": ["tortilla", "gazpacho", "bravas"],
    },
    {
        "name": "Carlos Chef",
        "email": "carlos.chef.real@demo.sabores.es",
        "recipes": ["paella", "pulpo", "crema"],
    },
    {
        "name": "Lucía Fogones",
        "email": "lucia.fogones.real@demo.sabores.es",
        "recipes": ["bacalao", "pimientos"],
    },
]

COMMENTERS = [
    {"name": "Miguel Tapas", "email": "miguel.tapas.real@demo.sabores.es"},
    {"name": "Sofía Mesa", "email": "sofia.mesa.real@demo.sabores.es"},
    {"name": "Pedro Horno", "email": "pedro.horno.real@demo.sabores.es"},
]

# Solo vídeos YouTube que son claramente ESA receta. Si no hay match fiable → None.
RECIPES = {
    "tortilla": {
        "title": "Tortilla de patatas española",
        "description": (
            "La tortilla de patatas clásica: patata pochada en AOVE, huevo y cebolla "
            "opcional. Jugosa por dentro y dorada por fuera. Ideal para 4 raciones."
        ),
        "typeeat": "maindishes",
        "ccaa": "castillaleon",
        "time": "15a30",
        "proteins": ["huevo", "vegetariana"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Tortilla_de_patatas_con_cebolla.jpg/1280px-Tortilla_de_patatas_con_cebolla.jpg",
        "video": "https://www.youtube.com/watch?v=w_3YM-DZVOE",
        "ingredients": [
            ("Patatas", "600 g"),
            ("Huevos", "6 unidades"),
            ("Cebolla", "1 mediana (opcional)"),
            ("Aceite de oliva virgen extra", "250 ml aprox."),
            ("Sal", "al gusto"),
        ],
        "steps": [
            {
                "title": "Cortar y pochar",
                "description": (
                    "Pela las patatas y córtalas en láminas finas. Pocha a fuego suave "
                    "en AOVE 15–20 min con la cebolla en juliana. Escurre bien."
                ),
                "image": "https://images.pexels.com/photos/1656663/pexels-photo-1656663.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Mezclar con el huevo",
                "description": (
                    "Bate los huevos con sal. Incorpora la patata escurrida, mezcla y "
                    "deja reposar 2–3 minutos."
                ),
                "image": "https://images.pexels.com/photos/824635/pexels-photo-824635.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Cuajar y dar la vuelta",
                "description": (
                    "En sartén antiadherente a fuego medio-bajo, cuaja un lado, da la "
                    "vuelta con un plato y termina al punto que prefieras."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Tortilla_de_Patatas_%28Corte_transversal%29.jpg/1280px-Tortilla_de_Patatas_%28Corte_transversal%29.jpg",
            },
        ],
        "comments": [
            ("miguel.tapas.real@demo.sabores.es", "Quedó cremosita por dentro, tal cual me gusta."),
            ("sofia.mesa.real@demo.sabores.es", "¿Cuánto AOVE reutilizáis después de pochar?"),
            ("ana.cocina.real@demo.sabores.es", "Yo lo filtro y lo uso para otra tortilla o pisto."),
            ("pedro.horno.real@demo.sabores.es", "Sin cebolla también sale genial estilo Betanzos."),
        ],
    },
    "gazpacho": {
        "title": "Gazpacho andaluz",
        "description": (
            "Sopa fría andaluza de tomate, pimiento, pepino y ajo. Refrescante, "
            "ligera y lista en minutos. Mejor con tomates bien maduros."
        ),
        "typeeat": "soups",
        "ccaa": "andalucia",
        "time": "menos15",
        "proteins": ["vegana", "vegetariana"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Gazpacho_Cazuela_Barro.jpg/1280px-Gazpacho_Cazuela_Barro.jpg",
        "video": "https://www.youtube.com/watch?v=Q155S4hWaLk",
        "ingredients": [
            ("Tomates maduros", "1 kg"),
            ("Pimiento verde italiano", "1"),
            ("Pepino", "1/2–1"),
            ("Ajo", "1–2 dientes"),
            ("Pan duro", "50 g"),
            ("AOVE", "50–80 ml"),
            ("Vinagre de Jerez", "2–3 cucharadas"),
            ("Sal y agua fría", "al gusto"),
        ],
        "steps": [
            {
                "title": "Trocear hortalizas",
                "description": "Lava y trocea tomate, pimiento, pepino y ajo. Remoja el pan si está muy duro.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Gazpacho_ingredients.png",
            },
            {
                "title": "Triturar y colar",
                "description": (
                    "Tritura con AOVE, vinagre, sal y un poco de agua. Pasa por chino "
                    "si quieres textura fina. Enfría 1–2 h."
                ),
                "image": "https://images.pexels.com/photos/1327838/pexels-photo-1327838.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
        ],
        "comments": [
            ("sofia.mesa.real@demo.sabores.es", "Lo hice ayer con tomate pera: 10/10."),
            ("carlos.chef.real@demo.sabores.es", "Tip: quita el germen del ajo para que no repita."),
            ("miguel.tapas.real@demo.sabores.es", "¿Le ponéis cebolla? En mi casa sí, poquita."),
        ],
    },
    "paella": {
        "title": "Paella valenciana",
        "description": (
            "Arroz en paella con pollo, conejo, bajoqueta, garrofón, tomate, azafrán "
            "y romero. Sin remover el arroz tras echarlo. 6–8 raciones."
        ),
        "typeeat": "maindishes",
        "ccaa": "valencia",
        "time": "mas60",
        "proteins": ["pollo", "conejo"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/01_Paella_Valenciana_original.jpg/1280px-01_Paella_Valenciana_original.jpg",
        "video": "https://www.youtube.com/watch?v=vWySIREExjo",
        "ingredients": [
            ("Arroz bomba", "500–800 g según paella"),
            ("Pollo", "1 kg en trozos"),
            ("Conejo", "500 g en trozos"),
            ("Judía verde plana (bajoqueta)", "150–350 g"),
            ("Garrofón", "150 g"),
            ("Tomate rallado", "2 grandes / 400 g"),
            ("AOVE", "75 ml"),
            ("Azafrán y pimentón dulce", "al gusto"),
            ("Romero, sal y agua", "hasta remaches"),
        ],
        "steps": [
            {
                "title": "Sofreír carnes",
                "description": "Dora bien pollo y conejo en AOVE con sal. El tostado marca el sabor del caldo.",
                "image": "https://images.pexels.com/photos/4253312/pexels-photo-4253312.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Verdura y tomate",
                "description": "Añade bajoqueta y garrofón, sofríe. Incorpora tomate y reduce. Tosta azafrán/pimentón sin quemar.",
                "image": "https://images.pexels.com/photos/533280/pexels-photo-533280.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Caldo y arroz",
                "description": (
                    "Cubre con agua hasta remaches, cuece ~20–25 min, prueba sal, "
                    "añade arroz y no remuevas. Reposa 5 min."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/01_Paella_Valenciana_original.jpg/1280px-01_Paella_Valenciana_original.jpg",
            },
        ],
        "comments": [
            ("pedro.horno.real@demo.sabores.es", "¿Sin conejo se puede? En casa a veces solo pollo."),
            ("carlos.chef.real@demo.sabores.es", "Se puede, pero ya no es la DO clásica. Sigue quedando rica."),
            ("lucia.fogones.real@demo.sabores.es", "El socarrat al final es lo mejor."),
            ("miguel.tapas.real@demo.sabores.es", "Probada: el romero al final marca muchísimo."),
        ],
    },
    "pulpo": {
        "title": "Pulpo a la gallega",
        "description": (
            "Pulpo cocido tierno con cachelos, pimentón dulce/picante y AOVE. "
            "Clásico de feria y domingo en Galicia."
        ),
        "typeeat": "maindishes",
        "ccaa": "galicia",
        "time": "30a60",
        "proteins": ["pulpo"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/El_Pulpo_a_la_gallega%2C_t%C3%ADpica_tapa_espa%C3%B1ola.jpg/1280px-El_Pulpo_a_la_gallega%2C_t%C3%ADpica_tapa_espa%C3%B1ola.jpg",
        "video": None,
        "ingredients": [
            ("Pulpo", "1–1,5 kg"),
            ("Patatas", "4–5 medianas"),
            ("Pimentón dulce", "1–2 cucharaditas"),
            ("Pimentón picante", "opcional"),
            ("AOVE", "chorro generoso"),
            ("Sal gruesa", "al gusto"),
        ],
        "steps": [
            {
                "title": "Cocer el pulpo",
                "description": "Congelado descongelado o fresco asustado. Cuece 30–45 min según tamaño. Reposa en el agua 15 min.",
                "image": "https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Cachelos y emplatar",
                "description": "Cuece patatas, córtalas. Corta pulpo, monta, sal gruesa, pimentón y AOVE en crudo.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Polbo_%C3%A1_feira._Galiza.jpg/1280px-Polbo_%C3%A1_feira._Galiza.jpg",
            },
        ],
        "comments": [
            ("miguel.tapas.real@demo.sabores.es", "¿Congelado o fresco? Yo siempre congelado 48 h."),
            ("lucia.fogones.real@demo.sabores.es", "Congelado ayuda a ablandar las fibras, sí."),
            ("sofia.mesa.real@demo.sabores.es", "El pimentón ahumado le da un punto brutal."),
        ],
    },
    "bravas": {
        "title": "Patatas bravas",
        "description": (
            "Patatas fritas con salsa brava de tomate/pimentón y alioli suave. "
            "Tapeo imprescindible."
        ),
        "typeeat": "starters",
        "ccaa": "madrid",
        "time": "30a60",
        "proteins": ["vegetariana"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Patatas_bravas._Tapa_de_bar_%28Espa%C3%B1a%29.jpg/1280px-Patatas_bravas._Tapa_de_bar_%28Espa%C3%B1a%29.jpg",
        "video": None,
        "ingredients": [
            ("Patatas", "800 g"),
            ("Tomate frito / triturado", "200 g"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Guindilla o cayena", "al gusto"),
            ("Ajo", "2 dientes"),
            ("Mayonesa o alioli", "para acompañar"),
            ("Aceite para freír y sal", ""),
        ],
        "steps": [
            {
                "title": "Freír patatas",
                "description": "Corta en dados, seca bien y fríe en dos tiempos si puedes: primero suave, luego fuerte.",
                "image": "https://images.pexels.com/photos/1583884/pexels-photo-1583884.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Salsa brava",
                "description": "Sofríe ajo, pimentón y tomate. Ajusta picante y sal. Sirve con alioli.",
                "image": "https://images.pexels.com/photos/1893556/pexels-photo-1893556.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
        ],
        "comments": [
            ("pedro.horno.real@demo.sabores.es", "En Madrid la brava pica de verdad 🔥"),
            ("ana.cocina.real@demo.sabores.es", "Yo las hago al horno a 210 °C si quiero menos aceite."),
            ("miguel.tapas.real@demo.sabores.es", "Alioli + brava = combinación ganadora."),
        ],
    },
    "crema": {
        "title": "Crema catalana",
        "description": (
            "Postre de yema con leche, canela y piel de limón, cuajado y "
            "caramelizado con azúcar. Clásico de Catalunya."
        ),
        "typeeat": "dessert",
        "ccaa": "catalunya",
        "time": "30a60",
        "proteins": ["huevo"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Crema_catalana._Postre.jpg/1280px-Crema_catalana._Postre.jpg",
        "video": None,
        "ingredients": [
            ("Leche entera", "500 ml"),
            ("Yemas", "4"),
            ("Azúcar", "100 g + extra para quemar"),
            ("Maicena", "1 cucharada sopera"),
            ("Canela en rama", "1"),
            ("Piel de limón", "1 tira sin blanco"),
        ],
        "steps": [
            {
                "title": "Infusionar la leche",
                "description": "Calienta leche con canela y limón. Reserva 10 min y cuela.",
                "image": "https://images.pexels.com/photos/1126359/pexels-photo-1126359.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Cuajar y quemar",
                "description": (
                    "Mezcla yemas, azúcar y maicena; incorpora leche caliente. "
                    "Cuece sin hervir fuerte. Enfría, azucara y quema."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Cazuelita_con_crema_catalana._Postre.jpg/1280px-Cazuelita_con_crema_catalana._Postre.jpg",
            },
        ],
        "comments": [
            ("sofia.mesa.real@demo.sabores.es", "Quedó con costra perfecta con el soplete."),
            ("carlos.chef.real@demo.sabores.es", "Sin soplete: plancha bien caliente encima del azúcar."),
            ("lucia.fogones.real@demo.sabores.es", "La canela no puede faltar."),
        ],
    },
    "bacalao": {
        "title": "Bacalao al pil-pil",
        "description": (
            "Bacalao desalado confitado en AOVE emulsionado con el propio "
            "colágeno del pescado. Joya de la cocina vasca."
        ),
        "typeeat": "maindishes",
        "ccaa": "paisvasco",
        "time": "30a60",
        "proteins": ["bacalao"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Bacalao_al_Pil_Pil_%28Vizcaya%29.jpg",
        "video": None,
        "ingredients": [
            ("Lomos de bacalao desalado", "4"),
            ("AOVE", "200–250 ml"),
            ("Ajos", "4–5 dientes laminados"),
            ("Guindilla", "1 (opcional)"),
        ],
        "steps": [
            {
                "title": "Preparar el bacalao",
                "description": "Desala bien y seca. Reserva a temperatura ambiente 20 min.",
                "image": "https://images.pexels.com/photos/725991/pexels-photo-725991.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Emulsionar el pil-pil",
                "description": (
                    "Dora ajos en AOVE suave, retira. Confita el bacalao piel abajo "
                    "y mueve la cazuela en círculos hasta emulsionar."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Bacalao-pil-pil-vaionnoth.jpg",
            },
        ],
        "comments": [
            ("miguel.tapas.real@demo.sabores.es", "La clave es no pasar de 60–70 °C en el aceite."),
            ("pedro.horno.real@demo.sabores.es", "Me costó emulsionar: ¿usáis un colador para ayudar?"),
            ("lucia.fogones.real@demo.sabores.es", "Sí, a veces cuelo un poco de salsa y vuelvo a ligar."),
        ],
    },
    "pimientos": {
        "title": "Pimientos del piquillo rellenos de bacalao",
        "description": (
            "Piquillos rellenos de brandada suave de bacalao, napados con "
            "salsa de los propios pimientos. Elegante y de fiesta."
        ),
        "typeeat": "maindishes",
        "ccaa": "navarra",
        "time": "30a60",
        "proteins": ["bacalao"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Tapa_de_pimientos_del_piquillo_rellenos.jpg/1280px-Tapa_de_pimientos_del_piquillo_rellenos.jpg",
        "video": None,
        "ingredients": [
            ("Pimientos del piquillo", "12–16"),
            ("Bacalao desalado", "300 g"),
            ("Cebolla", "1"),
            ("Leche o nata", "100 ml"),
            ("AOVE y harina", "para bechamel ligera"),
            ("Sal", "al gusto"),
        ],
        "steps": [
            {
                "title": "Brandada",
                "description": "Pochar cebolla, añadir bacalao desmigado y ligar con un poco de bechamel/nata.",
                "image": "https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg?auto=compress&cs=tinysrgb&w=900",
            },
            {
                "title": "Rellenar y gratinar",
                "description": "Rellena piquillos, napa con salsa de pimiento triturado y gratina 5–8 min.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Piquillo_Peppers.jpg/1280px-Piquillo_Peppers.jpg",
            },
        ],
        "comments": [
            ("sofia.mesa.real@demo.sabores.es", "Los de bote de calidad valen mucho la pena."),
            ("ana.cocina.real@demo.sabores.es", "Quedaron perfectos para cena de viernes."),
            ("carlos.chef.real@demo.sabores.es", "Prueba a añadir un toque de pimentón dulce a la salsa."),
        ],
    },
}


def _candidate_urls(url: str) -> list[str]:
    urls = [url]
    if "/thumb/" in url and "900px-" in url:
        urls.append(url.replace("900px-", "1280px-"))
    if "/thumb/" in url and "1280px-" in url:
        urls.append(url.replace("1280px-", "1024px-"))
    # Pexels food fallback
    urls.append(
        "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1200"
    )
    # dedupe preserve order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def download(url: str, key: str) -> dict:
    path = CACHE / f"{key}.bin"
    if path.exists() and path.stat().st_size > 2000:
        data = path.read_bytes()
    else:
        data = None
        last_err = None
        for candidate in _candidate_urls(url):
            try:
                print(f"  DL {candidate[:90]}...")
                r = requests.get(
                    candidate,
                    timeout=120,
                    headers={
                        "User-Agent": (
                            "SaboresEspanaSeed/2.0 "
                            "(https://github.com/GuillermoLopezArgudo/SaboresEspa-a; recipe demo seed)"
                        )
                    },
                    allow_redirects=True,
                )
                r.raise_for_status()
                data = r.content
                if len(data) < 2000:
                    raise RuntimeError(f"imagen demasiado pequeña: {key}")
                path.write_bytes(data)
                time.sleep(0.6)
                break
            except Exception as exc:
                last_err = exc
                print(f"  fail: {exc}")
                continue
        if data is None:
            raise RuntimeError(f"no image for {key}: {last_err}")
    ext = ".jpg"
    if data.startswith(b"\x89PNG"):
        ext = ".png"
    return {"name": f"{key}{ext}", "base64": base64.b64encode(data).decode("ascii")}


def ensure_user(api: str, name: str, email: str) -> str:
    r = requests.post(
        f"{api}/login",
        json={"email": email, "password": PASS},
        timeout=90,
    )
    if r.status_code == 200:
        return r.json()["userToken"]
    r = requests.post(
        f"{api}/register",
        json={"name": name, "email": email, "password": PASS},
        timeout=90,
    )
    if r.status_code in (200, 201):
        return r.json()["userToken"]
    if r.status_code == 409:
        r2 = requests.post(
            f"{api}/login",
            json={"email": email, "password": PASS},
            timeout=90,
        )
        r2.raise_for_status()
        return r2.json()["userToken"]
    raise RuntimeError(f"register/login {email}: {r.status_code} {r.text[:300]}")


def find_recipe_id(api: str, token: str, title: str) -> int | None:
    r = requests.post(
        f"{api}/viewRecipes",
        headers={"Authorization": f"Bearer {token}"},
        json={"all": True},
        timeout=90,
    )
    r.raise_for_status()
    body = r.json()
    items = body.get("recipe_list") or body.get("message") or []
    if not isinstance(items, list):
        items = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if (item.get("title") or "").strip().casefold() == title.casefold():
            return int(item["id"])
    return None


def create_recipe(api: str, token: str, key: str, data: dict) -> int:
    existing = find_recipe_id(api, token, data["title"])
    if existing:
        print(f"  ya existe id={existing}")
        return existing

    main = download(data["image"], f"{key}_main")
    steps_out = []
    for i, step in enumerate(data["steps"]):
        img = download(step["image"], f"{key}_s{i}")
        steps_out.append(
            {
                "title": step["title"],
                "description": step["description"],
                "image": img,
            }
        )

    payload = {
        "title": data["title"],
        "description": data["description"],
        "visibility": True,
        "image": main,
        "ingredients": [i[0] for i in data["ingredients"]],
        "quantities": [i[1] for i in data["ingredients"]],
        "steps": steps_out,
        "typeeat": data.get("typeeat") or "",
        "ccaa": data.get("ccaa") or "",
        "time": data.get("time") or "",
        "proteins": data.get("proteins") or [],
    }
    if data.get("video"):
        payload["video"] = data["video"]

    r = requests.post(
        f"{api}/create",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=300,
    )
    if r.status_code >= 400:
        # Si el backend aún no acepta YouTube, reintenta sin vídeo
        if data.get("video") and "vídeo" in (r.text or "").casefold():
            print("  backend sin YouTube aún → creo sin vídeo")
            payload.pop("video", None)
            r = requests.post(
                f"{api}/create",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
                timeout=300,
            )
        if r.status_code >= 400:
            raise RuntimeError(f"create {key}: {r.status_code} {r.text[:400]}")

    rid = r.json().get("idrecipe")
    if not rid:
        time.sleep(1)
        rid = find_recipe_id(api, token, data["title"])
    if not rid:
        raise RuntimeError(f"no id for {data['title']}")
    print(f"  creada id={rid}" + (" +youtube" if data.get("video") else ""))
    return int(rid)


def post_comments(api: str, tokens: dict[str, str], recipe_id: int, threads: list[tuple[str, str]]):
    for email, text in threads:
        token = tokens.get(email)
        if not token:
            continue
        r = requests.post(
            f"{api}/createComment",
            headers={"Authorization": f"Bearer {token}"},
            json={"idrecipe": recipe_id, "comment": text},
            timeout=60,
        )
        if r.status_code >= 400:
            print(f"  comment fail {email}: {r.status_code} {r.text[:160]}")
        else:
            print(f"  comment ok ({email.split('@')[0]})")
        time.sleep(0.3)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api",
        default="https://sabores-espana-api.onrender.com",
        help="Base URL de la API",
    )
    args = parser.parse_args()
    api = args.api.rstrip("/")

    print(f"API {api}")
    tokens: dict[str, str] = {}
    for person in AUTHORS + COMMENTERS:
        print(f"user {person['email']}")
        tokens[person["email"]] = ensure_user(api, person["name"], person["email"])

    created: dict[str, int] = {}
    for author in AUTHORS:
        token = tokens[author["email"]]
        for key in author["recipes"]:
            data = RECIPES[key]
            print(f"\n== {data['title']} ==")
            created[key] = create_recipe(api, token, key, data)

    print("\n== comentarios ==")
    for key, rid in created.items():
        threads = RECIPES[key].get("comments") or []
        print(f"\n{RECIPES[key]['title']} ({rid})")
        post_comments(api, tokens, rid, threads)

    print("\nDONE")
    print("Cuentas demo password:", PASS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
