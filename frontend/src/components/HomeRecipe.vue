<template>
  <div class="min-h-screen bg-amber-50">

          <!-- Header con imagen de fondo -->
          <div class="bg-amber-900 py-8 px-4 sm:px-6 lg:px-8 relative">
        <div class="absolute inset-0 bg-black opacity-20"></div>
        <div class="relative max-w-7xl mx-auto text-center">
          <h1 class="text-4xl md:text-5xl font-bold text-white font-serif mb-2">
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-amber-300 to-orange-300">Bienvenido a tu Recetario</span>
          </h1>
          <p class="text-xl text-amber-100">Descubre, crea y comparte tus recetas favoritas</p>
        </div>
      </div>
    <!-- Navbar mejorado -->
    <NavbarHome/>


    <!-- Main content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <ListRecipes :greeting="'favs'"/>
    </main>
  </div>
</template>

<script setup>

import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ListRecipes from './ListRecipes.vue';
import NavbarHome from './NavbarHome.vue';

const userToken = ref(localStorage.getItem("userToken"));
const router = useRouter();


// Redirigir al login si no hay token
if (userToken.value == null) {
  router.push({ name: "login" });
}


</script>

<style scoped>
/* Transición suave para el menú móvil */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Efecto para los enlaces activos */
.router-link-exact-active {
  @apply text-amber-900 font-semibold;
}

/* Animación para el logo */
@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }
}

.logo:hover {
  animation: pulse 1s infinite;
}
</style>