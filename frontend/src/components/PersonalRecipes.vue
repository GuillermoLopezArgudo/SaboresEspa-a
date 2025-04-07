<template>
  <div class="min-h-screen bg-amber-50">
    <!-- Navbar Component -->
    <NavbarHome />

    <!-- Encabezado -->
    <div class="max-w-7xl mx-auto text-center mb-8 pt-8 px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-3">
        Tus Creaciones Culinarias
      </h1>
      <p class="text-lg text-amber-700">Todas las recetas que has compartido con la comunidad</p>
    </div>

    <!-- Botón de regreso -->
    <div class="max-w-7xl mx-auto mb-6 px-4 sm:px-6 lg:px-8">
      <router-link to="/home"
        class="inline-flex items-center px-5 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg transition duration-300 shadow-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd" />
        </svg>
        Volver al inicio
      </router-link>
    </div>

    <!-- Main content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <ListRecipes :greeting="'personal'" />
    </main>
  </div>
</template>

<script setup>
import ListRecipes from './ListRecipes.vue';
import NavbarHome from './NavbarHome.vue';
</script>

<style scoped>
/* Estilos opcionales para transiciones suaves */
.router-link-active {
  @apply font-semibold;
}

/* Animación para el logo */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.router-link-active:first-child:hover svg {
  animation: pulse 1s infinite;
}
</style>