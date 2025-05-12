<template>
  <!-- Navbar con soporte para modo oscuro -->
  <nav
    class="bg-gradient-to-r from-amber-50 to-amber-100 dark:from-gray-800 dark:to-gray-900 shadow-sm sm:shadow-md sticky top-0 z-50 border-b border-amber-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20 lg:h-24">
        <!-- Logo con imagen y texto -->
        <router-link to="/" class="flex items-center group">
          <div
            class="p-1 rounded-md sm:p-1.5 sm:rounded-lg bg-amber-100 dark:bg-gray-700 group-hover:bg-amber-200 dark:group-hover:bg-gray-600 ">
            <img src="@/assets/logo.png" alt="Logo" class="h-14 w-14 sm:h-16 sm:w-16 md:h-18 md:w-18 lg:h-20 lg:w-20" />
          </div>
          <span
            class="ml-3 mr-4 sm:ml-3 sm:mr-2 text-xl sm:text-2xl lg:text-3xl font-bold text-amber-800 dark:text-amber-200 font-serif tracking-tight">
            Sabores España
          </span>
        </router-link>

        <!-- Botón de menú móvil y toggle de modo oscuro -->
        <div class="flex items-center space-x-2 lg:hidden">

          <!-- Botón de menú móvil -->
          <button @click="toggleNavbar" aria-label="Menú principal" ref="NavbarRef"
            class="inline-flex items-center justify-center p-1.5 sm:p-2 rounded-md text-amber-700 dark:text-amber-200 hover:text-amber-900 dark:hover:text-amber-100 hover:bg-amber-200 dark:hover:bg-gray-700 focus:outline-none"
            :aria-expanded="navbarOpen">
            <svg class="h-5 w-5 sm:h-6 sm:w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <!-- Toggle de modo oscuro para móvil -->
          <button @click="toggleDarkMode"
            class="p-1.5 rounded-full text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 ">
            <span v-if="darkMode">🌞</span>
            <span v-else>🌙</span>
          </button>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden lg:flex lg:items-center lg:space-x-4 xl:space-x-6">

          <!-- Elementos de navegación -->
          <template v-if="isLoggedIn">
            <router-link v-for="item in navItems" :key="item.to" :to="item.to"
              class="px-3 py-2 rounded-lg text-sm font-medium text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 hover:text-amber-900 dark:hover:text-amber-100 flex items-center group"
              active-class="bg-amber-200 dark:bg-gray-700 text-amber-900 dark:text-amber-100 font-semibold">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1.5" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
              </svg>
              <span class="whitespace-nowrap">{{ item.text }}</span>
            </router-link>

            <button @click="logout"
              class="ml-1 px-3 py-2 rounded-lg text-sm font-medium text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 hover:text-amber-900 dark:hover:text-amber-100 flex items-center group">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1.5" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="whitespace-nowrap">Cerrar Sesión</span>
            </button>
            <!-- Toggle de modo oscuro para desktop -->
            <button @click="toggleDarkMode"
              class="p-1.5 rounded-full text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 ">
              <span v-if="darkMode">🌞</span>
              <span v-else>🌙</span>
            </button>
          </template>
          <template v-else>
            <router-link to="/login"
              class="px-2.5 py-1.5 text-sm font-medium text-amber-700 dark:text-amber-200 hover:text-amber-900 dark:hover:text-amber-100 flex items-center whitespace-nowrap"
              active-class="text-amber-900 dark:text-amber-100 font-semibold">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path fill-rule="evenodd"
                  d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z"
                  clip-rule="evenodd" />
              </svg>
              Iniciar Sesión
            </router-link>
            <router-link to="/register"
              class="px-3 py-2 rounded-lg text-sm font-medium bg-amber-500 dark:bg-amber-600 text-white hover:bg-amber-600 dark:hover:bg-amber-700 flex items-center whitespace-nowrap">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path fill-rule="evenodd"
                  d="M9 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H7Zm8-1a1 1 0 0 1 1-1h1v-1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0v-1h-1a1 1 0 0 1-1-1Z"
                  clip-rule="evenodd" />
              </svg>
              Registrarse
            </router-link>
            <button @click="toggleDarkMode"
              class="p-1.5 rounded-full text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 ">
              <span v-if="darkMode">🌞</span>
              <span v-else>🌙</span>
            </button>
          </template>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <transition enter-active-class="transition ease-out duration-200 transform"
      enter-from-class="opacity-0 -translate-y-4" enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150 transform" leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-4">
      <div v-show="navbarOpen"
        class="absolute top-20 left-0 w-full bg-amber-50 dark:bg-gray-800 shadow-xl border-t border-amber-200 dark:border-gray-700 z-40">
        <div class="px-2 pt-1 pb-2 space-y-1 sm:px-3">
          <div v-if="isLoggedIn">
            <router-link v-for="item in navItems" :key="item.to" :to="item.to"
              class="block px-3 py-2.5 rounded-lg text-base font-medium text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 hover:text-amber-900 dark:hover:text-amber-100 flex items-center"
              @click="navbarOpen = false"
              active-class="bg-amber-200 dark:bg-gray-700 text-amber-900 dark:text-amber-100 font-semibold">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
              </svg>
              <span>{{ item.text }}</span>
            </router-link>

            <button @click="logout"
              class="w-full text-left block px-3 py-2.5 rounded-lg text-base font-medium text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 hover:text-amber-900 dark:hover:text-amber-100 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Cerrar Sesión
            </button>
          </div>
          <div v-else class="space-y-1">
            <router-link to="/login"
              class="block px-3 py-2.5 rounded-lg text-base font-medium text-amber-700 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-gray-700 hover:text-amber-900 dark:hover:text-amber-100 flex items-center"
              @click="navbarOpen = false">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path fill-rule="evenodd"
                  d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z"
                  clip-rule="evenodd" />
              </svg>
              Iniciar Sesión
            </router-link>
            <router-link to="/register"
              class="block px-3 py-2.5 rounded-lg text-base font-medium bg-amber-500 dark:bg-amber-600 text-white hover:bg-amber-600 dark:hover:bg-amber-700 flex items-center justify-center"
              @click="navbarOpen = false">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path fill-rule="evenodd"
                  d="M9 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H7Zm8-1a1 1 0 0 1 1-1h1v-1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0v-1h-1a1 1 0 0 1-1-1Z"
                  clip-rule="evenodd" />
              </svg>
              Registrarse
            </router-link>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const navbarOpen = ref(false);
