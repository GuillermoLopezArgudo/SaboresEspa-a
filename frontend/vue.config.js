/*const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})*/

module.exports = {
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    hot: true,
    liveReload: true,
    watchFiles: ['src/**/*'],
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    allowedHosts: 'all', // 👈 Reemplaza disableHostCheck con esto
  },
};




