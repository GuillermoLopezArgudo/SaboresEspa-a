<template>
  <nav class="site-nav sticky top-0 z-50 border-b border-amber-200/80 bg-amber-50/90 backdrop-blur-md shadow-sm">
    <div class="max-w-7xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14 sm:h-16 gap-3">
        <router-link to="/" class="flex items-center min-w-0 group shrink-0" @click="closeMenus">
          <div class="p-1 sm:p-1.5 rounded-xl bg-amber-100 group-hover:bg-amber-200 transition shrink-0 ring-1 ring-amber-200/80">
            <img src="@/assets/logo.png" alt="Logo" class="h-7 w-7 sm:h-8 sm:w-8" />
          </div>
          <div class="ml-2 sm:ml-3 min-w-0">
            <p class="text-base sm:text-xl font-bold text-amber-900 font-serif tracking-tight truncate leading-tight">
              <span class="xs:hidden">Sabores</span>
              <span class="hidden xs:inline">Sabores España</span>
            </p>
            <p class="nav-tagline hidden sm:block text-[10px] uppercase tracking-[0.16em] text-amber-700/70 font-semibold">
              Cocina para compartir
            </p>
          </div>
        </router-link>

        <!-- Desktop: links principales -->
        <div class="hidden lg:flex items-center gap-1 flex-1 justify-center min-w-0 px-2">
          <router-link
            v-for="item in primaryNav"
            :key="item.to"
            :to="item.to"
            class="nav-pill"
            :class="{ 'nav-pill-active': isActive(item.to) }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
            </svg>
            <span>{{ item.text }}</span>
          </router-link>
        </div>

        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
          <button
            type="button"
            class="nav-icon-btn inline-flex items-center justify-center h-10 w-10 rounded-full text-amber-800 hover:bg-amber-200/80 transition"
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

          <!-- Desktop auth -->
          <template v-if="loggedIn">
            <router-link
              to="/create"
              class="hidden lg:inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-amber-800 hover:bg-amber-900 text-white text-sm font-semibold shadow-sm transition"
            >
              <span aria-hidden="true">+</span>
              Crear
            </router-link>

            <div class="relative hidden lg:block" data-user-menu>
              <button
                type="button"
                class="account-trigger inline-flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full border border-amber-200 bg-white hover:bg-amber-50 text-amber-900 text-sm font-medium transition"
                :aria-expanded="userMenuOpen"
                @click.stop="userMenuOpen = !userMenuOpen"
              >
                <span class="h-7 w-7 rounded-full bg-amber-800 text-amber-50 text-xs font-bold flex items-center justify-center">
                  {{ userInitial }}
                </span>
                <span class="max-w-[7rem] truncate">Cuenta</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-600 transition" :class="{ 'rotate-180': userMenuOpen }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <transition
                enter-active-class="transition ease-out duration-150"
                enter-from-class="opacity-0 translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-100"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 translate-y-1"
              >
                <div
                  v-show="userMenuOpen"
                  class="account-menu absolute right-0 mt-2 w-52 rounded-2xl border border-amber-200 bg-white shadow-xl shadow-amber-900/10 overflow-hidden z-50"
                >
                  <div class="account-menu-head px-4 py-3 border-b border-amber-100 bg-amber-50/80">
                    <p class="text-xs font-semibold uppercase tracking-wide text-amber-700/70">Tu espacio</p>
                    <p class="text-sm font-semibold text-amber-950 truncate">{{ userLabel }}</p>
                  </div>
                  <router-link
                    v-for="item in accountNav"
                    :key="item.to"
                    :to="item.to"
                    class="account-menu-link flex items-center gap-2.5 px-4 py-2.5 text-sm text-amber-900 hover:bg-amber-50 transition"
                    @click="userMenuOpen = false"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
                    </svg>
                    {{ item.text }}
                  </router-link>
                  <button
                    type="button"
                    class="account-logout w-full flex items-center gap-2.5 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 border-t border-amber-100 transition"
                    @click="logout"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Cerrar sesión
                  </button>
                </div>
              </transition>
            </div>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="hidden lg:inline-flex px-3.5 py-2 rounded-full text-sm font-medium text-amber-900 hover:bg-amber-200/70 transition"
            >
              Entrar
            </router-link>
            <router-link
              to="/register"
              class="hidden lg:inline-flex px-3.5 py-2 rounded-full text-sm font-semibold text-white bg-amber-800 hover:bg-amber-900 transition"
            >
              Registro
            </router-link>
          </template>

          <button
            type="button"
            class="nav-icon-btn lg:hidden inline-flex items-center justify-center h-10 w-10 rounded-xl text-amber-800 hover:bg-amber-200/80 transition"
            :aria-expanded="navbarOpen"
            aria-controls="mobile-nav"
            @click="toggleNavbar"
          >
            <span class="sr-only">Menú</span>
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

    <!-- Mobile drawer -->
    <Teleport to="body">
      <div v-if="navbarOpen" class="lg:hidden fixed inset-0 z-[70]">
        <div class="absolute inset-0 bg-stone-900/40 backdrop-blur-[2px]" @click="navbarOpen = false" />
        <aside
          id="mobile-nav"
          class="mobile-drawer absolute top-0 right-0 h-full w-[min(20rem,88vw)] bg-amber-50 shadow-2xl border-l border-amber-200 flex flex-col animate-drawer"
        >
          <div class="mobile-drawer-head flex items-center justify-between px-4 h-14 border-b border-amber-200">
            <p class="font-serif font-bold text-amber-950">Menú</p>
            <button
              type="button"
              class="mobile-close h-9 w-9 rounded-full border border-amber-200 bg-white text-amber-900"
              @click="navbarOpen = false"
            >
              ×
            </button>
          </div>

          <div class="flex-1 overflow-y-auto p-3 space-y-1">
            <p class="px-3 pt-2 pb-1 text-[11px] font-semibold uppercase tracking-wide text-amber-700/70">Explorar</p>
            <router-link
              v-for="item in mobileExplore"
              :key="'m-' + item.to"
              :to="item.to"
              class="mobile-link"
              :class="{ 'mobile-link-active': isActive(item.to) }"
              @click="navbarOpen = false"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
              </svg>
              {{ item.text }}
            </router-link>

            <template v-if="loggedIn">
              <p class="px-3 pt-4 pb-1 text-[11px] font-semibold uppercase tracking-wide text-amber-700/70">Tu cuenta</p>
              <router-link
                v-for="item in accountNav"
                :key="'ma-' + item.to"
                :to="item.to"
                class="mobile-link"
                :class="{ 'mobile-link-active': isActive(item.to) }"
                @click="navbarOpen = false"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.iconPath" />
                </svg>
                {{ item.text }}
              </router-link>
            </template>
          </div>

          <div class="p-4 border-t border-amber-200 space-y-2">
            <template v-if="loggedIn">
              <button
                type="button"
                class="w-full py-3 rounded-xl border border-red-200 text-red-700 font-semibold text-sm hover:bg-red-50 transition"
                @click="logout"
              >
                Cerrar sesión
              </button>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="block w-full text-center py-3 rounded-xl border border-amber-300 text-amber-950 font-semibold text-sm"
                @click="navbarOpen = false"
              >
                Iniciar sesión
              </router-link>
              <router-link
                to="/register"
                class="block w-full text-center py-3 rounded-xl bg-amber-800 text-white font-semibold text-sm"
                @click="navbarOpen = false"
              >
                Crear cuenta
              </router-link>
            </template>
          </div>
        </aside>
      </div>
    </Teleport>
  </nav>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { logoutRequest } from '../api'
