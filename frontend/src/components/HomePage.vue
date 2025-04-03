<template>
  <div class="bg-gray-100 min-h-screen">
    <!-- Header -->
    <h1 class="text-center mt-6 text-4xl font-bold text-orange-600 mb-8">Bienvenido a tu Recetario</h1>
    
    <!-- Navbar -->
    <nav class="bg-white shadow-lg mb-6">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <router-link to="/" class="text-3xl font-extrabold text-orange-600">Recetario</router-link>
        
        <!-- Mobile Navbar Toggle -->
        <button class="lg:hidden px-4 py-2 border-2 border-orange-600 rounded-lg" @click="toggleNavbar">
          <span class="text-orange-600">☰</span>
        </button>

        <!-- Links for large screens -->
        <div v-show="!navbarOpen" class="lg:flex lg:ml-auto space-x-8">
          <router-link to="/create" class="text-lg font-medium text-gray-700 hover:text-orange-600 transition duration-300">Crear receta</router-link>
          <router-link to="/recipes_personal" class="text-lg font-medium text-gray-700 hover:text-orange-600 transition duration-300">Mis recetas</router-link>
          <router-link to="/" class="text-lg font-medium text-gray-700 hover:text-orange-600 transition duration-300">Todas las recetas</router-link>
          <router-link to="/profile" class="text-lg font-medium text-gray-700 hover:text-orange-600 transition duration-300">Ajustes</router-link>
          <router-link @click="closeSession" to="/login" class="text-lg font-medium text-gray-700 hover:text-orange-600 transition duration-300">Cerrar sesión</router-link>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <div class="container mx-auto px-6">
      <FavoriteRecipe />
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

// Redirigir al login si no hay token
if (userToken.value == null) {
  router.push({ name: "login" });
}

// Función para cerrar sesión
function closeSession() {
  localStorage.clear();
}

// Función para manejar el toggle del navbar en pantallas pequeñas
function toggleNavbar() {
  navbarOpen.value = !navbarOpen.value;
}
</script>

<style scoped>
/* Estilos para el body */
body {
  font-family: 'Roboto', sans-serif;
}

/* Estilo de la receta favorita */
.favorite-recipes {
  @apply grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8;
}

.favorite-recipes .recipe-card {
  @apply bg-white border border-gray-300 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300;
}

.favorite-recipes .recipe-card img {
  @apply w-full h-48 object-cover rounded-t-lg;
}

.favorite-recipes .recipe-card h5 {
  @apply text-xl font-semibold text-gray-800 mt-4 px-4;
}

.favorite-recipes .recipe-card p {
  @apply text-gray-600 mt-2 px-4 pb-4;
}

.favorite-recipes .recipe-card .btn {
  @apply bg-orange-600 text-white border-none mt-4 w-full py-2 rounded-lg hover:bg-orange-700 transition duration-300;
}

button {
  @apply bg-orange-600 text-white py-2 px-6 text-lg rounded-lg border-none hover:bg-orange-700 transition duration-300;
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
    font-size: 2.5rem;
  }
}
</style>
