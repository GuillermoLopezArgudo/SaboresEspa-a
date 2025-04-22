# Usa Node oficial
FROM node:16

# Directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY package*.json ./

# Instala dependencias
RUN npm install

# Copia el resto del código fuente
COPY . .

# Construye la app
RUN npm run build

# Instala 'serve' para servir archivos estáticos
RUN npm install -g serve

# Expón el puerto para producción
EXPOSE 8080

# Sirve el contenido estático de 'dist'
CMD ["serve", "-s", "dist", "-l", "8080"]
