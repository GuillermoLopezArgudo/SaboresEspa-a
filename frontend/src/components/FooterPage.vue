<template>
  <footer class="bg-amber-800 text-amber-100 py-3 px-4 text-sm dark:bg-gray-800 dark:text-gray-200">
    <div class="container mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
      <div class="flex items-center">
        <span>© 2025 Recetario Español</span>
      </div>
      <div class="flex flex-wrap justify-center gap-x-4 gap-y-1">
        <a href="/" class="hover:text-amber-300 dark:hover:text-amber-400">Recetas</a>
        <a href="/sobre-nosotros" class="hover:text-amber-300 dark:hover:text-amber-400">Sobre Nosotros</a>
        <a href="/contacto" class="hover:text-amber-300 dark:hover:text-amber-400">Contacto</a>
      </div>
    </div>
  </footer>
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
footer a {
  position: relative;
}

footer a:hover:after {
  content: '';
  position: absolute;
  width: 100%;
  height: 1px;
  bottom: -1px;
  left: 0;
  background-color: #f59e0b;
}
</style>