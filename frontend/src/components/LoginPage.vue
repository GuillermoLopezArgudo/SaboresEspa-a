<template>
  <div>
    <form @submit.prevent="OnSubmit">
      <h1>Iniciar Sesión</h1>
      <fieldset>
        <label for="email" class="form-label">Correo:</label>
        <input type="email" id="email" v-model="email" class="form-control" required/>
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" required/>
        <input type="submit" value="Enviar" />
      </fieldset>
      <router-link to="/register">¿Registrar?</router-link>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from "vue-router";
import axios from 'axios';

const router = useRouter();

const email = ref('');
const password = ref('');

function OnSubmit() {
  
  const payload = {
    email:email.value,
    password:password.value,
  }
  axios.post('http://localhost:5000/login', payload)
    .then(response => {
      localStorage.setItem("userToken", response.data.usertoken);
      localStorage.setItem("iduser", response.data.iduser);
      router.push({ name: "home" });
    })
    .catch(error => {
      console.log(error)
    })
  


}



</script>

<style></style>