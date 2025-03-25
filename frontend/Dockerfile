# Dockerfile para el Frontend

# Usamos la imagen base de Node.js
FROM node:16 AS build

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de configuración
COPY package.json /app/
COPY package-lock.json /app/

# Instalamos las dependencias
RUN npm install

# Copiamos todo el código fuente
COPY . /app/

# Construimos el proyecto de Vue
RUN npm run build

# Usamos Nginx para servir los archivos estáticos
FROM nginx:alpine

# Copiamos el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiamos los archivos de construcción de Vue al directorio de Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Exponemos el puerto 80
EXPOSE 80
