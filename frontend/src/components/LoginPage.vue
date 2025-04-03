<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50 to-amber-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-2xl overflow-hidden">
      <!-- Header con imagen -->
      <div class="bg-amber-700 py-6 px-8 text-center">
        <h1 class="text-3xl font-bold text-white font-serif">Bienvenido</h1>
        <p class="text-amber-100 mt-1">Inicia sesión en tu Recetario</p>
      </div>
      
      <!-- Formulario -->
      <form @submit.prevent="OnSubmit" class="p-8">
        <!-- Mensaje de error -->
        <div v-if="error" class="mb-6 p-3 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r-lg flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          {{ error }}
        </div>

        <!-- Campo Email -->
        <div class="mb-6">
          <label for="email" class="block text-amber-800 font-medium mb-2 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Correo electrónico
          </label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="w-full px-4 py-3 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm" 
            placeholder="tucorreo@ejemplo.com"
            required
          />
        </div>

        <!-- Campo Contraseña -->
        <div class="mb-6">
          <label for="password" class="block text-amber-800 font-medium mb-2 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Contraseña
          </label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            class="w-full px-4 py-3 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm" 
            placeholder="••••••••"
            required
          />
        </div>

        <!-- Botón de envío -->
        <button 
          type="submit" 
          class="w-full py-3 bg-gradient-to-r from-amber-600 to-amber-700 text-white font-bold rounded-lg shadow-lg hover:from-amber-700 hover:to-amber-800 transition duration-300 flex items-center justify-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
          Iniciar Sesión
        </button>

        <!-- Enlace a registro -->
        <div class="mt-6 text-center">
          <router-link 
            to="/register" 
            class="text-amber-600 hover:text-amber-800 font-medium transition duration-300 inline-flex items-center"
          >
            ¿No tienes cuenta? 
            <span class="ml-1 underline">Regístrate aquí</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const email = ref('');
const password = ref('');
const error = ref('')

function OnSubmit() {
  const payload = {
    email: email.value,
    password: password.value,
  };

  axios
    .post('http://localhost:5000/login', payload)
    .then((response) => {
      if (response.data.userToken) {
        localStorage.setItem('userToken', response.data.userToken);
        localStorage.setItem('iduser', response.data.iduser);
        router.push({ name: 'home' });
      } else {
        error.value = response.data.message;
        setTimeout(() => {
          error.value = '';
        }, 3000);
      }
    })
    .catch((err) => {
      error.value = err.response?.data?.message || 'Error al iniciar sesión';
      setTimeout(() => {
        error.value = '';
      }, 3000);
    });
}
</script>

<style scoped>
/* Animación para el mensaje de error */
.error-message {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Efecto para los inputs al enfocar */
input:focus {
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
  transition: all 0.2s ease;
}
</style>