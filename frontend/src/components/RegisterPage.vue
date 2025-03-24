<template>
  <div>
    <form @submit.prevent="OnSubmit">
      <h1>Registrarse</h1>
      <fieldset>
        <label for="email" class="form-label">Correo:</label>
        <input type="email" id="email" v-model="email" class="form-control" required />
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" required />
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" class="form-control" required />
        <input type="submit" value="Enviar" />
      </fieldset>
      <router-link to="/login">¿Iniciar Sesión?</router-link>
    </form>
  </div>
</template>

<script setup>

import { ref } from 'vue';
import { useRouter } from "vue-router";

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();

function OnSubmit() {
  console.log("Email:" + email.value)
  console.log("Password:" + password.value)
  console.log("Password:" + confirmPassword.value)
  router.push({ name: "home" });
}

</script>

<style></style>