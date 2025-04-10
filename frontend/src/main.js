import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './assets/css/tailwind.css'
import axios from 'axios';

axios.defaults.baseURL = 'https://localhost:5000';
axios.defaults.timeout = 10000; 

createApp(App).use(router).mount('#app');
