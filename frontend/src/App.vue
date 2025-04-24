<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
    <!-- Navbar Component -->
    <NavbarHome />
    
    <div id="app" >
      <router-view></router-view>
    </div>
    
    <FooterPage />
  </div>
</template>

<script setup>
import NavbarHome from './components/NavbarHome.vue';
import FooterPage from './components/FooterPage.vue';
import { onMounted } from 'vue';

// Función para verificar el tema preferido del sistema
const checkDarkMode = () => {
  if (localStorage.theme === 'dark' || 
      (!('theme' in localStorage) && 
       window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

onMounted(() => {
  checkDarkMode();
});
</script>

<style>
/* Transición suave para el cambio de tema */
html {
  transition: background-color 0.3s, color 0.3s;
}
</style>