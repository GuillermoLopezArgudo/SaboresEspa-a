import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/css/tailwind.css'

import PrimeVue from 'primevue/config';


// Toastification
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Crear la app
const app = createApp(App)

// Usar los plugins
app.use(router)
app.use(Toast) // 👈 Aquí es donde lo activas
app.use(PrimeVue);


app.mount('#app')
