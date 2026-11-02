<template>
  <div>
    <PageHero
      title="Crear cuenta"
      subtitle="Únete para publicar, guardar favoritos y comentar"
    >
      <router-link
        to="/"
        class="inline-flex items-center px-4 py-2 rounded-full bg-white/15 hover:bg-white/25 text-white text-sm font-medium border border-white/20 transition"
      >
        ← Recetario
      </router-link>
    </PageHero>

    <div class="max-w-md mx-auto px-3 xs:px-4 sm:px-6 py-8 sm:py-10">
      <div class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
        <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50">
          <p class="font-serif font-bold text-amber-950 text-lg">Registro</p>
          <p class="text-sm text-amber-800/70">Solo te pedimos lo esencial</p>
        </div>

        <form class="p-4 sm:p-6 md:p-8 space-y-5" @submit.prevent="OnSubmit">
          <div
            v-if="error"
            class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800"
          >
            {{ error }}
          </div>

          <div>
            <label for="name" class="block text-sm font-medium text-amber-900 mb-1.5">
              Nombre
            </label>
            <input
              id="name"
              v-model="name"
              type="text"
              required
              autocomplete="name"
              placeholder="Tu nombre"
              class="w-full rounded-xl border border-amber-300 px-4 py-3 text-amber-950 placeholder:text-amber-700/40 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-amber-900 mb-1.5">
              Correo electrónico
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              placeholder="tucorreo@ejemplo.com"
              class="w-full rounded-xl border border-amber-300 px-4 py-3 text-amber-950 placeholder:text-amber-700/40 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-amber-900 mb-1.5">
              Contraseña
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              minlength="8"
              autocomplete="new-password"
              placeholder="Mínimo 8 caracteres"
              class="w-full rounded-xl border border-amber-300 px-4 py-3 text-amber-950 placeholder:text-amber-700/40 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-amber-900 mb-1.5">
              Confirmar contraseña
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              required
              minlength="8"
              autocomplete="new-password"
              placeholder="Repite la contraseña"
              class="w-full rounded-xl border border-amber-300 px-4 py-3 text-amber-950 placeholder:text-amber-700/40 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
          </div>

          <button
            type="submit"
            class="w-full rounded-full bg-amber-800 hover:bg-amber-900 text-white font-semibold py-3 transition"
            :disabled="submitting"
          >
            {{ submitting ? 'Creando cuenta…' : 'Crear cuenta' }}
          </button>

          <p class="text-center text-sm text-amber-800/80">
            ¿Ya tienes cuenta?
            <router-link to="/login" class="font-semibold text-amber-950 underline underline-offset-2">
              Inicia sesión
            </router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { apiUrl } from '../api'
import PageHero from './PageHero.vue'
import { setCachedProfile } from '../utils/profileCache'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const submitting = ref(false)
const router = useRouter()

function OnSubmit() {
  if (password.value !== confirmPassword.value) {
    error.value = 'Las contraseñas no coinciden'
    return
  }

  submitting.value = true
  error.value = ''
  axios
    .post(apiUrl('/register'), {
      name: name.value,
      email: email.value,
      password: password.value,
    })
    .then((response) => {
      if (response.data.userToken) {
        localStorage.setItem('userToken', response.data.userToken)
        localStorage.setItem('iduser', response.data.iduser)
        localStorage.setItem('type', response.data.type)
        localStorage.setItem('userName', response.data.name || name.value)
        setCachedProfile({
          name: response.data.name || name.value,
          email: response.data.email || email.value,
          image: response.data.image || '',
        })
        router.push({ name: 'landing' })
      } else {
        error.value = response.data.message || 'No se pudo crear la cuenta'
      }
    })
    .catch((err) => {
      error.value =
        err.response?.data?.message || 'Error en el servidor. Inténtalo más tarde.'
    })
    .finally(() => {
      submitting.value = false
    })
}
</script>
