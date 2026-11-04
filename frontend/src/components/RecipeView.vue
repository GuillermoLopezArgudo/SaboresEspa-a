<template>
  <div>
    <PageHero
      :title="receta?.title || 'Detalle de receta'"
      :subtitle="heroSubtitle"
    >
      <router-link to="/" class="hero-cta-ghost">
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
              class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold shadow-sm transition"
              :class="isFavorite
                ? 'bg-red-600 text-white hover:bg-red-700'
                : 'bg-amber-800 text-white hover:bg-amber-900'"
              @click="toggleFavorite"
            >
              <i class="fa text-lg" :class="isFavorite ? 'fa-heart' : 'fa-heart-o'" />
              {{ isFavorite ? 'Guardada en favoritos' : 'Añadir a favoritos' }}
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
              <RecipeImage
                :path="receta.image"
                :alt="receta.title"
                wrap-class="w-full max-h-[28rem] min-h-[14rem]"
                img-class="max-h-[28rem]"
                loading="eager"
              />
            </div>
            <div
              v-if="receta.video"
              class="rounded-2xl overflow-hidden border border-amber-200 bg-black shadow-sm"
            >
              <iframe
                v-if="youtubeEmbedUrl"
                class="w-full aspect-video"
                :src="youtubeEmbedUrl"
                title="Vídeo de la receta"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                loading="lazy"
                referrerpolicy="strict-origin-when-cross-origin"
              />
              <video
                v-else
                controls
                :src="mediaUrl(receta.video)"
                class="w-full"
              />
            </div>
          </div>

          <div class="lg:col-span-2">
            <div class="h-full rounded-2xl border border-amber-200 bg-white p-5 sm:p-6 shadow-sm">
              <h2 class="text-xl font-serif font-bold text-amber-950 mb-3 tracking-tight">Sobre la receta</h2>
              <p class="se-prose leading-[1.7] text-[15px] sm:text-base whitespace-pre-line font-serif">
                {{ receta.description || 'Sin descripción.' }}
              </p>
              <p class="mt-5 text-xs se-muted-text">
                Pulsa un ingrediente para ver precios orientativos.
              </p>
            </div>
          </div>
        </section>

        <!-- Ingredientes + pasos -->
        <section class="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <aside class="lg:col-span-2 space-y-6">
            <div class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden lg:sticky lg:top-20">
              <div class="px-5 py-4 border-b border-amber-100 bg-amber-50">
                <h3 class="font-serif font-bold text-amber-950 text-xl tracking-tight">Ingredientes</h3>
              </div>
              <ul class="divide-y divide-amber-100">
                <li v-for="(ingrediente, idx) in ingredients" :key="'ing-' + idx">
                  <router-link
                    :to="{ path: '/ingredients', query: { ingredients: ingrediente } }"
                    class="flex items-start justify-between gap-3 px-5 py-3.5 hover:bg-amber-50 transition group"
                  >
                    <div class="min-w-0">
                      <p class="font-medium text-amber-950 group-hover:text-amber-800">
                        {{ ingrediente }}
                      </p>
                      <p class="text-sm se-muted-text mt-0.5">
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

            <div
              v-for="(sub, sIdx) in subrecipes"
              :key="'subing-block-' + sIdx"
              v-show="(sub.ingredients || []).length"
              class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden"
            >
              <div class="px-5 py-4 border-b border-amber-100 bg-amber-50">
                <h3 class="font-serif font-bold text-amber-950 text-xl tracking-tight">
                  {{ sub.title || `Subreceta ${sIdx + 1}` }}
                </h3>
                <p class="text-xs text-amber-700/80 mt-0.5">Ingredientes de la subreceta</p>
              </div>
              <ul class="divide-y divide-amber-100">
                <li
                  v-for="(row, idx) in (sub.ingredients || [])"
                  :key="'subing-' + sIdx + '-' + idx"
                >
                  <router-link
                    :to="{ path: '/ingredients', query: { ingredients: row.ingredients } }"
                    class="flex items-start justify-between gap-3 px-5 py-3.5 hover:bg-amber-50 transition group"
                  >
                    <div class="min-w-0">
                      <p class="font-medium text-amber-950 group-hover:text-amber-800">
                        {{ row.ingredients }}
                      </p>
                      <p class="text-sm se-muted-text mt-0.5">
                        {{ row.quantity || 'Cantidad no indicada' }}
                      </p>
                    </div>
                    <span class="shrink-0 text-xs font-semibold text-amber-700 mt-1 opacity-80 group-hover:opacity-100">
                      Precios →
                    </span>
                  </router-link>
                </li>
              </ul>
            </div>
          </aside>

          <div class="lg:col-span-3 space-y-6">
            <div class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
              <div class="px-5 py-4 border-b border-amber-100 bg-amber-50">
                <h3 class="font-serif font-bold text-amber-950 text-xl tracking-tight">Preparación</h3>
                <p class="text-xs text-amber-700/80 mt-0.5">{{ steps.length }} paso{{ steps.length === 1 ? '' : 's' }}</p>
              </div>
              <div v-if="steps.length" class="p-5 sm:p-6 space-y-5">
                <article
                  v-for="(step, idx) in steps"
                  :key="'step-' + idx"
                  class="relative rounded-2xl border border-amber-100 bg-amber-50/40 p-4 sm:p-5"
                >
                  <div class="flex gap-4">
                    <div class="shrink-0 flex flex-col items-center">
                      <span
                        class="h-10 w-10 rounded-full bg-amber-800 text-white text-base font-bold flex items-center justify-center shadow-sm ring-4 ring-amber-100"
                      >
                        {{ idx + 1 }}
                      </span>
                      <span
                        v-if="idx < steps.length - 1"
                        class="mt-2 w-px flex-1 min-h-[1.5rem] bg-amber-200"
                        aria-hidden="true"
                      />
                    </div>
                    <div class="min-w-0 flex-1 pb-1">
                      <h4 class="font-serif text-lg font-bold text-amber-950 tracking-tight">
                        {{ step.title || `Paso ${idx + 1}` }}
                      </h4>
                      <p class="mt-2 se-prose leading-[1.7] text-[15px] whitespace-pre-line">
                        {{ step.description }}
                      </p>
                      <div
                        v-if="step.image"
                        class="mt-4 rounded-xl overflow-hidden border border-amber-200 max-w-md"
                      >
                        <RecipeImage
                          :path="step.image"
                          :alt="`Paso ${idx + 1}`"
                          wrap-class="w-full h-40 sm:h-48"
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

            <div
              v-for="(sub, sIdx) in subrecipes"
              :key="'substep-block-' + sIdx"
              class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden"
            >
              <div class="px-5 py-4 border-b border-amber-100 bg-amber-50">
                <h3 class="font-serif font-bold text-amber-950 text-xl tracking-tight">
                  Preparación · {{ sub.title || `Subreceta ${sIdx + 1}` }}
                </h3>
                <p class="text-xs text-amber-700/80 mt-0.5">
                  {{ (sub.steps || []).length }} paso{{ (sub.steps || []).length === 1 ? '' : 's' }}
                </p>
              </div>
              <div v-if="(sub.steps || []).length" class="p-5 sm:p-6 space-y-5">
                <article
                  v-for="(step, idx) in sub.steps"
                  :key="'substep-' + sIdx + '-' + idx"
                  class="relative rounded-2xl border border-amber-100 bg-amber-50/40 p-4 sm:p-5"
                >
                  <div class="flex gap-4">
                    <div class="shrink-0 flex flex-col items-center">
                      <span
                        class="h-10 w-10 rounded-full bg-amber-700 text-white text-base font-bold flex items-center justify-center shadow-sm ring-4 ring-amber-100"
                      >
                        {{ idx + 1 }}
                      </span>
                      <span
                        v-if="idx < sub.steps.length - 1"
                        class="mt-2 w-px flex-1 min-h-[1.5rem] bg-amber-200"
                        aria-hidden="true"
                      />
                    </div>
                    <div class="min-w-0 flex-1 pb-1">
                      <h4 class="font-serif text-lg font-bold text-amber-950 tracking-tight">
                        {{ step.title || `Paso ${idx + 1}` }}
                      </h4>
                      <p class="mt-2 se-prose leading-[1.7] text-[15px] whitespace-pre-line">
                        {{ step.description }}
                      </p>
                      <div
                        v-if="step.image"
                        class="mt-4 rounded-xl overflow-hidden border border-amber-200 max-w-md"
                      >
                        <RecipeImage
                          :path="step.image"
                          :alt="`${sub.title} paso ${idx + 1}`"
                          wrap-class="w-full h-40 sm:h-48"
                        />
                      </div>
                    </div>
                  </div>
                </article>
              </div>
              <p v-else class="px-5 py-6 text-sm text-amber-700">
                Sin pasos publicados para esta subreceta.
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
                  <p class="se-prose leading-relaxed">{{ c.comment }}</p>
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
import { computed, ref, onMounted, onBeforeUnmount, watch } from 'vue'
import axios from 'axios'
import { apiUrl, mediaUrl } from '../api'
import { useRouter, useRoute } from 'vue-router'
import PageHero from './PageHero.vue'
import RecipeImage from './RecipeImage.vue'
import { labelForFilter } from '../utils/filterOptions'
import { setPageSeo, resetPageSeo } from '../utils/seo'
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
const subrecipes = ref([])
const filters = ref([])
const comments = ref([])
const isFavorite = ref(false)
const editingCommentId = ref(null)
const editedComment = ref('')

