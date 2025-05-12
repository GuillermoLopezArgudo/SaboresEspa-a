<template>
  <!-- Contenedor principal: ocupa el 100% del viewport sin scroll -->
  <div class="flex flex-col h-screen overflow-hidden bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
    <!-- Navbar (altura automática) -->
    <NavbarHome />
    
    <!-- Contenedor del contenido principal -->
    <div class="flex-1 overflow-y-auto">
      <router-view></router-view>
    </div>
    
    <!-- Footer  -->
    <FooterPage />
  </div>
</template>

<script setup>
import NavbarHome from './components/NavbarHome.vue';
import FooterPage from './components/FooterPage.vue';
import { onMounted } from 'vue';

// Configuración del tema oscuro (igual que antes)
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
/* Reset básico para html y body (opcional pero recomendado) */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

/* Transición suave para el cambio de tema */
html {
  transition: background-color 0.3s, color 0.3s;
}
</style>