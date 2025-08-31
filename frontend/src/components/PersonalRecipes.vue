<template>
  <div class="min-h-screen bg-amber-50 dark:bg-gray-900">

    <!-- Encabezado -->
    <div class="bg-amber-900 py-8 px-4 sm:px-6 lg:px-8 relative dark:bg-gray-800">
      <div class="absolute inset-0 bg-black opacity-20"></div>
      <div class="relative max-w-7xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-white font-serif mb-2 dark:text-white">
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-amber-300 to-orange-300">Tus Creaciones Culinarias</span>
        </h1>
        <p class="text-xl text-amber-100 dark:text-gray-400">Todas las recetas que has compartido con la comunidad</p>
      </div>
    </div>

    <!-- Main content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <ListRecipes :greeting="'personal'" />
    </main>

  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import ListRecipes from './ListRecipes.vue';

const darkMode = ref(false);

onMounted(() => {
  const savedMode = localStorage.getItem('darkMode');
  if (savedMode !== null) {
    darkMode.value = JSON.parse(savedMode);
    applyDarkMode();
  }

});

function applyDarkMode() {
  if (darkMode.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}
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