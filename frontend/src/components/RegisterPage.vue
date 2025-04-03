<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="p-6 shadow-lg rounded-lg w-[400px] bg-white">
      <h1 class="text-center text-blue-600 text-2xl font-bold mb-4">Registrarse</h1>
      <form @submit.prevent="OnSubmit">
        <div class="mb-4">
          <label for="name" class="block text-gray-700 font-semibold">Nombre:</label>
          <input id="name" class="w-full p-2 border border-gray-300 rounded-md" v-model="name"  />
        </div>
        <div class="mb-4">
          <label for="email" class="block text-gray-700 font-semibold">Correo:</label>
          <input type="email" id="email" class="w-full p-2 border border-gray-300 rounded-md" v-model="email"  />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 font-semibold">Contraseña:</label>
          <input type="password" id="password" class="w-full p-2 border border-gray-300 rounded-md" v-model="password"  pattern=".{8,}" />
          <small class="text-sm text-gray-500">La contraseña debe tener al menos 8 caracteres.</small>
        </div>
        <div class="mb-4">
          <label for="confirmPassword" class="block text-gray-700 font-semibold">Confirmar Contraseña:</label>
          <input type="password" id="confirmPassword" class="w-full p-2 border border-gray-300 rounded-md" v-model="confirmPassword"  pattern=".{8,}" />
        </div>
        <div class="mb-4">
          <label for="type" class="block text-gray-700 font-semibold">Tipo de usuario:</label>
          <select id="type" class="w-full p-2 border border-gray-300 rounded-md" v-model="type" >
            <option value="user">Usuario</option>
            <option value="admin">Administrador</option>
          </select>
        </div>
        <div class="mb-4">
          <input type="submit" value="Registrar" class="w-full py-2 bg-blue-600 text-white text-lg rounded-md hover:bg-blue-700 transition" />
        </div>
      </form>
      <div class="text-center mt-3">
        <router-link to="/login" class="text-blue-600 hover:underline">¿Ya tienes cuenta? Iniciar sesión</router-link>
      </div>
      <div v-if="error" class="mt-3 p-4 bg-red-100 text-red-600 border border-red-300 rounded-md">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from "vue-router";
import axios from 'axios';

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const type = ref('user');
const error = ref('');
const router = useRouter();

// Función que cuando se pulsa en enviar llama al back por la referencia /register
function OnSubmit() {
  if (password.value === confirmPassword.value) {
    const payload = {
      name: name.value,
      email: email.value,
      password: password.value,
      type: type.value,
    };
    axios.post('http://localhost:5000/register', payload)
      .then(response => {
        if (response.data.userToken) {
          localStorage.setItem("userToken", response.data.userToken);
          localStorage.setItem("iduser", response.data.iduser);
          router.push({ name: "home" });
        } else {
          error.value = response.data.message;
          name.value = '';
          email.value = '';
          password.value = '';
          confirmPassword.value = '';
          type.value = 'user';
        }
        setTimeout(() => {
          error.value = '';
        }, 3000);
      })
      .catch(err => {
        error.value = err.response?.data?.message || "Hubo un problema con el servidor. Intenta más tarde.";
        setTimeout(() => {
          error.value = '';
        }, 3000);
      });
  } else {
    error.value = "LAS CONTRASEÑAS NO SON IGUALES";
    setTimeout(() => {
      error.value = '';
    }, 3000);
  }
}
</script>
