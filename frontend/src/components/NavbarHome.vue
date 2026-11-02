<template>
  <nav class="bg-gradient-to-r from-amber-50 to-amber-100 shadow-md sticky top-0 z-50 border-b border-amber-200">
    <div class="max-w-7xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14 sm:h-16 gap-2">
        <router-link to="/" class="flex items-center min-w-0 group">
          <div class="p-1 sm:p-1.5 rounded-lg bg-amber-100 group-hover:bg-amber-200 transition duration-300 shrink-0">
            <img src="@/assets/logo.png" alt="Logo" class="h-7 w-7 sm:h-8 sm:w-8" />
          </div>
          <span class="ml-2 sm:ml-3 text-lg sm:text-2xl font-bold text-amber-800 font-serif tracking-tight truncate">
            <span class="xs:hidden">Sabores</span>
            <span class="hidden xs:inline">Sabores España</span>
          </span>
        </router-link>

        <div class="flex items-center gap-1 sm:gap-2 shrink-0">
          <button
            type="button"
            class="inline-flex items-center justify-center h-10 w-10 rounded-full text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition"
            :title="isDark ? 'Modo día' : 'Modo noche'"
            :aria-label="isDark ? 'Activar modo día' : 'Activar modo noche'"
            @click="toggleTheme"
          >
            <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <div class="hidden lg:flex lg:items-center lg:space-x-1">
            <router-link
              v-for="item in visibleNavItems"
              :key="item.to"
              :to="item.to"
              class="px-3 xl:px-4 py-2.5 rounded-lg text-sm font-medium text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition duration-300 flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
              </svg>
              <span>{{ item.text }}</span>
            </router-link>

            <template v-if="loggedIn">
              <button
                type="button"
                class="ml-2 px-4 py-2.5 rounded-lg text-sm font-medium text-red-600 hover:bg-red-100 transition duration-300 flex items-center"
                @click="logout"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span>Cerrar sesión</span>
              </button>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="ml-2 px-4 py-2.5 rounded-lg text-sm font-medium text-amber-800 hover:bg-amber-200 transition duration-300"
              >
                Iniciar sesión
              </router-link>
              <router-link
                to="/register"
                class="px-4 py-2.5 rounded-lg text-sm font-medium text-white bg-amber-700 hover:bg-amber-800 transition duration-300"
              >
                Registrarse
              </router-link>
            </template>
          </div>

          <button
            type="button"
            class="lg:hidden inline-flex items-center justify-center h-10 w-10 rounded-md text-amber-700 hover:text-amber-900 hover:bg-amber-200 focus:outline-none transition"
            @click="toggleNavbar"
          >
            <span class="sr-only">Menú principal</span>
            <svg v-if="!navbarOpen" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-1"
    >
      <div v-show="navbarOpen" class="lg:hidden bg-amber-50 shadow-xl border-t border-amber-200 max-h-[calc(100vh-3.5rem)] overflow-y-auto">
        <div class="px-3 pt-2 pb-4 space-y-1">
          <router-link
            v-for="item in visibleNavItems"
            :key="'m-' + item.to"
            :to="item.to"
            class="block px-3 py-3.5 rounded-lg text-base font-medium text-amber-700 hover:bg-amber-200 hover:text-amber-900 transition duration-300 flex items-center"
            @click="navbarOpen = false"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
            </svg>
            <span>{{ item.text }}</span>
          </router-link>

          <template v-if="loggedIn">
            <button
              type="button"
              class="w-full text-left block px-3 py-3.5 rounded-lg text-base font-medium text-red-600 hover:bg-red-100 transition duration-300 flex items-center"
              @click="logout"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Cerrar sesión
            </button>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="block px-3 py-3.5 rounded-lg text-base font-medium text-amber-800 hover:bg-amber-200"
              @click="navbarOpen = false"
            >
              Iniciar sesión
            </router-link>
            <router-link
              to="/register"
              class="block px-3 py-3.5 rounded-lg text-base font-medium text-white bg-amber-700 hover:bg-amber-800 text-center"
              @click="navbarOpen = false"
            >
              Registrarse
            </router-link>
          </template>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { isTokenValid, logoutRequest } from '../api'
import { useTheme } from '../utils/theme'

const router = useRouter()
const route = useRoute()
const navbarOpen = ref(false)
const { isDark, toggleTheme } = useTheme()

const loggedIn = computed(() => isTokenValid(localStorage.getItem('userToken')))

watch(
  () => route.fullPath,
  () => {
    navbarOpen.value = false
  }
)

const publicItems = [
  {
    to: '/',
    text: 'Recetario',
    iconPath:
      'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
  },
]

const authItems = [
  {
    to: '/home',
    text: 'Favoritos',
    iconPath:
      'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z',
  },
  {
    to: '/create',
    text: 'Crear receta',
    iconPath: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
  },
  {
    to: '/recipes_personal',
    text: 'Mis recetas',
    iconPath:
      'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
  },
  {
    to: '/profile',
    text: 'Ajustes',
    iconPath:
      'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
  },
]

const visibleNavItems = computed(() =>
  loggedIn.value ? [...publicItems, ...authItems] : publicItems
)

const toggleNavbar = () => {
  navbarOpen.value = !navbarOpen.value
}

const logout = async () => {
  navbarOpen.value = false
  await logoutRequest()
  router.push('/login')
}
</script>

<style scoped>
.router-link-exact-active {
  @apply bg-amber-200 text-amber-900 font-semibold;
}
</style>
