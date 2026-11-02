<template>
  <div>
    <PageHero
      :title="receta?.title || 'Detalle de receta'"
      :subtitle="heroSubtitle"
    >
      <router-link
        to="/"
        class="inline-flex items-center px-4 py-2 rounded-full bg-white/15 hover:bg-white/25 text-white text-sm font-medium border border-white/20 transition"
      >
        ← Volver al recetario
      </router-link>
    </PageHero>

    <div class="max-w-6xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600" />
        <p class="mt-4 text-amber-700">Cargando receta…</p>
      </div>

      <div v-else-if="receta" class="space-y-6">
        <!-- Cabecera de acciones -->
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex flex-wrap items-center gap-2 text-sm text-amber-800/80">
            <span v-if="receta.author" class="font-medium text-amber-900">
              Por {{ receta.author }}
            </span>
            <span v-if="filters.length" class="text-amber-400">·</span>
            <button
              v-for="f in filters"
              :key="f.category + f.type"
              type="button"
              class="px-2.5 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-medium"
              disabled
            >
              {{ filterLabel(f) }}
            </button>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <button
              type="button"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-amber-200 bg-white text-amber-900 text-sm font-medium hover:border-amber-400 transition"
              @click="toggleFavorite"
            >
              <i class="fa text-lg" :class="isFavorite ? 'fa-heart text-red-500' : 'fa-heart-o text-amber-700'" />
              {{ isFavorite ? 'En favoritos' : 'Favorito' }}
            </button>
            <template v-if="canManage">
              <button
                type="button"
                class="px-4 py-2 rounded-full bg-amber-700 hover:bg-amber-800 text-white text-sm font-medium transition"
                @click="editeRecipe"
              >
                Editar
              </button>
              <button
                type="button"
                class="px-4 py-2 rounded-full bg-red-600 hover:bg-red-700 text-white text-sm font-medium transition"
                @click="deleteRecipe"
              >
                Eliminar
              </button>
            </template>
          </div>
        </div>

        <!-- Media + descripción -->
        <section class="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <div class="lg:col-span-3 space-y-4">
            <div
              v-if="receta.image"
              class="rounded-2xl overflow-hidden border border-amber-200 bg-amber-100 shadow-sm"
            >
              <img
                :src="mediaUrl(receta.image)"
                :alt="receta.title"
                class="w-full max-h-[28rem] object-cover"
              />
            </div>
            <div
              v-if="receta.video"
              class="rounded-2xl overflow-hidden border border-amber-200 bg-black shadow-sm"
            >
              <video controls :src="mediaUrl(receta.video)" class="w-full" />
            </div>
          </div>

          <div class="lg:col-span-2">
            <div class="h-full rounded-2xl border border-amber-200 bg-white p-5 sm:p-6 shadow-sm">
              <h2 class="text-lg font-serif font-bold text-amber-950 mb-3">Sobre la receta</h2>
              <p class="text-amber-800/90 leading-relaxed whitespace-pre-line">
                {{ receta.description || 'Sin descripción.' }}
              </p>
              <p class="mt-5 text-xs text-amber-700/80">
                Pulsa un ingrediente para ver precios en Mercadona.
              </p>
            </div>
          </div>
        </section>

        <!-- Ingredientes + pasos -->
        <section class="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <aside class="lg:col-span-2">
            <div class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden lg:sticky lg:top-20">
              <div class="px-5 py-4 border-b border-amber-100 bg-amber-50">
                <h3 class="font-serif font-bold text-amber-950 text-lg">Ingredientes</h3>
              </div>
              <ul class="divide-y divide-amber-100">
                <li v-for="(ingrediente, idx) in ingredients" :key="idx">
                  <router-link
                    :to="{ path: '/ingredients', query: { ingredients: ingrediente } }"
                    class="flex items-start justify-between gap-3 px-5 py-3.5 hover:bg-amber-50 transition group"
                  >
                    <div class="min-w-0">
                      <p class="font-medium text-amber-950 group-hover:text-amber-800">
                        {{ ingrediente }}
                      </p>
                      <p class="text-sm text-amber-700/80 mt-0.5">
                        {{ quantity[idx] || 'Cantidad no indicada' }}
                      </p>
                    </div>
                    <span class="shrink-0 text-xs font-semibold text-amber-700 mt-1 opacity-80 group-hover:opacity-100">
                      Precios →
                    </span>
                  </router-link>
                </li>
                <li v-if="!ingredients.length" class="px-5 py-6 text-sm text-amber-700">
                  Esta receta no tiene ingredientes listados.
                </li>
              </ul>
            </div>
          </aside>

          <div class="lg:col-span-3">
            <div class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
              <div class="px-5 py-4 border-b border-amber-100 bg-amber-50">
                <h3 class="font-serif font-bold text-amber-950 text-lg">Preparación</h3>
              </div>
              <div v-if="steps.length" class="p-5 space-y-4">
                <article
                  v-for="(step, idx) in steps"
                  :key="idx"
                  class="rounded-xl border border-amber-100 bg-amber-50/40 p-4"
                >
                  <div class="flex gap-3">
                    <span
                      class="shrink-0 h-8 w-8 rounded-full bg-amber-800 text-white text-sm font-bold flex items-center justify-center"
                    >
                      {{ idx + 1 }}
                    </span>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-semibold text-amber-950">
                        {{ step.title || `Paso ${idx + 1}` }}
                      </h4>
                      <p class="mt-1 text-amber-800/90 leading-relaxed whitespace-pre-line">
                        {{ step.description }}
                      </p>
                      <div
                        v-if="step.image"
                        class="mt-3 rounded-lg overflow-hidden border border-amber-200 max-w-md"
                      >
                        <img
                          :src="mediaUrl(step.image)"
                          :alt="`Paso ${idx + 1}`"
                          class="w-full object-cover"
                        />
                      </div>
                    </div>
                  </div>
                </article>
              </div>
              <p v-else class="px-5 py-8 text-sm text-amber-700">
                No hay pasos publicados para esta receta.
              </p>
            </div>
          </div>
        </section>

        <!-- Comentarios -->
        <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
          <div class="px-5 py-4 border-b border-amber-100 bg-amber-50 flex items-center justify-between gap-3">
            <h3 class="font-serif font-bold text-amber-950 text-lg">Comentarios</h3>
            <span class="text-xs text-amber-700">{{ comments.length }}</span>
          </div>

          <div class="p-5 space-y-4">
            <div v-if="comments.length" class="space-y-3">
              <article
                v-for="c in comments"
                :key="c.id"
                class="rounded-xl border border-amber-100 bg-amber-50/50 p-4"
              >
                <div v-if="editingCommentId === c.id" class="space-y-2">
                  <textarea
                    v-model="editedComment"
                    rows="3"
                    class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                  />
                  <div class="flex gap-2">
                    <button
                      type="button"
                      class="px-3 py-1.5 rounded-lg bg-amber-800 text-white text-sm"
                      @click="updateComment(c.id)"
                    >
                      Guardar
                    </button>
                    <button
                      type="button"
                      class="px-3 py-1.5 rounded-lg border border-amber-300 text-amber-900 text-sm"
                      @click="cancelEdit"
                    >
                      Cancelar
                    </button>
                  </div>
                </div>
                <div v-else>
                  <p class="text-amber-950 leading-relaxed">{{ c.comment }}</p>
                  <div class="mt-2 flex flex-wrap items-center justify-between gap-2">
                    <p class="text-xs font-medium text-amber-700">{{ c.username || 'Usuario' }}</p>
                    <div
                      v-if="iduser == c.iduser || type == 'admin'"
                      class="flex gap-2"
                    >
                      <button
                        type="button"
                        class="text-xs text-amber-800 hover:underline"
                        @click="startEditComment(c)"
                      >
                        Editar
                      </button>
                      <button
                        type="button"
                        class="text-xs text-red-600 hover:underline"
                        @click="deleteComment(c.id)"
                      >
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              </article>
            </div>
            <p
              v-else
              class="rounded-xl border border-dashed border-amber-200 px-4 py-6 text-center text-sm text-amber-700"
            >
              Todavía no hay comentarios. Sé el primero.
            </p>

            <div v-if="userToken" class="pt-2 border-t border-amber-100">
              <textarea
                v-model="comment"
                rows="3"
                placeholder="Escribe tu comentario…"
                class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              />
              <button
                type="button"
                class="mt-2 w-full sm:w-auto px-5 py-2.5 rounded-full bg-amber-800 hover:bg-amber-900 text-white text-sm font-semibold transition"
                @click.prevent="createComment"
              >
                Publicar comentario
              </button>
            </div>
            <p v-else class="text-sm text-amber-800">
              <router-link to="/login" class="font-medium underline hover:text-amber-950">
                Inicia sesión
              </router-link>
              para comentar.
            </p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { apiUrl, mediaUrl } from '../api'
