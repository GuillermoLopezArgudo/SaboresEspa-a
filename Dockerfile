#FROM python:3.9-slim

#RUN apt-get update && apt-get install -y \
#    pkg-config \
#    libmariadb-dev-compat \
#    build-essential \
#    && rm -rf /var/lib/apt/lists/*

#WORKDIR /app

#COPY requirements.txt /app/

#RUN pip install --no-cache-dir -r requirements.txt

#COPY . /app/

#EXPOSE 5000

#CMD ["python", "app.py"]


# ---- Etapa 1: Construcción del Frontend ----
# Basado en tu frontend/Dockerfile pero optimizado para producción
FROM node:16 as frontend-builder

WORKDIR /frontend

# Copia solo los archivos necesarios para npm install (mejora el caching de capas)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --silent

# Copia el resto y construye
COPY frontend .
RUN npm run build

# ---- Etapa 2: Backend ----
# Basado en tu Dockerfile raíz pero optimizado
FROM python:3.9-slim

# Instala dependencias del sistema (las que tenías en tu original)
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia el backend
COPY app.py .

# Copia el frontend construido (desde la etapa 1)
COPY --from=frontend-builder /frontend/dist /static

# Puerto expuesto (el de tu backend)
EXPOSE 5000

# Usa Gunicorn para producción en lugar de python directamente
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]