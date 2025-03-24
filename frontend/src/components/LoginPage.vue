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

const router = useRouter();

const email = ref('');
const password = ref('');

function OnSubmit() {
  console.log("Email:" + email.value)
  console.log("Password:" + password.value)
  router.push({ name: "home" });
}



</script>

<style></style>