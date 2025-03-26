<template>
  <div>
    <form @submit.prevent="OnSubmit">
      <h1>Registrarse</h1>
      <fieldset>
        <label for="name" class="form-label">Nombre:</label>
        <input id="nombre" class="form-control" v-model="name" required>
        <label for="email" class="form-label">Correo:</label>
        <input type="email" id="email" v-model="email" class="form-control" required />
        <label for="password" class="form-label">Password</label>
        <input pattern=".{8,}" type="password" id="password" v-model="password" class="form-control" required />
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input pattern=".{8,}" type="password" id="confirmPassword" v-model="confirmPassword" class="form-control"
          required />
        <select name="type" placeholder="Select" v-model="type">
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
        <input type="submit" value="Enviar" />
      </fieldset>
      <router-link to="/login">¿Iniciar Sesión?</router-link>
    </form>
    <div v-if="error">
      <p class="alert alert-danger">{{ error }}</p>
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
const type = ref('');
const confirmPassword = ref('');
const router = useRouter();
const error = ref('');

function OnSubmit() {
  if (password.value === confirmPassword.value) {
    const payload = {
      name: name.value,
      email: email.value,
      password: password.value,
      type: type.value
    };
    axios.post('http://localhost:5000/register', payload)
    
      .then(response => {
        if (response.data.usertoken) {  
          localStorage.setItem("userToken", response.data.usertoken);
          localStorage.setItem("iduser", response.data.iduser);
          router.push({ name: "home" });
        } else {
          error.value = response.data.message;
          name.value='';
          email.value='';
          password.value='';
          confirmPassword.value='';
          type.value='';
        }
        setTimeout(() => {
          error.value = '';
        }, 3000);
      })
      .catch(error => {
        error.value = error.response?.data?.message || "Hubo un problema con el servidor. Intenta más tarde.";
        setTimeout(() => {
          error.value = '';
        }, 3000);
      });
  } else {
    error.value = "LAS CONTRASEÑAS NO SON IGUALES";
    setTimeout(() => {
      error.value = "";
    }, 3000)
  }
}

</script>

<style></style>