import { useAuth } from '../utils/auth'
import { useTheme } from '../utils/theme'

const router = useRouter()
const route = useRoute()
const navbarOpen = ref(false)
const userMenuOpen = ref(false)
const { isDark, toggleTheme } = useTheme()
const { loggedIn, userName: userLabel } = useAuth()

const userInitial = computed(() => {
  const label = String(userLabel.value || 'U').trim()
  return (label[0] || 'U').toUpperCase()
})

const icons = {
  recetario:
    'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
  favoritos:
    'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z',
  crear: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
  mis:
    'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
  ajustes:
    'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
}

const primaryNav = computed(() => {
  const items = [{ to: '/', text: 'Recetario', iconPath: icons.recetario }]
  if (loggedIn.value) {
    items.push(
      { to: '/home', text: 'Favoritos', iconPath: icons.favoritos },
      { to: '/recipes_personal', text: 'Mis recetas', iconPath: icons.mis }
    )
  }
  return items
})

const accountNav = [
  { to: '/create', text: 'Crear receta', iconPath: icons.crear },
  { to: '/profile', text: 'Ajustes', iconPath: icons.ajustes },
]

const mobileExplore = computed(() => primaryNav.value)

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path === path || route.path.startsWith(path + '/')
}

function closeMenus() {
  navbarOpen.value = false
  userMenuOpen.value = false
}