import { useRouter, useRoute } from 'vue-router'
import PageHero from './PageHero.vue'
import { labelForFilter } from '../utils/filterOptions'
import 'font-awesome/css/font-awesome.min.css'

const route = useRoute()
const router = useRouter()
const recipeId = route.query.id
const loading = ref(true)
const receta = ref(null)
const comment = ref('')
const userToken = localStorage.getItem('userToken')
const iduser = localStorage.getItem('iduser')
const type = localStorage.getItem('type')
const ingredients = ref([])
const quantity = ref([])
const steps = ref([])
const filters = ref([])
const comments = ref([])
const isFavorite = ref(false)
const editingCommentId = ref(null)
const editedComment = ref('')

const payload = {
  idrecipe: parseInt(recipeId, 10),
  comment: '',
  idcomment: 0,
}

const canManage = computed(
  () => iduser == receta.value?.id_user || type === 'admin'
)

const heroSubtitle = computed(() => {
  if (!receta.value) return 'Cargando…'
  if (receta.value.author) return `Por ${receta.value.author}`
  return 'Ingredientes, pasos y opiniones'
})

function filterLabel(f) {
  return labelForFilter(f.category, f.type)
}

function toggleFavorite() {
  if (!iduser) {
    router.push({ name: 'login' })
    return
  }
  isFavorite.value = !isFavorite.value
  const url = isFavorite.value ? '/updateFavs' : '/deleteFavs'
  axios.post(apiUrl(url), { idrecipe: payload.idrecipe }).catch((error) => {
    isFavorite.value = !isFavorite.value
    alert(error.response?.data?.message || 'Error al actualizar favoritos')
  })
}

