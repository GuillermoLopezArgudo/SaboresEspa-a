<template>
  <div>
    <PageHero title="Ajustes" subtitle="Gestiona tu perfil y preferencias de cuenta" />

    <div class="max-w-3xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-4 sm:space-y-5">
      <div
        v-if="loading && !name && !email"
        class="rounded-2xl border border-amber-100 bg-white p-8 animate-pulse space-y-4"
      >
        <div class="mx-auto h-28 w-28 rounded-full bg-amber-100" />
        <div class="h-4 bg-amber-100 rounded w-1/3 mx-auto" />
        <div class="h-10 bg-amber-50 rounded" />
        <div class="h-10 bg-amber-50 rounded" />
      </div>

      <template v-else>
        <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
          <div class="px-6 py-5 border-b border-amber-100 bg-amber-50 text-center">
            <div class="relative inline-block group">
              <img
                :src="imageUrl"
                alt="Imagen de perfil"
                class="w-28 h-28 rounded-full object-cover border-4 border-white shadow-md"
              />
              <label
                for="imageRecipe"
                class="absolute bottom-1 right-1 bg-amber-800 text-white p-2 rounded-full cursor-pointer hover:bg-amber-900 transition shadow"
                title="Cambiar foto"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <input id="imageRecipe" type="file" class="hidden" accept="image/*" @change="handleImageChange" />
              </label>
            </div>
            <p class="mt-3 font-serif text-xl font-bold text-amber-950">{{ name || 'Tu perfil' }}</p>
            <p class="text-sm text-amber-800/70">{{ email }}</p>
          </div>

          <div class="p-6 space-y-4">
            <!-- Nombre -->
            <div class="rounded-xl border border-amber-100 bg-amber-50/50 p-4">
              <div v-if="!boolChangeName" class="space-y-3">
                <h3 class="text-sm font-semibold text-amber-900">Nombre</h3>
                <input
                  v-model="name"
                  type="text"
                  class="w-full rounded-xl border border-amber-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                />
                <div class="flex gap-2">
                  <button
                    type="button"
                    class="flex-1 rounded-full bg-amber-800 hover:bg-amber-900 text-white py-2 text-sm font-semibold"
                    @click="changeName"
                  >
                    Guardar
                  </button>
                  <button
                    type="button"
                    class="flex-1 rounded-full border border-amber-300 text-amber-900 py-2 text-sm font-medium hover:bg-white"
                    @click="handleNameChange"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
              <div v-else class="flex items-center justify-between gap-3">
                <div>
                  <h3 class="text-sm font-semibold text-amber-900">Nombre</h3>
                  <p class="text-amber-950 mt-0.5">{{ name }}</p>
                </div>
                <button
                  type="button"
                  class="text-sm font-semibold text-amber-800 hover:underline"
                  @click="handleNameChange"
                >
                  Editar
                </button>
              </div>
            </div>

            <!-- Email -->
            <div class="rounded-xl border border-amber-100 bg-amber-50/50 p-4">
              <div v-if="!boolChangeEmail" class="space-y-3">
                <h3 class="text-sm font-semibold text-amber-900">Email</h3>
                <input
                  v-model="email"
                  type="email"
                  class="w-full rounded-xl border border-amber-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                />
                <div class="flex gap-2">
                  <button
                    type="button"
                    class="flex-1 rounded-full bg-amber-800 hover:bg-amber-900 text-white py-2 text-sm font-semibold"
                    @click="changeEmail"
                  >
                    Guardar
                  </button>
                  <button
                    type="button"
                    class="flex-1 rounded-full border border-amber-300 text-amber-900 py-2 text-sm font-medium hover:bg-white"
                    @click="handleChangeEmail"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
              <div v-else class="flex items-center justify-between gap-3">
                <div>
                  <h3 class="text-sm font-semibold text-amber-900">Email</h3>
                  <p class="text-amber-950 mt-0.5">{{ email }}</p>
                </div>
                <button
                  type="button"
                  class="text-sm font-semibold text-amber-800 hover:underline"
                  @click="handleChangeEmail"
                >
                  Editar
                </button>
              </div>
            </div>

            <!-- Contraseña -->
            <div class="rounded-xl border border-amber-100 bg-amber-50/50 p-4">
              <div v-if="!boolChangePassword" class="space-y-3">
                <h3 class="text-sm font-semibold text-amber-900">Cambiar contraseña</h3>
                <input
                  v-model="currentPassword"
                  type="password"
                  autocomplete="current-password"
                  placeholder="Contraseña actual"
                  class="w-full rounded-xl border border-amber-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                />
                <input
                  v-model="newPassword"
                  type="password"
                  autocomplete="new-password"
                  placeholder="Nueva contraseña"
                  class="w-full rounded-xl border border-amber-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                />
                <input
                  v-model="confirmPassword"
                  type="password"
                  autocomplete="new-password"
                  placeholder="Confirmar contraseña"
                  class="w-full rounded-xl border border-amber-300 px-4 py-2.5 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                />
                <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
                <div class="flex gap-2">
                  <button
                    type="button"
                    class="flex-1 rounded-full bg-amber-800 hover:bg-amber-900 text-white py-2 text-sm font-semibold"
                    @click="changePassword"
                  >
                    Guardar
                  </button>
                  <button
                    type="button"
                    class="flex-1 rounded-full border border-amber-300 text-amber-900 py-2 text-sm font-medium hover:bg-white"
                    @click="handleChangePassword"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
              <button
                v-else
                type="button"
                class="w-full text-sm font-semibold text-amber-800 hover:underline py-1"
                @click="handleChangePassword"
              >
                Cambiar contraseña
              </button>
            </div>
          </div>
        </section>

        <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
          <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50">
            <h2 class="font-serif text-lg sm:text-xl font-bold text-amber-950">Apariencia</h2>
            <p class="text-sm text-amber-800/70 mt-0.5">Elige modo día o noche</p>
          </div>
          <div class="p-4 sm:p-5 flex flex-col xs:flex-row gap-2">
            <button
              type="button"
              class="flex-1 rounded-xl border px-4 py-3 text-sm font-semibold transition"
              :class="!isDark
                ? 'border-amber-700 bg-amber-800 text-white'
                : 'border-amber-200 bg-amber-50 text-amber-900 hover:bg-amber-100'"
              @click="applyTheme(false)"
            >
              Modo día
            </button>
            <button
              type="button"
              class="flex-1 rounded-xl border px-4 py-3 text-sm font-semibold transition"
              :class="isDark
                ? 'border-amber-700 bg-amber-800 text-white'
                : 'border-amber-200 bg-amber-50 text-amber-900 hover:bg-amber-100'"
              @click="applyTheme(true)"
            >
              Modo noche
            </button>
          </div>
        </section>

        <section class="rounded-2xl border border-red-200 bg-white shadow-sm p-5 text-center">
          <p class="text-sm text-amber-900/80 mb-3">Esta acción no se puede deshacer.</p>
          <button
            type="button"
            class="inline-flex px-5 py-2.5 rounded-full bg-red-600 hover:bg-red-700 text-white text-sm font-semibold transition"
            @click="deleteProfile"
          >
            Eliminar perfil
          </button>
        </section>

        <section
          v-if="type === 'admin'"
          class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden"
        >
          <div class="px-6 py-4 border-b border-amber-100 bg-amber-50">
            <h2 class="font-serif text-xl font-bold text-amber-950">Administración de usuarios</h2>
          </div>
          <div class="p-5 space-y-3">
            <div
              v-for="(item, index) in users"
              :key="index"
              class="flex items-center justify-between gap-3 rounded-xl border border-amber-100 bg-amber-50/60 p-4"
            >
              <div>
                <p class="font-semibold text-amber-950">{{ item.name }}</p>
                <p class="text-sm text-amber-700">{{ item.email }}</p>
              </div>
              <button
                type="button"
                class="rounded-full bg-red-600 hover:bg-red-700 text-white px-4 py-2 text-sm font-semibold"
                @click="deleteUser(index)"
              >
                Eliminar
              </button>
            </div>
            <p v-if="!users.length" class="text-sm text-amber-700 text-center py-4">
              No hay usuarios para administrar.
            </p>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'ProfileUser' })

