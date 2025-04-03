/*const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})*/

module.exports = {
  devServer: {
    host: '0.0.0.0',  // Permite acceso desde Docker
    port: 8080,       // Usa el puerto expuesto
    hot: true,        // Activa Hot Module Replacement
    liveReload: true, // Permite la recarga automática
    watchFiles: ['src/**/*'], // Activa la observación de archivos
  }
};


