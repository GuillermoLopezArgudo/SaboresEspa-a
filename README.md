# SaboresEspaña

App fullstack de recetas (Vue 3 + Flask + Peewee). Proyecto final de grado.

## Stack

- **Frontend:** Vue 3, Vue Router, Tailwind, Bootstrap (Vercel)
- **Backend:** Flask, JWT, Peewee (Render)
- **Base de datos:** PostgreSQL en Neon (producción) o MySQL local (docker-compose)

Misma arquitectura de despliegue que App Balonmano: **Vercel + Render + Neon**.

## Desarrollo local

### Backend

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

Con MySQL (docker):

```bash
docker compose up db -d
set MYSQL_HOST=127.0.0.1
set MYSQL_USER=root
set MYSQL_PASSWORD=1234
set MYSQL_DB=recipesSpain
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run serve
```

API por defecto: `http://localhost:5000` (`frontend/.env` → `VUE_APP_API_URL`).

## Despliegue (como Balonmano)

### 1. Neon (PostgreSQL)

1. Crea un proyecto en [neon.tech](https://neon.tech)
2. Copia la connection string (`postgresql://...?...sslmode=require`)

### 2. Render (API)

1. New → Web Service → repo `SaboresEspa-a` (o este fork)
2. Runtime: Python
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Variables:

| Key | Value |
|---|---|
| `DATABASE_URL` | connection string de Neon |
| `JWT_SECRET_KEY` | secreto largo aleatorio |
| `CORS_ORIGINS` | `https://TU-FRONT.vercel.app` |

URL ejemplo: `https://sabores-espana-api.onrender.com`

### 3. Vercel (frontend)

1. Importa la carpeta `frontend` (Root Directory: `frontend`)
2. Framework: Vue / otro
3. Build: `npm run build`
4. Output: `dist`
5. Env:

| Key | Value |
|---|---|
| `VUE_APP_API_URL` | `https://sabores-espana-api.onrender.com` |

Tras el deploy, actualiza `CORS_ORIGINS` en Render con la URL real de Vercel.

## Healthcheck

`GET /health` → `{ "status": "ok" }`
