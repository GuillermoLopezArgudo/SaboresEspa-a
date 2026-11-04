"""Borra recetas demo cortas (1–8) y reescribe las nuevas con textos largos y pasos reales."""
from __future__ import annotations

import base64
import sys
import time
from pathlib import Path

import requests

API = "https://sabores-espana-api.onrender.com"
CACHE = Path(__file__).resolve().parent / "_media_cache"
CACHE.mkdir(exist_ok=True)

OLD_ACCOUNTS = {
    "ana.cocina.49665@demo.sabores.es": "DemoPass123",
    "carlos.chef.49665@demo.sabores.es": "DemoPass123",
    "lucia.fogones.49665@demo.sabores.es": "DemoPass123",
}
NEW_PASS = "DemoPass123!"
NEW_ACCOUNTS = {
    "ana.cocina.real@demo.sabores.es": [10, 11, 12],
    "carlos.chef.real@demo.sabores.es": [13, 14, 15],
    "lucia.fogones.real@demo.sabores.es": [16, 17],
}
COMMENTERS = [
    "miguel.tapas.real@demo.sabores.es",
    "sofia.mesa.real@demo.sabores.es",
    "pedro.horno.real@demo.sabores.es",
]

# Contenido largo y realista (sin abreviaturas AOVE)
RECIPES = {
    10: {
        "title": "Tortilla de patatas española",
        "description": (
            "La tortilla de patatas es uno de los platos más reconocibles de la cocina española "
            "y, al mismo tiempo, de los más discutidos: con cebolla o sin ella, poco hecha o "
            "cuajada del todo, en láminas o en dados. Esta versión busca el equilibrio de casa: "
            "patata pochada despacio en Aceite de Oliva Virgen Extra para que quede melosa, "
            "huevo de calidad y un punto jugoso en el centro sin llegar a crudo.\n\n"
            "Sirve para 3–4 personas como plato principal o para picar en frío al día siguiente. "
            "El truco está en escurrir bien la patata, dejar reposar la mezcla un par de minutos "
            "y manejar el fuego medio-bajo al cuajar, dando la vuelta con un plato ancho. "
            "Si te gusta más cremosa, acorta el tiempo del segundo lado."
        ),
        "typeeat": "maindishes",
        "ccaa": "castillaleon",
        "time": "30a60",
        "proteins": ["huevo", "vegetariana"],
        "video": "https://www.youtube.com/watch?v=w_3YM-DZVOE",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Tortilla_de_patatas_con_cebolla.jpg/1280px-Tortilla_de_patatas_con_cebolla.jpg",
        "ingredients": [
            ("Patatas (monalisa, kennebec o agria)", "700 g aprox."),
            ("Huevos frescos M/L", "6 unidades"),
            ("Cebolla dulce (opcional pero recomendada)", "1 mediana"),
            ("Aceite de Oliva Virgen Extra", "250–300 ml para pochar"),
            ("Sal fina", "al gusto (aprox. 1 cucharadita)"),
        ],
        "steps": [
            {
                "title": "Preparar patata y cebolla",
                "description": (
                    "Pela las patatas y córtalas en láminas de unos 2–3 mm (ni papel ni trozos "
                    "gruesos). Si usas cebolla, límpiala y córtala en juliana fina. Reserva. "
                    "Cuanto más uniforme sea el corte, más pareja quedará la cocción."
                ),
                "image": "https://images.pexels.com/photos/1656663/pexels-photo-1656663.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Pochar en Aceite de Oliva Virgen Extra",
                "description": (
                    "Cubre el fondo de una sartén amplia con Aceite de Oliva Virgen Extra y "
                    "calienta a fuego medio-bajo. Incorpora la patata (y la cebolla a los 5 "
                    "minutos). Debe pochar, no freír: remueve de vez en cuando 18–25 minutos "
                    "hasta que la patata esté tierna al pincharla. Sala ligeramente."
                ),
                "image": "https://images.pexels.com/photos/4253312/pexels-photo-4253312.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Mezclar con el huevo",
                "description": (
                    "Escurre muy bien la patata en un colador (reserva el aceite limpio para "
                    "otras tortilla). En un bol amplio bate los huevos con sal. Añade la "
                    "patata, mezcla con cuidado y deja reposar 2–3 minutos para que el huevo "
                    "se impregne."
                ),
                "image": "https://images.pexels.com/photos/824635/pexels-photo-824635.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Cuajar y dar la vuelta",
                "description": (
                    "En sartén antiadherente (24–26 cm) con un hilo del Aceite de Oliva "
                    "Virgen Extra de pochar, vierte la mezcla a fuego medio-bajo. Cuando "
                    "los bordes cuajen (4–6 min), despega con espátula, coloca un plato "
                    "encima, dale la vuelta y termina 2–4 minutos más según el punto "
                    "deseado. Reposa 1 minuto antes de cortar."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Tortilla_de_Patatas_%28Corte_transversal%29.jpg/1280px-Tortilla_de_Patatas_%28Corte_transversal%29.jpg",
            },
        ],
        "comments": [
            ("miguel.tapas.real@demo.sabores.es", "Quedó cremosita por dentro, tal cual me gusta en casa."),
            ("sofia.mesa.real@demo.sabores.es", "¿Cuánto Aceite de Oliva Virgen Extra reutilizáis después de pochar?"),
            ("ana.cocina.real@demo.sabores.es", "Yo lo filtro y lo uso para otra tortilla o un pisto."),
            ("pedro.horno.real@demo.sabores.es", "Sin cebolla también sale genial estilo Betanzos, poco hecha."),
        ],
    },
    11: {
        "title": "Gazpacho andaluz",
        "description": (
            "El gazpacho andaluz es una sopa fría de hortalizas crudas emulsionadas con "
            "Aceite de Oliva Virgen Extra y un toque de vinagre de Jerez. No es un zumo "
            "de tomate: bien hecho tiene cuerpo, frescor y un equilibrio entre dulzor del "
            "tomate maduro, verdor del pimiento y el contrapunto ácido.\n\n"
            "La clave está en la materia prima (tomates de temporada, bien rojos) y en "
            "triturar hasta obtener una textura fina; si lo pasas por chino o colador, "
            "queda todavía más sedoso. Enfríalo al menos una hora. Ideal como entrante "
            "de verano o bebida ligera en jarra con hielo."
        ),
        "typeeat": "soups",
        "ccaa": "andalucia",
        "time": "menos15",
        "proteins": ["vegana", "vegetariana"],
        "video": "https://www.youtube.com/watch?v=Q155S4hWaLk",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Gazpacho_Cazuela_Barro.jpg/1280px-Gazpacho_Cazuela_Barro.jpg",
        "ingredients": [
            ("Tomates maduros (pera o ensalada)", "1 kg"),
            ("Pimiento verde italiano", "1 unidad (aprox. 100–120 g)"),
            ("Pepino", "1/2–1 pequeño (pelado)"),
            ("Ajo", "1–2 dientes (sin germen)"),
            ("Pan de hogaza del día anterior", "40–60 g"),
            ("Aceite de Oliva Virgen Extra", "60–80 ml"),
            ("Vinagre de Jerez", "2–3 cucharadas"),
            ("Agua muy fría", "100–250 ml según espesor"),
            ("Sal", "al gusto"),
        ],
        "steps": [
            {
                "title": "Lavar y trocear",
                "description": (
                    "Lava bien tomates, pimiento y pepino. Retira el pedúnculo del tomate "
                    "y las pepitas/blancos del pimiento. Pela el pepino si la piel es gruesa. "
                    "Trocea todo en trozos manejables. Remoja el pan en un poco de agua si "
                    "está muy duro."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Gazpacho_ingredients.png",
            },
            {
                "title": "Triturar y emulsionar",
                "description": (
                    "Pon las hortalizas en el vaso con el pan, sal, vinagre y parte del "
                    "Aceite de Oliva Virgen Extra. Tritura a máxima potencia. Sin dejar de "
                    "batir, añade el resto del aceite en hilo para emulsionar. Ajusta con "
                    "agua fría hasta la textura que prefieras (más espeso tipo sopa o más "
                    "ligero para beber)."
                ),
                "image": "https://images.pexels.com/photos/1327838/pexels-photo-1327838.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Colar y enfriar",
                "description": (
                    "Pasa por chino o colador fino apretando con cuchara si quieres un "
                    "resultado sin pieles ni semillas. Prueba y rectifica sal, vinagre o "
                    "aceite. Enfría mínimo 1–2 horas. Sirve solo o con tropezones de "
                    "pepino, tomate y un chorrito de Aceite de Oliva Virgen Extra."
                ),
                "image": None,
            },
        ],
        "comments": [
            ("sofia.mesa.real@demo.sabores.es", "Con tomate pera bien maduro sale dulce y perfecto."),
            ("carlos.chef.real@demo.sabores.es", "Quita el germen del ajo: marca la diferencia y no repite."),
            ("miguel.tapas.real@demo.sabores.es", "En mi casa le ponemos un poco de cebolleta; ¿alguien más?"),
        ],
    },
    12: {
        "title": "Patatas bravas",
        "description": (
            "Las patatas bravas son el tapeo por excelencia: dados de patata crujientes "
            "por fuera y tiernos por dentro, coronados con una salsa brava de tomate y "
            "pimentón con picante controlado, y a menudo un contrapunto de alioli.\n\n"
            "Para que no queden aceitosas conviene secar bien la patata y, si puedes, "
            "freír en dos tiempos (primero suave para cocer, después fuerte para dorar). "
            "La salsa se hace en minutos: sofrito de ajo, pimentón sin quemar y tomate. "
            "Rectifica el picante al gusto de la mesa."
        ),
        "typeeat": "starters",
        "ccaa": "madrid",
        "time": "30a60",
        "proteins": ["vegetariana"],
        "video": None,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Patatas_bravas._Tapa_de_bar_%28Espa%C3%B1a%29.jpg/1280px-Patatas_bravas._Tapa_de_bar_%28Espa%C3%B1a%29.jpg",
        "ingredients": [
            ("Patatas para freír", "800 g–1 kg"),
            ("Aceite para freír (girasol o mezcla)", "la necesaria"),
            ("Tomate triturado o frito", "200–250 g"),
            ("Ajo", "2 dientes"),
            ("Pimentón dulce", "1 cucharadita colmada"),
            ("Guindilla / cayena / chile", "al gusto"),
            ("Aceite de Oliva Virgen Extra", "2 cucharadas para la salsa"),
            ("Sal", "al gusto"),
            ("Alioli o mayonesa", "para acompañar (opcional)"),
        ],
        "steps": [
            {
                "title": "Cortar y secar las patatas",
                "description": (
                    "Pela las patatas y córtalas en dados de 2–2,5 cm. Enjuaga en agua "
                    "fría para quitar almidón superficial y sécalas muy bien con un paño "
                    "limpio: el agua es enemiga del crujiente."
                ),
                "image": "https://images.pexels.com/photos/1583884/pexels-photo-1583884.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Freír en dos tiempos",
                "description": (
                    "Calienta el aceite a unos 150–160 °C y fríe las patatas 6–8 minutos "
                    "hasta que estén cocidas pero poco doradas. Escurre. Sube a 180–190 °C "
                    "y vuelve a freír 2–4 minutos hasta dorar. Sala al salir."
                ),
                "image": "https://images.pexels.com/photos/1893556/pexels-photo-1893556.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Salsa brava y emplatado",
                "description": (
                    "En una sartén con Aceite de Oliva Virgen Extra sofríe el ajo laminado "
                    "sin quemarlo. Retira del fuego, añade pimentón y remueve; incorpora "
                    "tomate, picante y sal. Cocina 5–8 minutos a fuego medio hasta espesar. "
                    "Sirve las patatas con brava y, si quieres, alioli."
                ),
                "image": None,
            },
        ],
        "comments": [
            ("pedro.horno.real@demo.sabores.es", "En Madrid la brava tiene que picar de verdad."),
            ("ana.cocina.real@demo.sabores.es", "Si quieres menos aceite, al horno a 210 °C con un chorrito también funcionan."),
            ("miguel.tapas.real@demo.sabores.es", "Alioli + brava es la combinación ganadora."),
        ],
    },
    13: {
        "title": "Paella valenciana",
        "description": (
            "La paella valenciana tradicional se cocina en paella ancha, con fuego "
            "repartido, arroz bomba o similar de grano corto, y un sofrito profundo de "
            "carnes y verdura. Los ingredientes clásicos giran en torno a pollo, conejo, "
            "bajoqueta (judía verde plana), garrofón, tomate, azafrán, pimentón, romero "
            "y Aceite de Oliva Virgen Extra.\n\n"
            "Regla de oro: una vez echas el arroz, no se remueve. El caldo debe estar "
            "sabroso antes de añadir el grano; el socarrat del final es premio, no "
            "castigo. Calcula unas 6–8 raciones según el diámetro de tu paella."
        ),
        "typeeat": "maindishes",
        "ccaa": "valencia",
        "time": "mas60",
        "proteins": ["pollo", "conejo"],
        "video": "https://www.youtube.com/watch?v=vWySIREExjo",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/01_Paella_Valenciana_original.jpg/1280px-01_Paella_Valenciana_original.jpg",
        "ingredients": [
            ("Arroz bomba (o D.O. Valencia)", "500–800 g según paella"),
            ("Pollo en trozos", "1 kg aprox."),
            ("Conejo en trozos", "500 g aprox."),
            ("Judía verde plana (bajoqueta)", "200–350 g"),
            ("Garrofón (fresco, congelado o conserva)", "150–200 g"),
            ("Tomates maduros rallados", "2 grandes / 350–400 g"),
            ("Aceite de Oliva Virgen Extra", "75–100 ml"),
            ("Pimentón dulce", "1 cucharadita"),
            ("Azafrán en hebra", "una pizca generosa"),
            ("Romero fresco", "1–2 ramitas"),
            ("Sal y agua", "hasta los remaches de la paella"),
        ],
        "steps": [
            {
                "title": "Dorado de las carnes",
                "description": (
                    "Calienta Aceite de Oliva Virgen Extra en la paella a fuego fuerte. "
                    "Sala y dora el pollo y el conejo por todos lados hasta color profundo: "
                    "ese tostado será la base del caldo. Reserva un poco de espacio en el "
                    "centro si tu fuego lo permite."
                ),
                "image": "https://images.pexels.com/photos/4253312/pexels-photo-4253312.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Verdura, tomate y especias",
                "description": (
                    "Añade la bajoqueta y el garrofón; sofríe un par de minutos. Incorpora "
                    "el tomate rallado y cocina hasta que pierda agua. En un lateral tuesta "
                    "ligero el azafrán; añade pimentón y remueve enseguida para que no se "
                    "queme."
                ),
                "image": "https://images.pexels.com/photos/533280/pexels-photo-533280.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Caldo",
                "description": (
                    "Cubre con agua hasta pasar un poco los remaches de las asas. Cuece "
                    "unos 20–25 minutos (fuerte al principio, luego medio). Añade romero, "
                    "prueba la sal y retira el romero antes del arroz. El caldo debe saber "
                    "ya a paella."
                ),
                "image": None,
            },
            {
                "title": "Arroz y reposo",
                "description": (
                    "Reparte el arroz en cruz o en lluvia sin amontonarlo. No lo remuevas. "
                    "Cocina unos 18 minutos (más fuerte al inicio). Si hace falta, rectifica "
                    "con un chorrito de agua caliente solo en zonas secas. Reposa 5 minutos "
                    "tapada con un paño antes de servir."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/01_Paella_Valenciana_original.jpg/1280px-01_Paella_Valenciana_original.jpg",
            },
        ],
        "comments": [
            ("pedro.horno.real@demo.sabores.es", "¿Sin conejo se puede? En casa a veces solo llevamos pollo."),
            ("carlos.chef.real@demo.sabores.es", "Se puede y queda rica, pero ya no es la versión más clásica."),
            ("lucia.fogones.real@demo.sabores.es", "El socarrat del final es lo mejor de la paella."),
            ("miguel.tapas.real@demo.sabores.es", "El romero al final marca muchísimo el aroma."),
        ],
    },
    14: {
        "title": "Pulpo a la gallega",
        "description": (
            "El pulpo a la gallega (polbo á feira) es simple y exigente a la vez: pulpo "
            "tierno, cachelos de patata, pimentón, sal gruesa y un buen chorro de Aceite "
            "de Oliva Virgen Extra en crudo.\n\n"
            "Congelar el pulpo un par de días ayuda a ablandar las fibras. La cocción "
            "depende del tamaño (suele ir de 30 a 45 minutos). Después conviene dejarlo "
            "reposar en su agua unos minutos. Se sirve en tabla de madera o plato ancho, "
            "nunca nadando en caldo."
        ),
        "typeeat": "maindishes",
        "ccaa": "galicia",
        "time": "30a60",
        "proteins": ["pulpo"],
        "video": None,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/El_Pulpo_a_la_gallega%2C_t%C3%ADpica_tapa_espa%C3%B1ola.jpg/1280px-El_Pulpo_a_la_gallega%2C_t%C3%ADpica_tapa_espa%C3%B1ola.jpg",
        "ingredients": [
            ("Pulpo limpio", "1–1,5 kg"),
            ("Patatas para cachelos", "4–6 medianas"),
            ("Pimentón dulce", "1–2 cucharaditas"),
            ("Pimentón picante", "al gusto (opcional)"),
            ("Sal gruesa", "al gusto"),
            ("Aceite de Oliva Virgen Extra", "chorro generoso al servir"),
            ("Hoja de laurel", "1 (opcional en la cocción)"),
        ],
        "steps": [
            {
                "title": "Cocer el pulpo",
                "description": (
                    "Si está congelado, descongélalo en nevera. Hierve agua abundante (con "
                    "laurel si quieres). 'Asusta' el pulpo sumergiéndolo 3 veces unos "
                    "segundos. Cocina 30–45 minutos según tamaño. Apaga y deja reposar "
                    "10–15 minutos en el agua."
                ),
                "image": "https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Cachelos",
                "description": (
                    "Cuece las patatas con piel en agua con sal hasta que estén tiernas. "
                    "Pélalas en caliente y córtalas en rodajas gruesas. Reserva un poco "
                    "del agua del pulpo por si quieres humedecer la base (sin encharcar)."
                ),
                "image": None,
            },
            {
                "title": "Montar y aliñar",
                "description": (
                    "Corta el pulpo en rodajas. Dispon cachelos y pulpo. Espolvorea sal "
                    "gruesa y pimentón (dulce y un toque picante si te gusta). Termina con "
                    "un chorro generoso de Aceite de Oliva Virgen Extra en crudo. Sirve "
                    "al momento."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Polbo_%C3%A1_feira._Galiza.jpg/1280px-Polbo_%C3%A1_feira._Galiza.jpg",
            },
        ],
        "comments": [
            ("miguel.tapas.real@demo.sabores.es", "Yo siempre lo congelo 48 h: queda más tierno."),
            ("lucia.fogones.real@demo.sabores.es", "Congelar ayuda a romper fibras, sí. Buen consejo."),
            ("sofia.mesa.real@demo.sabores.es", "Un pimentón un poco ahumado le da un punto brutal."),
        ],
    },
    15: {
        "title": "Crema catalana",
        "description": (
            "La crema catalana es el postre de yema infusionada con leche, canela y "
            "piel de limón, cuajada con maicena y terminada con una costra de azúcar "
            "caramelizado. Se parece a la crème brûlée, pero su perfil aromático es "
            "claramente mediterráneo.\n\n"
            "No dejes hervir a borbotones la mezcla de yemas o puede cortarse. Enfría "
            "bien antes de azucarar y quemar con soplete o plancha muy caliente. Sirve "
            "fresca, recién quemada, para contrastar la crema fría con el caramelo "
            "caliente."
        ),
        "typeeat": "dessert",
        "ccaa": "catalunya",
        "time": "30a60",
        "proteins": ["huevo"],
        "video": None,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Crema_catalana._Postre.jpg/1280px-Crema_catalana._Postre.jpg",
        "ingredients": [
            ("Leche entera", "500 ml"),
            ("Yemas de huevo", "4"),
            ("Azúcar", "100 g + extra para quemar"),
            ("Maicena", "1 cucharada sopera colmada"),
            ("Canela en rama", "1 rama"),
            ("Piel de limón", "1 tira sin blanco amargo"),
        ],
        "steps": [
            {
                "title": "Infusionar la leche",
                "description": (
                    "Calienta la leche con la canela y la piel de limón hasta casi hervir. "
                    "Retira, tapa y deja infusionar 10 minutos. Cuela y vuelve a calentar "
                    "suavemente."
                ),
                "image": "https://images.pexels.com/photos/1126359/pexels-photo-1126359.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Ligar yemas y cuajar",
                "description": (
                    "Bate yemas con el azúcar y la maicena hasta integrar. Añade la leche "
                    "caliente en hilo sin dejar de remover. Vuelve a la cazuela a fuego "
                    "bajo-medio y cocina removiendo hasta espesar (no hervir fuerte). "
                    "Reparte en cazuelitas."
                ),
                "image": None,
            },
            {
                "title": "Enfriar y quemar",
                "description": (
                    "Enfría primero a temperatura ambiente y luego en nevera al menos 2 "
                    "horas. Espolvorea una capa fina de azúcar y carameliza con soplete "
                    "(o plancha muy caliente). Sirve al momento."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Cazuelita_con_crema_catalana._Postre.jpg/1280px-Cazuelita_con_crema_catalana._Postre.jpg",
            },
        ],
        "comments": [
            ("sofia.mesa.real@demo.sabores.es", "Con el soplete la costra queda perfecta."),
            ("carlos.chef.real@demo.sabores.es", "Sin soplete: una plancha bien caliente encima del azúcar."),
            ("lucia.fogones.real@demo.sabores.es", "La canela en rama no puede faltar."),
        ],
    },
    16: {
        "title": "Bacalao al pil-pil",
        "description": (
            "El bacalao al pil-pil es una joya de la cocina vasca: lomos desalados "
            "confitados en Aceite de Oliva Virgen Extra a temperatura controlada, "
            "emulsionando el propio colágeno del pescado hasta obtener una salsa "
            "ligera y brillante.\n\n"
            "La dificultad no está en la lista de ingredientes (es corta) sino en el "
            "gesto: movimiento constante de la cazuela y no pasarse de temperatura "
            "(orientativamente 60–70 °C). Un bacalao bien desalado y un buen Aceite de "
            "Oliva Virgen Extra hacen el 80% del plato."
        ),
        "typeeat": "maindishes",
        "ccaa": "paisvasco",
        "time": "30a60",
        "proteins": ["bacalao"],
        "video": None,
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Bacalao_al_Pil_Pil_%28Vizcaya%29.jpg",
        "ingredients": [
            ("Lomos de bacalao desalado", "4 (aprox. 600–800 g)"),
            ("Aceite de Oliva Virgen Extra", "200–250 ml"),
            ("Ajos", "4–5 dientes laminados"),
            ("Guindilla cayena", "1 (opcional)"),
        ],
        "steps": [
            {
                "title": "Preparar el bacalao",
                "description": (
                    "Si parte de bacalao en salazón, desálalo cambiando el agua según "
                    "instrucciones (suele requerir varias horas/días). Seca muy bien los "
                    "lomos con papel de cocina y déjalos atemperar 20 minutos."
                ),
                "image": "https://images.pexels.com/photos/725991/pexels-photo-725991.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Perfumar el aceite",
                "description": (
                    "En cazuela baja calienta el Aceite de Oliva Virgen Extra a fuego "
                    "suave con los ajos laminados y la guindilla. Cuando los ajos estén "
                    "dorados claros, retíralos (y la guindilla). El aceite debe oler, no "
                    "humear."
                ),
                "image": None,
            },
            {
                "title": "Confitar y emulsionar el pil-pil",
                "description": (
                    "Coloca el bacalao piel abajo. Mantén fuego mínimo. Mueve la cazuela "
                    "en círculos o con vaivén suave para que el colágeno emulsionen el "
                    "aceite (pil-pil). En 8–15 minutos la salsa debe espesar ligeramente. "
                    "Si se parte, ayuda con un colador chino y vuelve a ligar. Sirve con "
                    "los ajos por encima."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Bacalao-pil-pil-vaionnoth.jpg",
            },
        ],
        "comments": [
            ("miguel.tapas.real@demo.sabores.es", "La clave es no pasar de 60–70 °C en el aceite."),
            ("pedro.horno.real@demo.sabores.es", "Me costó emulsionar: un colador ayuda a recuperar la salsa."),
            ("lucia.fogones.real@demo.sabores.es", "Sí: cuelas un poco, vuelves a la cazuela y ligas otra vez."),
        ],
    },
    17: {
        "title": "Pimientos del piquillo rellenos de bacalao",
        "description": (
            "Los pimientos del piquillo rellenos son un plato de fiesta navarra: el "
            "dulzor asado del piquillo envuelve una brandada o relleno suave de bacalao, "
            "y se napan con una salsa hecha a partir de los propios pimientos.\n\n"
            "Puedes usar piquillos de bote de buena calidad (escurridos con mimo para "
            "no romperlos). El relleno debe estar sabroso pero no seco; una bechamel "
            "ligera o un poco de nata ayuda a ligar. Gratina solo lo justo para calentar "
            "y dorar sin resecar."
        ),
        "typeeat": "maindishes",
        "ccaa": "navarra",
        "time": "30a60",
        "proteins": ["bacalao"],
        "video": None,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Tapa_de_pimientos_del_piquillo_rellenos.jpg/1280px-Tapa_de_pimientos_del_piquillo_rellenos.jpg",
        "ingredients": [
            ("Pimientos del piquillo", "12–16 unidades"),
            ("Bacalao desalado desmigado", "300 g"),
            ("Cebolla", "1 mediana"),
            ("Leche o nata líquida", "100 ml"),
            ("Harina", "1 cucharada sopera"),
            ("Aceite de Oliva Virgen Extra", "3–4 cucharadas"),
            ("Sal", "al gusto"),
            ("Pimentón dulce", "1 pizca (opcional en la salsa)"),
        ],
        "steps": [
            {
                "title": "Preparar el relleno (brandada ligera)",
                "description": (
                    "Pochar la cebolla picada fina en Aceite de Oliva Virgen Extra hasta "
                    "transparente. Añade una cucharada de harina, remueve y vierte leche "
                    "o nata hasta espesar ligeramente. Incorpora el bacalao desmigado, "
                    "prueba la sal y deja enfriar un poco para rellenar con facilidad."
                ),
                "image": "https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg?auto=compress&cs=tinysrgb&w=1200",
            },
            {
                "title": "Rellenar los piquillos",
                "description": (
                    "Escurre los pimientos. Con una cucharilla, rellénalos sin forzar para "
                    "no romper la piel. Colócalos en una fuente de horno ligeramente "
                    "aceitada, juntos pero sin aplastarlos."
                ),
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Piquillo_Peppers.jpg/1280px-Piquillo_Peppers.jpg",
            },
            {
                "title": "Salsa y gratinado",
                "description": (
                    "Tritura 2–3 pimientos de reserva (o restos) con un chorrito de Aceite "
                    "de Oliva Virgen Extra, un poco del líquido del bote y una pizca de "
                    "pimentón si te gusta. Napa los rellenos, calienta/gratina 5–8 minutos "
                    "a 180–200 °C y sirve."
                ),
                "image": None,
            },
        ],
        "comments": [
            ("sofia.mesa.real@demo.sabores.es", "Los de bote de calidad merecen mucho la pena."),
            ("ana.cocina.real@demo.sabores.es", "Quedaron perfectos para una cena de viernes."),
            ("carlos.chef.real@demo.sabores.es", "Un toque de pimentón dulce en la salsa redondea el plato."),
        ],
    },
}


def download(url: str | None, key: str) -> dict | None:
    if not url:
        return None
    path = CACHE / f"up_{key}.bin"
    if path.exists() and path.stat().st_size > 2000:
        data = path.read_bytes()
    else:
        candidates = [url]
        if "900px-" in url:
            candidates.append(url.replace("900px-", "1280px-"))
        candidates.append(
            "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1200"
        )
        data = None
        for candidate in candidates:
            try:
                print(f"  DL {candidate[:90]}...")
                r = requests.get(
                    candidate,
                    timeout=120,
                    headers={
                        "User-Agent": "SaboresEspanaSeed/3.0 (recipe upgrade; github GuillermoLopezArgudo)"
                    },
                    allow_redirects=True,
                )
                r.raise_for_status()
                if len(r.content) < 2000:
                    continue
                data = r.content
                path.write_bytes(data)
                time.sleep(0.5)
                break
            except Exception as exc:
                print(f"  fail: {exc}")
        if data is None:
            return None
    ext = ".png" if data.startswith(b"\x89PNG") else ".jpg"
    return {"name": f"{key}{ext}", "base64": base64.b64encode(data).decode("ascii")}


def login(email: str, password: str) -> str:
    r = requests.post(f"{API}/login", json={"email": email, "password": password}, timeout=90)
    r.raise_for_status()
    return r.json()["userToken"]


def delete_old() -> None:
    mapping = {
        "ana.cocina.49665@demo.sabores.es": [1, 2],
        "carlos.chef.49665@demo.sabores.es": [3, 4, 5],
        "lucia.fogones.49665@demo.sabores.es": [6, 7, 8],
    }
    for email, ids in mapping.items():
        token = login(email, OLD_ACCOUNTS[email])
        for rid in ids:
            r = requests.post(
                f"{API}/deleteRecipe",
                headers={"Authorization": f"Bearer {token}"},
                json={"idrecipe": rid},
                timeout=60,
            )
            print(f"delete {rid}: {r.status_code} {r.text[:80]}")


def replace_comments(token_by_email: dict[str, str], recipe_id: int, threads: list[tuple[str, str]]) -> None:
    # borra comentarios actuales del recipe intentando con cada user (solo propios)
    cr = requests.post(f"{API}/viewComment", json={"idrecipe": recipe_id}, timeout=60)
    if cr.status_code < 400:
        for c in cr.json().get("comment_list") or []:
            for email, token in token_by_email.items():
                dr = requests.post(
                    f"{API}/deleteComment",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"idcomment": c["id"]},
                    timeout=60,
                )
                if dr.status_code < 400:
                    break
    for email, text in threads:
        token = token_by_email.get(email)
        if not token:
            continue
        r = requests.post(
            f"{API}/createComment",
            headers={"Authorization": f"Bearer {token}"},
            json={"idrecipe": recipe_id, "comment": text},
            timeout=60,
        )
        print(f"  comment {email.split('@')[0]}: {r.status_code}")
        time.sleep(0.2)


def upgrade_recipe(email: str, token: str, recipe_id: int, data: dict, token_by_email: dict[str, str]) -> None:
    print(f"\n== {recipe_id} {data['title']} ==")
    main = download(data.get("image"), f"r{recipe_id}_main")
    steps_out = []
    for i, step in enumerate(data["steps"]):
        step_payload = {
            "title": step["title"],
            "description": step["description"],
        }
        img = download(step.get("image"), f"r{recipe_id}_s{i}")
        if img:
            step_payload["image"] = img
        steps_out.append(step_payload)

    payload = {
        "idrecipe": recipe_id,
        "title": data["title"],
        "description": data["description"],
        "visibility": True,
        "ingredients": [x[0] for x in data["ingredients"]],
        "quantities": [x[1] for x in data["ingredients"]],
        "steps": steps_out,
        "typeeat": data.get("typeeat") or "",
        "ccaa": data.get("ccaa") or "",
        "time": data.get("time") or "",
        "proteins": data.get("proteins") or [],
    }
    if main:
        payload["image"] = main
    if data.get("video"):
        payload["video"] = data["video"]

    r = requests.post(
        f"{API}/editRecipe",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=300,
    )
    if r.status_code >= 400:
        print(f"FAIL edit {recipe_id}: {r.status_code} {r.text[:300]}")
        return
    print("  edited ok")
    replace_comments(token_by_email, recipe_id, data.get("comments") or [])


def main() -> int:
    print("1) Borrar demos cortas 1–8")
    delete_old()

    print("\n2) Login cuentas nuevas + comentaristas")
    token_by_email: dict[str, str] = {}
    for email in list(NEW_ACCOUNTS) + COMMENTERS:
        token_by_email[email] = login(email, NEW_PASS)
        print(" login", email)

    print("\n3) Reescribir fichas largas")
    for email, ids in NEW_ACCOUNTS.items():
        token = token_by_email[email]
        for rid in ids:
            upgrade_recipe(email, token, rid, RECIPES[rid], token_by_email)

    print("\nDONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
