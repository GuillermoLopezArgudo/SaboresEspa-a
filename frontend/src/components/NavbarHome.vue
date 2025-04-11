<template>
  <!-- Navbar con sombra suave y fondo cálido -->
  <nav class="bg-gradient-to-r from-amber-50 to-amber-100 shadow-md sticky top-0 z-50 border-b border-amber-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo con imagen y texto -->
        <router-link to="/" class="flex items-center group">
          <div class="p-1.5 rounded-lg bg-amber-100 group-hover:bg-amber-200 transition duration-300">
            <img src="@/assets/logo.png" alt="Logo" class="h-8 w-8" />
          </div>
          <span class="ml-3 text-2xl font-bold text-amber-800 font-serif tracking-tight">Sabores España</span>
        </router-link>

        <!-- Mobile menu button -->
        <div class="flex lg:hidden">
          <button @click="toggleNavbar"
            class="inline-flex items-center justify-center p-2 rounded-md text-amber-700 hover:text-amber-900 hover:bg-amber-200 focus:outline-none transition duration-300">
            <span class="sr-only">Menú principal</span>
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        <!-- Desktop Navigation -->
        <div v-if="isLoggedIn">
          <div class="hidden lg:flex lg:items-center lg:space-x-1">
            <router-link v-for="item in navItems" :key="item.to" :to="item.to"
              class="px-4 py-2.5 rounded-lg text-sm font-medium text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition duration-300 flex items-center group">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
              </svg>
              <span>{{ item.text }}</span>
            </router-link>

            <button @click="logout"
              class="ml-2 px-4 py-2.5 rounded-lg text-sm font-medium text-red-600 hover:bg-red-100 transition duration-300 flex items-center group">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
        <div v-else>
          <div class="hidden lg:flex lg:items-center lg:space-x-8">
            <router-link to="/"
              class="px-3 py-2 text-sm font-medium text-amber-700 hover:text-amber-900 transition duration-300 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Home
            </router-link>
            <router-link @click="closeSession" to="/login"
              class="px-3 py-2 text-sm font-medium text-amber-700 hover:text-amber-900 transition duration-300 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path fill-rule="evenodd" d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z" clip-rule="evenodd"/>
              </svg>
              Loguear
            </router-link>
            <router-link @click="closeSession" to="/register"
              class="px-3 py-2 text-sm font-medium text-amber-700 hover:text-amber-900 transition duration-300 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path fill-rule="evenodd" d="M9 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H7Zm8-1a1 1 0 0 1 1-1h1v-1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0v-1h-1a1 1 0 0 1-1-1Z" clip-rule="evenodd"/>
              </svg>
              Registrar
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100" leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">

      <div v-show="navbarOpen" class="lg:hidden bg-amber-50 shadow-xl border-t border-amber-200">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <router-link v-for="item in navItems" :key="item.to" :to="item.to"
            class="block px-3 py-3 rounded-lg text-base font-medium text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition duration-300 flex items-center"
            @click="navbarOpen = false">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
            </svg>
            <span>{{ item.text }}</span>
          </router-link>

          <button @click="logout"
            class="w-full text-left block px-3 py-3 rounded-lg text-base font-medium text-red-600 hover:bg-red-100 transition duration-300 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Cerrar Sesión
          </button>
        </div>
      </div>

    </transition>
  </nav>
</template>

<script setup>
import { ref,onMounted,onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const navbarOpen = ref(false);
const isLoggedIn = ref(!!localStorage.getItem("userToken"))

const checkAuth = () => {
  isLoggedIn.value = !!localStorage.getItem('userToken');
};

const handleStorageChange = (event) => {
  if (event.key === 'userToken') {
    checkAuth();
  }
};

watch(
  () => localStorage.getItem('userToken'),
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      checkAuth();
    }
  }
);

onMounted(() => {
  window.addEventListener('storage', handleStorageChange);
  
  const authCheckInterval = setInterval(checkAuth, 1000);
  
  onUnmounted(() => {
    clearInterval(authCheckInterval);
    window.removeEventListener('storage', handleStorageChange);
  });
});


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
    to: '/home',
    text: 'Favoritos',
    iconPath: 'm12.75 20.66 6.184-7.098c2.677-2.884 2.559-6.506.754-8.705-.898-1.095-2.206-1.816-3.72-1.855-1.293-.034-2.652.43-3.963 1.442-1.315-1.012-2.678-1.476-3.973-1.442-1.515.04-2.825.76-3.724 1.855-1.806 2.201-1.915 5.823.772 8.706l6.183 7.097c.19.216.46.34.743.34a.985.985 0 0 0 .743-.34Z'
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

const logout = async () => {
  try {
    // Limpiar datos de autenticación
    localStorage.removeItem('userToken');
    
    // Forzar actualización inmediata
    isLoggedIn.value = false;
    
    // Redirigir al login
    await router.push('/login');
    
    // Recargar para limpiar completamente el estado
    window.location.reload();
  } catch (error) {
    console.error('Error durante logout:', error);
  }
};
</script>

<style scoped>
.router-link-exact-active {
  @apply bg-amber-200 text-amber-900 font-semibold;
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

.router-link-active:first-child:hover img {
  animation: pulse 1s infinite;
}
</style>