# ---- Etapa de construcción del frontend ----
    FROM node:16 as frontend-builder

    WORKDIR /frontend
    COPY frontend/package*.json ./
    RUN npm ci --silent
    COPY frontend .
    RUN npm run build
    
    # ---- Etapa del backend ----
    FROM python:3.9-slim
    
    # Instala dependencias del sistema
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
    COPY models.py .
    COPY config.py .
    
    # Copia el frontend construido
    COPY --from=frontend-builder /frontend/dist /static
    
    # Crea directorios para uploads
    RUN mkdir -p /app/static/images /app/static/videos
    
    # Puerto expuesto
    EXPOSE 5000
    
    # Comando de inicio
    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]