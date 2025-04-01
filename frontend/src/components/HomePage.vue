<template>
  <div>
    <h1 class="text-center mt-4 text-blue-600 text-3xl font-bold mb-8">Bienvenido a tu Recetario</h1>
    <nav class="bg-white shadow-sm mb-4">
      <div class="container mx-auto px-4 py-2 flex justify-between items-center">
        <router-link to="/" class="text-2xl text-blue-600 font-semibold">Recetario</router-link>
        <button class="lg:hidden px-3 py-2 border border-blue-600 rounded-md" type="button" @click="toggleNavbar">
          <span class="text-blue-600">☰</span>
        </button>
        <div v-show="!navbarOpen" class="lg:flex lg:ml-auto space-x-6">
          <router-link to="/create" class="text-gray-600 text-lg hover:text-blue-600">Crear receta</router-link>
          <router-link to="/recipes_personal" class="text-gray-600 text-lg hover:text-blue-600">Mis recetas</router-link>
          <router-link to="/" class="text-gray-600 text-lg hover:text-blue-600">Todas las recetas</router-link>
          <router-link to="/profile" class="text-gray-600 text-lg hover:text-blue-600">Ajustes</router-link>
          <router-link @click="closeSession" to="/login" class="text-gray-600 text-lg hover:text-blue-600">Cerrar sesión</router-link>
        </div>
      </div>
    </nav>
    <div class="container mx-auto px-4">
      <FavoriteRecipe></FavoriteRecipe>
    </div>
  </div>
</template>

<script setup>
import FavoriteRecipe from './FavoriteRecipe.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const userToken = ref(localStorage.getItem("userToken"));
const router = useRouter();
const navbarOpen = ref(false);

// Si no hay token en el localstorage envía al login
if (userToken.value == null) {
  router.push({ name: "login" });
}

// Cierra la sesión eliminando lo almacenado en el localStorage
function closeSession() {
  localStorage.clear();
}

// Función para manejar el toggle del navbar en pantallas pequeñas
function toggleNavbar() {
  navbarOpen.value = !navbarOpen.value;
}
</script>

<style scoped>
body {
  background-color: #f8f9fa;
  font-family: 'Arial', sans-serif;
}

.favorite-recipes {
  @apply grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10;
}

.favorite-recipes .recipe-card {
  @apply bg-white border border-gray-300 rounded-lg shadow-md p-4;
}

.favorite-recipes .recipe-card img {
  @apply w-full rounded-lg;
}

.favorite-recipes .recipe-card h5 {
  @apply text-xl text-gray-800 font-semibold;
}

.favorite-recipes .recipe-card .btn {
  @apply bg-blue-600 text-white border-none mt-4 w-full py-2 rounded-lg hover:bg-blue-700;
}

button {
  @apply bg-blue-600 text-white py-2 px-4 text-lg rounded-lg border-none hover:bg-blue-700;
}

button:hover {
  background-color: #0056b3;
}

/* Media Queries */
@media (max-width: 768px) {
  .favorite-recipes {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .favorite-recipes {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 2rem;
  }
}
</style>
