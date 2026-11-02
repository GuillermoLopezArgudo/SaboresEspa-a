# SaboresEspaña

App fullstack de recetas (Vue 3 + Flask + Peewee).

## Estructura (rama `developer`)

```
app/                 # Backend Flask empaquetado
  config.py
  db.py
  models.py
  routes/            # Blueprints (auth, recipes, users, health, media)
  services/          # Utilidades (ficheros base64)
wsgi.py              # Entry point (Render / local)
frontend/            # Vue 3 (Vercel)
static/              # Imágenes y vídeos subidos
```

## Local (rápido)

Backend con **SQLite** (sin Docker):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py
```

API en `http://localhost:5000` → `/health`

Frontend:

```bash
cd frontend
npm install
npm run serve
```

Front en `http://localhost:8080` (usa `VUE_APP_API_URL=http://localhost:5000`).

## Producción

Igual que Balonmano: **Vercel** (frontend) + **Render** (`gunicorn wsgi:app`) + **Neon** (`DATABASE_URL`).