function fetchComments() {
  axios
    .post(apiUrl('/viewComment'), payload)
    .then((response) => {
      comments.value = response.data.comment_list || []
    })
    .catch((error) => console.error('Error en la solicitud:', error))
}

onMounted(() => {
  loading.value = true
  axios
    .post(apiUrl('/viewRecipe'), payload)
    .then((response) => {
      if (!response.data.recipe_list?.length) {
        alert('Receta no encontrada')
        router.push({ name: 'landing' })
        return
      }
      receta.value = response.data.recipe_list[0]
      ingredients.value = []
      quantity.value = []
      ;(response.data.ingredient_list || []).forEach((element) => {
        ingredients.value.push(element.ingredients)
        quantity.value.push(element.quantity)
      })
      steps.value = response.data.step_list || []
      filters.value = response.data.filters_list || []
      fetchComments()
      const favs = response.data.favorites_list || []
      if (iduser) {
        isFavorite.value = favs.some(
          (id) => id.id_recipe === parseInt(recipeId, 10)
        )
      }
    })
    .catch((error) => {
      alert(error.response?.data?.message || 'No se pudo cargar la receta')
      router.push({ name: 'landing' })
    })
    .finally(() => {
      loading.value = false
    })
})

function deleteRecipe() {
  if (!confirm('¿Estás seguro de que quieres eliminar esta receta?')) return
  axios
    .post(apiUrl('/deleteRecipe'), payload)
    .then(() => router.push({ name: 'landing' }))
    .catch((error) => {
      alert(error.response?.data?.message || 'No se pudo eliminar la receta')
    })
}

function editeRecipe() {
  router.push({ name: 'edit', query: { id: recipeId } })
}

function createComment() {
  if (!comment.value.trim()) return
  payload.comment = comment.value
  if (!userToken) {
    router.push({ name: 'login' })
    return
  }
  axios
    .post(apiUrl('/createComment'), payload)
    .then(() => {
      fetchComments()
      comment.value = ''
    })
    .catch((error) => {
      alert(error.response?.data?.message || 'No se pudo publicar el comentario')
    })
}

function deleteComment(idcomment) {
  if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) return
  payload.idcomment = idcomment
  axios
    .post(apiUrl('/deleteComment'), payload)
    .then(() => fetchComments())
    .catch((error) => {
      alert(error.response?.data?.message || 'No se pudo eliminar el comentario')
    })
}

function updateComment(idcomment) {
  payload.idcomment = idcomment
  payload.comment = editedComment.value
  axios
    .post(apiUrl('/editComment'), payload)
    .then(() => {
      fetchComments()
      cancelEdit()
    })
    .catch((error) => {
      alert(error.response?.data?.message || 'No se pudo editar el comentario')
    })
}

function startEditComment(c) {
  editingCommentId.value = c.id
  editedComment.value = c.comment
}

function cancelEdit() {
  editingCommentId.value = null
  editedComment.value = ''
}
</script>
