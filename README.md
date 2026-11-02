# SaboresEspaña

App fullstack de recetas (Vue 3 + Vite + Flask + Peewee).

## Estructura (rama `developer`)

```
app/                 # Backend Flask
  config.py
  db.py
  models.py
  security.py
  rate_limit.py
  routes/
  services/          # uploads (Cloudinary o disco local)
wsgi.py
frontend/            # Vue 3 + Vite (Vercel)
scripts/promote_admin.py
tests/
static/
```

## Local

Backend (SQLite):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set USE_SQLITE=1
python wsgi.py
```

API: `http://localhost:5000` → `/health`

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Front: `http://localhost:8080` (`VITE_API_URL=http://localhost:5000`).

Promover admin:

```bash
set USE_SQLITE=1
python scripts/promote_admin.py tu@email.com
```

## Producción

**Vercel** (frontend) + **Render** (`gunicorn wsgi:app`) + **Neon** (`DATABASE_URL`).

Obligatorio en Render:

- `JWT_SECRET_KEY` (auto en `render.yaml`)
- `FLASK_ENV=production`
- `CORS_ORIGINS=https://sabores-espana-one.vercel.app`
- **Cloudinary** (`CLOUDINARY_CLOUD_NAME` + `API_KEY` + `API_SECRET`) para que las fotos no se pierdan al redeploy

En Vercel: `VITE_API_URL=https://sabores-espana-api.onrender.com`

## Tests

```bash
set USE_SQLITE=1
pytest tests -q
```
