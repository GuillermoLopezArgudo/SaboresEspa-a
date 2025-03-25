# Dockerfile para el Frontend con Node.js

# Usamos la imagen base de Node.js
FROM node:16

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de configuración
COPY package.json /app/
COPY package-lock.json /app/

# Instalamos las dependencias
RUN npm install

# Copiamos todo el código fuente
COPY . /app/

# Exponemos el puerto 8080
EXPOSE 8080

# Comando para arrancar el servidor de desarrollo de Vue.js
CMD ["npm", "run", "serve"]