import { ref, onMounted, onActivated } from 'vue'
import axios from 'axios'
import { apiUrl, mediaUrl, clearSession } from '../api'
import { useRouter } from 'vue-router'
import PageHero from './PageHero.vue'
import {
  getCachedProfile,
  setCachedProfile,
  patchCachedProfile,
} from '../utils/profileCache'
import { useTheme } from '../utils/theme'

const { isDark, applyTheme } = useTheme()

const cached = getCachedProfile()
const image = ref('')
const imageUrl = ref(cached?.image ? mediaUrl(cached.image) : '')
const name = ref(cached?.name || '')
const email = ref(cached?.email || '')
const loading = ref(!cached?.name && !cached?.email)
const error = ref('')
const payload = ref({
  userToken: localStorage.getItem('userToken'),
  iduser: localStorage.getItem('iduser'),
  name: '',
  email: '',
  newPassword: '',
  confirmPassword: '',
  currentPassword: '',
  type: localStorage.getItem('type'),
})
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const boolChangeName = ref(true)
const boolChangeEmail = ref(true)
const boolChangePassword = ref(true)
const router = useRouter()
const type = localStorage.getItem('type')
const users = ref([])

function handleImageChange(event) {
  const file = event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onloadend = () => {
    image.value = reader.result
    imageUrl.value = reader.result
    changeImage({
      base64: image.value.split(',')[1],
      name: file.name,
    })
  }
  reader.readAsDataURL(file)
}

