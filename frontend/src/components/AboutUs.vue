<template>
  <div class="min-h-screen bg-amber-50 dark:bg-neutral-900 text-gray-900 dark:text-neutral-200 flex items-center justify-center transition-colors duration-300">
    <div class="max-w-4xl w-full p-8">
      <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm shadow-lg dark:shadow-md rounded-2xl p-6 transition-all duration-300">
        <h1 class="text-4xl font-bold text-amber-600 dark:text-amber-400 mb-4">Sobre Nosotros</h1>
        <p class="text-gray-700 dark:text-gray-300 text-lg mb-4">
          Bienvenido a nuestra plataforma. Somos un equipo apasionado por la cocina y la tecnología,
          dedicados a compartir recetas deliciosas y crear una comunidad donde todos puedan participar.
        </p>
        <p class="text-gray-700 dark:text-gray-300 text-lg mb-4">
          Nuestro objetivo es ofrecer un espacio colaborativo donde los usuarios puedan descubrir,
          comentar y valorar recetas de todo el mundo. Creemos en la creatividad, el aprendizaje
          compartido y el amor por la comida.
        </p>
        <p class="text-gray-700 dark:text-gray-300 text-lg">
          Gracias por ser parte de esta aventura culinaria. ¡Buen provecho!
        </p>
      </div>
    </div>
  </div>
</template>
  
  
  <script setup>
  import { ref, onMounted } from 'vue';

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
  </style>
  