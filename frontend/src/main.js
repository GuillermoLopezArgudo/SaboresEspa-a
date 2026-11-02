import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './api' // interceptors JWT
import 'font-awesome/css/font-awesome.min.css'
import './assets/css/tailwind.css'

createApp(App).use(router).mount('#app')
