# Usa una imagen base de Python
FROM python:3.9-slim

# Instalamos las dependencias necesarias para Peewee (MySQL)
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de dependencias de Python
COPY requirements.txt /app/

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Establecemos las variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copiamos el resto de la aplicación
COPY . /app/

# Exponemos el puerto que Flask va a usar
EXPOSE 5000

# Comando para iniciar Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