function youtubeIdFromUrl(raw) {
  if (!raw || typeof raw !== 'string') return null
  const url = raw.trim()
  const patterns = [
    /(?:youtube\.com\/watch\?[^#]*v=)([\w-]{11})/i,
    /(?:youtu\.be\/)([\w-]{11})/i,
    /(?:youtube\.com\/embed\/)([\w-]{11})/i,
    /(?:youtube-nocookie\.com\/embed\/)([\w-]{11})/i,
  ]
  for (const re of patterns) {
    const m = url.match(re)
    if (m?.[1]) return m[1]
  }
  return null
}

const youtubeEmbedUrl = computed(() => {
  const id = youtubeIdFromUrl(receta.value?.video)
  return id ? `https://www.youtube-nocookie.com/embed/${id}` : null
})

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

watch(
  receta,
  (r) => {
    if (!r) return
    setPageSeo({
      title: r.title,
      description: (r.description || `Receta de ${r.author || 'Sabores España'}`).slice(0, 160),
      image: r.image ? mediaUrl(r.image) : undefined,
      url: typeof window !== 'undefined' ? window.location.href : undefined,
      type: 'article',
    })
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  resetPageSeo()
})

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
      subrecipes.value = response.data.subrecipes || []
      // Compat: si solo viene el formato plano antiguo, envolver en una subreceta
      if (
        !subrecipes.value.length &&
        ((response.data.subingredient_list || []).length ||
          (response.data.substep_list || []).length)
      ) {
        subrecipes.value = [
          {
            title: 'Subreceta',
            ingredients: response.data.subingredient_list || [],
            steps: response.data.substep_list || [],
          },
        ]
      }
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
