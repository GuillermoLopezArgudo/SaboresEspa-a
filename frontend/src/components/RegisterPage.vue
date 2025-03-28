<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="card p-4 shadow-lg" style="width: 400px;">
      <h1 class="text-center mb-4">Registrarse</h1>
      <form @submit.prevent="OnSubmit">
        <div class="mb-3">
          <label for="name" class="form-label">Nombre:</label>
          <input id="name" class="form-control" v-model="name" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Correo:</label>
          <input type="email" id="email" class="form-control" v-model="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña:</label>
          <input type="password" id="password" class="form-control" v-model="password" required pattern=".{8,}" />
          <small class="form-text text-muted">La contraseña debe tener al menos 8 caracteres.</small>
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">Confirmar Contraseña:</label>
          <input type="password" id="confirmPassword" class="form-control" v-model="confirmPassword" required pattern=".{8,}" />
        </div>
        <div class="mb-3">
          <label for="type" class="form-label">Tipo de usuario:</label>
          <select id="type" class="form-select" v-model="type" required>
            <option value="user">Usuario</option>
            <option value="admin">Administrador</option>
          </select>
        </div>
        <div class="d-grid gap-2">
          <input type="submit" value="Registrar" class="btn btn-primary" />
        </div>
      </form>
      <div class="text-center mt-3">
        <router-link to="/login">¿Ya tienes cuenta? Iniciar sesión</router-link>
      </div>
      <div v-if="error" class="alert alert-danger mt-3">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from "vue-router";
import axios from 'axios';

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const type = ref('user');
const error = ref('');
const favs = reactive([]);
const router = useRouter();

//Funcion que cuando se pulsa en enviar llama al back por la referenica /register
function OnSubmit() {
  if (password.value === confirmPassword.value) {
    const payload = {
      name: name.value,
      email: email.value,
      password: password.value,
      type: type.value,
      favs: favs.value
    };
    axios.post('http://localhost:5000/register', payload)
      .then(response => {
        
        if (response.data.usertoken) {
          localStorage.setItem("userToken", response.data.usertoken);
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

<style scoped>
body {
  background-color: #f8f9fa;
}

.card {
  border-radius: 8px;
}

form {
  padding: 2rem;
}

h1 {
  color: #007bff;
  font-size: 2rem;
  font-weight: bold;
}

input[type="text"],
input[type="email"],
input[type="password"],
select {
  border-radius: 5px;
}

.form-label {
  font-weight: bold;
  color: #333;
}

input[type="submit"] {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
  padding: 10px;
  font-size: 1.1rem;
  border-radius: 5px;
}

input[type="submit"]:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

router-link {
  color: #007bff;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}

.alert {
  font-weight: bold;
  color: #dc3545;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}
</style>
