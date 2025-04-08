<template>
  <!-- Navbar con sombra suave y fondo cálido -->
  <nav class="bg-gradient-to-r from-amber-50 to-amber-100 shadow-md sticky top-0 z-50 border-b border-amber-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo con imagen y texto -->
        <router-link to="/home" class="flex items-center group">
          <div class="p-1.5 rounded-lg bg-amber-100 group-hover:bg-amber-200 transition duration-300">
            <img src="@/assets/logo.png" alt="Logo" class="h-8 w-8" />
          </div>
          <span class="ml-3 text-2xl font-bold text-amber-800 font-serif tracking-tight">Sabores España</span>
        </router-link>

        <!-- Mobile menu button -->
        <div class="flex lg:hidden">
          <button @click="toggleNavbar" class="inline-flex items-center justify-center p-2 rounded-md text-amber-700 hover:text-amber-900 hover:bg-amber-200 focus:outline-none transition duration-300">
            <span class="sr-only">Menú principal</span>
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden lg:flex lg:items-center lg:space-x-1">
          <router-link 
            v-for="item in navItems" 
            :key="item.to"
            :to="item.to"
            class="px-4 py-2.5 rounded-lg text-sm font-medium text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition duration-300 flex items-center group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
            </svg>
            <span>{{ item.text }}</span>
          </router-link>
          
          <button @click="logout" class="ml-2 px-4 py-2.5 rounded-lg text-sm font-medium text-red-600 hover:bg-red-100 transition duration-300 flex items-center group">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Cerrar Sesión</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-show="navbarOpen" class="lg:hidden bg-amber-50 shadow-xl border-t border-amber-200">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <router-link 
            v-for="item in navItems" 
            :key="item.to"
            :to="item.to"
            class="block px-3 py-3 rounded-lg text-base font-medium text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition duration-300 flex items-center"
            @click="navbarOpen = false"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
            </svg>
            <span>{{ item.text }}</span>
          </router-link>
          
          <button @click="logout" class="w-full text-left block px-3 py-3 rounded-lg text-base font-medium text-red-600 hover:bg-red-100 transition duration-300 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Cerrar Sesión
          </button>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const navbarOpen = ref(false);

const navItems = [
  {
    to: '/create',
    text: 'Crear Recetas',
    iconPath: 'M12 6v6m0 0v6m0-6h6m-6 0H6'
  },
  {
    to: '/recipes_personal',
    text: 'Mis Recetas',
    iconPath: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6'
  },
  {
    to: '/',
    text: 'Recetario',
    iconPath: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'
  },
  {
    to: '/profile',
    text: 'Ajustes',
    iconPath: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
  }
];

const toggleNavbar = () => {
  navbarOpen.value = !navbarOpen.value;
};

const logout = () => {
  localStorage.clear();
  router.push('/login');
};
</script>

<style scoped>
.router-link-exact-active {
  @apply bg-amber-200 text-amber-900 font-semibold;
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

.router-link-active:first-child:hover img {
  animation: pulse 1s infinite;
}
</style>