const isLoggedIn = ref(!!localStorage.getItem("userToken"));
const NavbarRef = ref(null);
const darkMode = ref(false);

// Función para alternar el modo oscuro
const toggleDarkMode = () => {
  darkMode.value = !darkMode.value;
  if (darkMode.value) {
    document.documentElement.classList.add('dark');
    localStorage.theme = 'dark';
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.theme = 'light';
  }
};

// Verificar el tema al cargar
const checkDarkMode = () => {
  if (localStorage.theme === 'dark' ||
    (!('theme' in localStorage) &&
      window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
    darkMode.value = true;
  } else {
    document.documentElement.classList.remove('dark');
    darkMode.value = false;
  }
};

// Función para comprobar la autenticación
const checkAuth = () => {
  isLoggedIn.value = !!localStorage.getItem('userToken');
};

// Manejar los cambios en localStorage
const handleStorageChange = (event) => {
  if (event.key === 'userToken') {
    checkAuth();
  }
};

// Detectar cambios en userToken usando watch
watch(
  () => localStorage.getItem('userToken'),
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      checkAuth();
    }
  }
);

onMounted(() => {
  checkDarkMode();
  window.addEventListener('storage', handleStorageChange);

  const authCheckInterval = setInterval(checkAuth, 1000);

  onUnmounted(() => {
    clearInterval(authCheckInterval);
    window.removeEventListener('storage', handleStorageChange);
  });
});

// Lista de elementos de navegación
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
    text: 'Perfil',
    iconPath: 'M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z M4.5 20.25a8.25 8.25 0 0115 0 M9 2l1.5-2 1.5 2h-3z M9 3h6v1H9V3z M7.5 2.25l1.5-1.25h4.5l1.5 1.25z'
  },
  {
    to:'/ingredientList',
    text: 'Ingredientes',
    iconPath: "M5.617 2.076a1 1 0 0 1 1.09.217L8 3.586l1.293-1.293a1 1 0 0 1 1.414 0L12 3.586l1.293-1.293a1 1 0 0 1 1.414 0L16 3.586l1.293-1.293A1 1 0 0 1 19 3v18a1 1 0 0 1-1.707.707L16 20.414l-1.293 1.293a1 1 0 0 1-1.414 0L12 20.414l-1.293 1.293a1 1 0 0 1-1.414 0L8 20.414l-1.293 1.293A1 1 0 0 1 5 21V3a1 1 0 0 1 .617-.924ZM9 7a1 1 0 0 0 0 2h6a1 1 0 1 0 0-2H9Zm0 4a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2H9Zm0 4a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2H9Z"

  }
];

// Función para alternar la visibilidad del navbar
const toggleNavbar = () => {
  navbarOpen.value = !navbarOpen.value;
};

// Función de logout
const logout = async () => {
  try {
    // Limpiar datos de autenticación
    localStorage.removeItem('userToken');
    navbarOpen.value = false;

    // Forzar actualización inmediata
    isLoggedIn.value = false;

    // Redirigir al login
    await router.push('/login');
  } catch (error) {
    console.error('Error durante logout:', error);
  }
};

// Función para manejar el clic fuera del navbar
const handleClickOutside = (event) => {
  if (NavbarRef.value && !NavbarRef.value.contains(event.target)) {
    navbarOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Mejoras de animación */
.router-link-active:first-child:hover img {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
}

/* Mejoras para mobile */
@media (max-width: 1023px) {
  nav {
    backdrop-filter: blur(5px);
  }

  .router-link-exact-active {
    @apply bg-amber-200 dark:bg-gray-700;
  }
}

/* Mejor contraste para accesibilidad */
.text-amber-700 {
  color: #b45309;
}

.dark .text-amber-200 {
  color: #fde68a;
}

.hover\:text-amber-900:hover {
  color: #78350f;
}

.dark .hover\:text-amber-100:hover {
  color: #fef3c7;
}
</style>