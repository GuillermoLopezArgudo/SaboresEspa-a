<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="card p-4 shadow-lg" style="width: 400px;">
      <h1 class="text-center mb-4">Iniciar Sesión</h1>
      <form @submit.prevent="OnSubmit">
        <div class="mb-3">
          <label for="email" class="form-label">Correo:</label>
          <input type="email" id="email" v-model="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña:</label>
          <input type="password" id="password" v-model="password" class="form-control" required />
        </div>
        <div class="d-grid gap-2">
          <input type="submit" value="Iniciar Sesión" class="btn btn-primary" />
        </div>
      </form>
      <div class="text-center mt-3">
        <router-link to="/register">¿No tienes cuenta? Regístrate aquí</router-link>
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

//Cuando se pulsa en enviar llamamos al back por la referencia /login y le pasamos los valores del objeto de payload y restorna el token, iduser los idFavs y los almacena en el localstorage
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
/* General background and layout */
body {
  background-color: #f8f9fa;
}

/* Card styling */
.card {
  border-radius: 8px;
}

.card p {
  font-size: 1.2rem;
}

/* Text centering and spacing for the form */
form {
  padding: 2rem;
}

h1 {
  color: #007bff;
  font-size: 2rem;
  font-weight: bold;
}

/* Input and label styling */
input[type='email'],
input[type='password'] {
  border-radius: 5px;
}

.form-label {
  font-weight: bold;
  color: #333;
}

/* Button styling */
input[type='submit'] {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
  padding: 10px;
  font-size: 1.1rem;
  border-radius: 5px;
}

input[type='submit']:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

/* Link styling */
router-link {
  color: #007bff;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}
</style>
