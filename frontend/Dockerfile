# Usa la imagen oficial de Node.js
FROM node:16

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY package.json /app/
COPY package-lock.json /app/

# Instala las dependencias de Vue
RUN npm install

# Copia el resto de tu aplicación (src, public, etc.)
COPY . /app/

# Expón el puerto 8080 donde Vue sirve la aplicación
EXPOSE 8080

# Construye la aplicación de Vue para producción
RUN npm run build

# Define el comando para servir la aplicación en producción
CMD ["npm", "run", "serve"]