function handleNameChange() {
  boolChangeName.value = !boolChangeName.value
}

function handleChangeEmail() {
  boolChangeEmail.value = !boolChangeEmail.value
}

function handleChangePassword() {
  boolChangePassword.value = !boolChangePassword.value
}

function changePassword() {
  if (!currentPassword.value) {
    error.value = 'Indica la contraseña actual'
    setTimeout(() => {
      error.value = ''
    }, 3000)
    return
  }
  if (newPassword.value.length < 8) {
    error.value = 'La nueva contraseña debe tener al menos 8 caracteres'
    setTimeout(() => {
      error.value = ''
    }, 3000)
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Las contraseñas no coinciden'
    setTimeout(() => {
      error.value = ''
    }, 3000)
    return
  }
  axios
    .post(apiUrl('/changePassword'), {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value,
    })
    .then((response) => {
      if (response.data.userToken) {
        localStorage.setItem('userToken', response.data.userToken)
        payload.value.userToken = response.data.userToken
      }
      currentPassword.value = ''
      newPassword.value = ''
      confirmPassword.value = ''
      handleChangePassword()
    })
    .catch((err) => {
      error.value = err.response?.data?.message || 'No se pudo cambiar la contraseña'
      setTimeout(() => {
        error.value = ''
      }, 3000)
    })
}

function changeImage(imageData) {
  axios
    .post(apiUrl('/changeImage'), { image: imageData })
    .then((response) => {
      imageUrl.value = mediaUrl(response.data.newImage)
      patchCachedProfile({ image: response.data.newImage || '' })
    })
    .catch((err) => {
      alert(err.response?.data?.message || 'No se pudo cambiar la imagen')
    })
}

function changeName() {
  axios
    .post(apiUrl('/changeName'), { name: name.value })
    .then(() => {
      patchCachedProfile({ name: name.value })
      handleNameChange()
    })
    .catch((err) => {
      alert(err.response?.data?.message || 'No se pudo cambiar el nombre')
    })
}

function changeEmail() {
  axios
    .post(apiUrl('/changeEmail'), { email: email.value })
    .then((response) => {
      if (response.data.userToken) {
        localStorage.setItem('userToken', response.data.userToken)
      }
      patchCachedProfile({ email: email.value })
      handleChangeEmail()
    })
    .catch((err) => {
      alert(err.response?.data?.message || 'No se pudo cambiar el email')
    })
}

function applyProfile(row) {
  if (!row) return
  name.value = row.name || ''
  email.value = row.email || ''
  imageUrl.value = mediaUrl(row.image || '')
  setCachedProfile({
    name: row.name || '',
    email: row.email || '',
    image: row.image || '',
  })
}

function loadProfile({ silent = false } = {}) {
  if (!silent && !name.value && !email.value) loading.value = true
  axios
    .post(apiUrl('/viewProfile'), {})
    .then((response) => {
      applyProfile(response.data.message?.[0])
    })
    .catch((err) => {
      if (!name.value && !email.value) {
        alert(err.response?.data?.message || 'No se pudo cargar el perfil')
      }
    })
    .finally(() => {
      loading.value = false
    })
}

function loadAdminUsers() {
  if (type !== 'admin' || users.value.length) return
  axios
    .post(apiUrl('/allUsers'), {})
    .then((response) => {
      users.value = response.data.users_list || []
    })
    .catch((err) => {
      alert(err.response?.data?.message || 'No se pudieron cargar usuarios')
    })
}

onMounted(() => {
  loadProfile({ silent: Boolean(name.value || email.value) })
  loadAdminUsers()
})

onActivated(() => {
  loadProfile({ silent: true })
})

function deleteProfile() {
  if (!confirm('¿Seguro que quieres eliminar tu perfil? Esta acción no se puede deshacer.')) {
    return
  }
  axios
    .post(apiUrl('/deleteProfile'), {})
    .then(() => {
      clearSession()
      router.push({ name: 'register' })
    })
    .catch((err) => {
      alert(err.response?.data?.message || 'No se pudo eliminar el perfil')
    })
}

function deleteUser(index) {
  if (!confirm('¿Estás seguro de que quieres eliminar este usuario?')) return
  const userId = users.value[index].iduser
  axios
    .post(apiUrl('/deleteUser'), { iduser: userId })
    .then(() => {
      users.value.splice(index, 1)
    })
    .catch((err) => {
      alert(err.response?.data?.message || 'No se pudo eliminar el usuario')
    })
}
</script>
