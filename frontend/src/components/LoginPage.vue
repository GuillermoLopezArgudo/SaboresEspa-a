<template>
  <div>
    <PageHero
      title="Iniciar sesión"
      subtitle="Entra para guardar favoritos, valorar y compartir recetas"
    >
      <router-link to="/" class="hero-cta-ghost">
        ← Recetario
      </router-link>
    </PageHero>

    <div class="max-w-md mx-auto px-3 xs:px-4 sm:px-6 py-8 sm:py-10">
      <div class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
        <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50">
          <p class="font-serif font-bold text-amber-950 text-lg">Tu cuenta</p>
          <p class="text-sm text-amber-800/70">Usa el email con el que te registraste</p>
        </div>

        <form class="p-4 sm:p-6 md:p-8 space-y-5" @submit.prevent="OnSubmit">
          <div
            v-if="error"
            class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800"
          >
            {{ error }}
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
              autocomplete="current-password"
              placeholder="••••••••"
              class="w-full rounded-xl border border-amber-300 px-4 py-3 text-amber-950 placeholder:text-amber-700/40 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
          </div>

          <button
            type="submit"
            class="w-full rounded-full bg-amber-800 hover:bg-amber-900 text-white font-semibold py-3 transition"
            :disabled="submitting"
          >
            {{ submitting ? 'Entrando…' : 'Entrar' }}
          </button>

          <p class="text-center text-sm text-amber-800/80">
            ¿No tienes cuenta?
            <router-link to="/register" class="font-semibold text-amber-950 underline underline-offset-2">
              Regístrate
            </router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { apiUrl, setSession } from '../api'
import PageHero from './PageHero.vue'
import { setCachedProfile } from '../utils/profileCache'

const router = useRouter()
const route = useRoute()
const email = ref('')
const password = ref('')
const error = ref('')
const submitting = ref(false)

function OnSubmit() {
  submitting.value = true
  error.value = ''
  axios
    .post(apiUrl('/login'), {
      email: email.value,
      password: password.value,
    })
    .then((response) => {
      if (response.data.userToken) {
        setSession({
          userToken: response.data.userToken,
          iduser: response.data.iduser,
          type: response.data.type,
          name: response.data.name || '',
          email: response.data.email || email.value,
        })
        setCachedProfile({
          name: response.data.name || '',
          email: response.data.email || email.value,
          image: response.data.image || '',
        })
        const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : ''
        router.push(redirect || { name: 'landing' })
      } else {
        error.value = response.data.message || 'No se pudo iniciar sesión'
      }
    })
    .catch((err) => {
      error.value = err.response?.data?.message || 'Error al iniciar sesión'
    })
    .finally(() => {
      submitting.value = false
    })
}
</script>