function toggleNavbar() {
  userMenuOpen.value = false
  navbarOpen.value = !navbarOpen.value
}

function onDocPointer(e) {
  if (!userMenuOpen.value) return
  const root = document.querySelector('[data-user-menu]')
  if (root && !root.contains(e.target)) userMenuOpen.value = false
}

watch(
  () => route.fullPath,
  () => closeMenus()
)

watch(navbarOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

onMounted(() => {
  document.addEventListener('pointerdown', onDocPointer, true)
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', onDocPointer, true)
  document.body.style.overflow = ''
})

const logout = async () => {
  closeMenus()
  await logoutRequest()
  router.push('/login')
}
</script>

<style scoped>
.nav-pill {
  @apply inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full text-sm font-medium text-amber-800 hover:bg-amber-200/70 transition whitespace-nowrap;
}
.nav-pill-active {
  @apply bg-amber-800 text-white hover:bg-amber-900 shadow-sm;
}
.mobile-link {
  @apply flex items-center gap-3 px-3 py-3 rounded-xl text-base font-medium text-amber-900 hover:bg-amber-100 transition;
}
.mobile-link-active {
  @apply bg-amber-800 text-white hover:bg-amber-800;
}
@keyframes drawer-in {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
.animate-drawer {
  animation: drawer-in 0.2s ease-out;
}

/* Modo noche: estilos propios (el @apply no hereda overrides globales) */
:global(html.dark) .site-nav {
  background-color: rgb(63 50 40 / 0.96) !important;
  border-color: #8a735c !important;
  box-shadow: 0 1px 0 rgb(0 0 0 / 0.25);
}
:global(html.dark) .nav-tagline {
  color: rgb(251 191 36 / 0.65) !important;
}
:global(html.dark) .nav-pill {
  color: #fde68a !important;
}
:global(html.dark) .nav-pill:hover {
  background-color: rgb(146 64 14 / 0.35) !important;
  color: #fffbeb !important;
}
:global(html.dark) .nav-pill-active {
  background-color: #d97706 !important;
  color: #2b211a !important;
}
:global(html.dark) .nav-pill-active:hover {
  background-color: #f59e0b !important;
  color: #2b211a !important;
}
:global(html.dark) .nav-icon-btn {
  color: #fde68a !important;
}
:global(html.dark) .nav-icon-btn:hover {
  background-color: rgb(146 64 14 / 0.4) !important;
  color: #fffbeb !important;
}
:global(html.dark) .account-trigger {
  background-color: #3d3128 !important;
  border-color: #6b5342 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .account-trigger:hover {
  background-color: #4a3a2f !important;
}
:global(html.dark) .account-menu {
  background-color: #3d3128 !important;
  border-color: #6b5342 !important;
}
:global(html.dark) .account-menu-head {
  background-color: #2b211a !important;
  border-color: #5a4638 !important;
}
:global(html.dark) .account-menu-link {
  color: #fef3c7 !important;
}
:global(html.dark) .account-menu-link:hover {
  background-color: #4a3a2f !important;
}
:global(html.dark) .account-logout {
  color: #fca5a5 !important;
  border-color: #5a4638 !important;
}
:global(html.dark) .account-logout:hover {
  background-color: rgb(127 29 29 / 0.35) !important;
}
:global(html.dark) .mobile-drawer {
  background-color: #2b211a !important;
  border-color: #5a4638 !important;
}
:global(html.dark) .mobile-drawer-head {
  border-color: #5a4638 !important;
}
:global(html.dark) .mobile-close {
  background-color: #3d3128 !important;
  border-color: #6b5342 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .mobile-link {
  color: #fde68a !important;
}
:global(html.dark) .mobile-link:hover {
  background-color: #4a3a2f !important;
  color: #fffbeb !important;
}
:global(html.dark) .mobile-link-active {
  background-color: #d97706 !important;
  color: #2b211a !important;
}
:global(html.dark) .mobile-link-active:hover {
  background-color: #f59e0b !important;
  color: #2b211a !important;
}
</style>
