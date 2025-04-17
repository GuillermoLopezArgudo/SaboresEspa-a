import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './assets/css/tailwind.css'

// Toastification
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Crear la app
const app = createApp(App)

// Usar los plugins
app.use(router)
app.use(Toast) // 👈 Aquí es donde lo activas

app.mount('#app')
