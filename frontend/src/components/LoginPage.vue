<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="p-6 shadow-lg rounded-lg w-[400px] bg-white">
      <h1 class="text-center text-blue-600 text-2xl font-bold mb-4">Iniciar Sesión</h1>
      <form @submit.prevent="OnSubmit">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 font-semibold">Correo:</label>
          <input type="email" id="email" v-model="email" class="w-full p-2 border border-gray-300 rounded-md" required />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 font-semibold">Contraseña:</label>
          <input type="password" id="password" v-model="password" class="w-full p-2 border border-gray-300 rounded-md" required />
        </div>
        <div class="mb-4">
          <input type="submit" value="Iniciar Sesión" class="w-full py-2 bg-blue-600 text-white text-lg rounded-md hover:bg-blue-700 transition" />
        </div>
      </form>
      <div class="text-center mt-3">
        <router-link to="/register" class="text-blue-600 hover:underline">¿No tienes cuenta? Regístrate aquí</router-link>
      </div>
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

// Cuando se pulsa en enviar, llamamos al back por la referencia /login y le pasamos los valores del objeto de payload
// y retorna el token, iduser, idFavs y los almacena en el localStorage
function OnSubmit() {
  const payload = {
    email: email.value,
    password: password.value,
  };

  axios
    .post('http://localhost:5000/login', payload)
    .then((response) => {
      localStorage.setItem('userToken', response.data.usertoken);
      localStorage.setItem('iduser', response.data.iduser);
      localStorage.setItem('idFavs', response.data.idFavs);
      router.push({ name: 'home' });
    })
    .catch((error) => {
      console.error(error);
    });
}
</script>

<style scoped>

body {
  background-color: #f8f9fa;
}
</style>
