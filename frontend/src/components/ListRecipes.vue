<template>
  <div class="space-y-5">
    <!-- Toolbar: búsqueda + orden + contador -->
    <div
      v-if="showToolbar"
      class="flex flex-col lg:flex-row lg:items-center gap-3"
    >
      <div class="relative flex-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-amber-700/60"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Buscar por título, autor o descripción…"
          class="list-search w-full rounded-full border border-amber-200 bg-white pl-10 pr-4 py-2.5 text-sm text-amber-950 placeholder:text-amber-700/50 shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
        />
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <span
          class="inline-flex items-center px-3 py-1.5 rounded-full bg-amber-900 text-amber-50 text-sm font-medium"
        >
          {{ pagination.total }}
          receta{{ pagination.total === 1 ? '' : 's' }}
        </span>
        <label class="inline-flex items-center gap-2 text-sm text-amber-900">
          <span class="text-amber-800/70 hidden sm:inline">Ordenar</span>
          <select
            v-model="sortBy"
            class="list-sort rounded-full border border-amber-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="rating-desc">Mejor valoradas</option>
            <option value="title-asc">Título A–Z</option>
            <option value="author-asc">Autor A–Z</option>
          </select>
        </label>
      </div>
    </div>

    <!-- Skeleton -->
    <div
      v-if="loading && !elementos.recetas.length"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5"
    >
      <div
        v-for="n in 6"
        :key="'sk-' + n"
        class="rounded-2xl overflow-hidden border border-amber-100 bg-white animate-pulse"
      >
        <div class="h-44 sm:h-52 bg-amber-100" />
        <div class="p-5 space-y-3">
          <div class="h-5 bg-amber-100 rounded w-3/4" />
          <div class="h-3 bg-amber-50 rounded w-1/3" />
          <div class="h-4 bg-amber-50 rounded w-full" />
          <div class="h-4 bg-amber-50 rounded w-2/3" />
        </div>
      </div>
    </div>

    <!-- Listado -->
    <div
      v-else-if="visibleRecipes.length > 0"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5"
    >
      <article
        v-for="item in visibleRecipes"
        :key="item.id"
        role="link"
        tabindex="0"
        class="group flex flex-col rounded-2xl overflow-hidden border border-amber-200 bg-white shadow-sm hover:shadow-lg hover:-translate-y-0.5 transition duration-300 cursor-pointer focus:outline-none focus:ring-2 focus:ring-amber-500"
        @click="openRecipe(item.id)"
        @keydown.enter.prevent="openRecipe(item.id)"
      >
        <div class="relative overflow-hidden">
          <div
            class="absolute top-3 left-3 z-[1] inline-flex items-center gap-1 rounded-full bg-amber-950/85 text-amber-50 px-2.5 py-1 text-xs font-semibold backdrop-blur-sm"
          >
            <span>{{ ratingLabel(item.id) }}</span>
            <span aria-hidden="true">★</span>
          </div>

          <button
            v-if="props.greeting !== 'personal'"
            type="button"
            class="absolute top-3 right-3 z-[1] h-10 w-10 rounded-full bg-white/90 shadow-md text-amber-700 hover:bg-white transition flex items-center justify-center"
            :aria-label="isFavorite(item.id) ? 'Quitar de favoritos' : 'Añadir a favoritos'"
            @click.stop="toggleFavorite(item.id)"
          >
            <i
              class="fa text-xl"
              :class="isFavorite(item.id) ? 'fa-heart text-red-500' : 'fa-heart-o'"
            />
          </button>

          <RecipeImage
            :path="item.image"
            :alt="item.title"
            wrap-class="h-44 sm:h-52"
            img-class="transition duration-500 group-hover:scale-105"
          />
        </div>

        <div class="flex flex-1 flex-col p-4 sm:p-5">
          <h3 class="text-lg sm:text-xl font-bold text-amber-950 font-serif line-clamp-1 group-hover:text-amber-800 transition">
            {{ item.title }}
          </h3>
          <p class="mt-1 text-sm font-medium text-amber-800/75">
            {{ item.author ? `Por ${item.author}` : 'Autor desconocido' }}
          </p>
          <p class="mt-2 text-sm text-amber-700/90 line-clamp-2 min-h-[2.5rem]">
            {{ item.description || 'Sin descripción.' }}
          </p>

          <div
            v-if="props.greeting !== 'personal'"
            class="mt-4 pt-3 border-t border-amber-100"
            @click.stop
          >
            <p class="text-[11px] uppercase tracking-wide text-amber-700/70 mb-1">Tu nota</p>
            <StarRating
              :rating="ratings[item.id] || 0"
              :onRatingChanged="ratingChanged(item.id)"
              :showRatingText="false"
            />
          </div>

          <div class="mt-3" @click.stop>
            <div v-if="catsFor(item.id).length" class="flex flex-wrap gap-1.5">
              <button
                v-for="cat in visibleCats(item.id)"
                :key="cat.type + cat.category"
                type="button"
                class="inline-flex px-2.5 py-1 rounded-full bg-amber-50 hover:bg-amber-800 hover:text-white text-amber-900 text-xs font-medium border border-amber-100 transition"
                :title="'Filtrar por ' + categoryLabel(cat)"
                @click="onCategoryClick(cat)"
              >
                {{ categoryLabel(cat) }}
              </button>
              <button
                v-if="extraCatsCount(item.id) > 0 && !isCatsExpanded(item.id)"
                type="button"
                class="inline-flex px-2.5 py-1 rounded-full bg-amber-100 hover:bg-amber-800 hover:text-white text-amber-900 text-xs font-semibold border border-amber-200 transition"
                :title="'Ver las ' + catsFor(item.id).length + ' categorías'"
                @click="expandCats(item.id)"
              >
                +{{ extraCatsCount(item.id) }}
              </button>
              <button
                v-else-if="isCatsExpanded(item.id) && catsFor(item.id).length > MAX_CATS"
                type="button"
                class="inline-flex px-2.5 py-1 rounded-full border border-amber-200 text-amber-800/80 hover:bg-amber-50 text-xs font-medium transition"
                title="Mostrar menos"
                @click="collapseCats(item.id)"
              >
                Menos
              </button>
            </div>
            <p v-else class="text-xs text-amber-600/80 italic">Sin categorías</p>
          </div>
        </div>
      </article>
    </div>

    <!-- Error de carga -->
    <div
      v-else-if="loadError"
      class="rounded-2xl border border-red-200 bg-red-50 px-6 py-12 text-center"
    >
      <p class="font-serif text-2xl font-bold text-red-900">No se pudo cargar</p>
      <p class="mt-2 text-red-800/90 max-w-md mx-auto text-sm">{{ loadError }}</p>
      <button
        type="button"
        class="mt-6 inline-flex px-5 py-2.5 rounded-full bg-red-700 hover:bg-red-800 text-white text-sm font-semibold"
        @click="retryLoad"
      >
        Reintentar
      </button>
    </div>

    <!-- Vacío / sin coincidencias -->
    <div
      v-else-if="!loading"
      class="rounded-2xl border border-amber-200 bg-white px-6 py-14 text-center"
    >
      <p class="font-serif text-2xl font-bold text-amber-950">
        {{ searchQuery.trim() ? 'Sin coincidencias' : emptyTitle }}
      </p>
      <p class="mt-2 text-amber-800/80 max-w-md mx-auto">
        <template v-if="searchQuery.trim()">
          No hay recetas para “{{ searchQuery }}”. Prueba otro término o quita filtros.
        </template>
        <template v-else>
          {{ emptySubtitle }}
        </template>
      </p>
      <div class="mt-6 flex flex-wrap justify-center gap-2">
        <button
          v-if="searchQuery.trim()"
          type="button"
          class="inline-flex px-4 py-2 rounded-full border border-amber-300 text-amber-900 text-sm font-medium hover:bg-amber-50"
          @click="searchQuery = ''"
        >
          Limpiar búsqueda
        </button>
        <router-link
          v-else-if="emptyLink"
          :to="emptyLink.to"
          class="se-btn-primary"
        >
          {{ emptyLink.label }}
        </router-link>
      </div>
    </div>

    <!-- Paginador -->
    <nav
      v-if="pagination.total_pages > 1"
      class="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2"
      aria-label="Paginación"
    >
      <p class="text-sm text-amber-800/80 order-2 sm:order-1">
        Página {{ pagination.page }} de {{ pagination.total_pages }}
      </p>
      <div class="flex flex-wrap items-center justify-center gap-1.5 order-1 sm:order-2">
        <button
          type="button"
          class="pager-btn"
          :disabled="!pagination.has_prev || loading"
          @click="goToPage(pagination.page - 1)"
        >
          Anterior
        </button>
        <button
          v-for="p in pageButtons"
          :key="'p-' + p"
          type="button"
          class="pager-btn min-w-[2.5rem]"
          :class="{ 'pager-btn-active': p === pagination.page }"
          :disabled="loading || p === '…'"
          @click="p !== '…' && goToPage(p)"
        >
          {{ p }}
        </button>
        <button
          type="button"
          class="pager-btn"
          :disabled="!pagination.has_next || loading"
          @click="goToPage(pagination.page + 1)"
        >
          Siguiente
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import StarRating from './StarRating.vue'
import RecipeImage from './RecipeImage.vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { apiUrl } from '../api'
import {
  getAverageStarsCache,
  invalidateRecipeCaches,
  setAverageStarsCache,
} from '../utils/recipeCache'
import { labelForFilter } from '../utils/filterOptions'

const emit = defineEmits(['seleccionarCategoria'])

const PAGE_SIZE = 12

const favoritos = reactive({})
const ratings = reactive({})
const average = reactive({})
const userToken = localStorage.getItem('userToken')
const router = useRouter()
const route = useRoute()
const elementos = reactive({ recetas: [] })
const categorias = reactive([])
const loading = ref(false)
const loadError = ref('')
const searchQuery = ref('')
const sortBy = ref('rating-desc')
const currentPage = ref(1)
let syncingUrl = false
const pagination = reactive({
  page: 1,
  page_size: PAGE_SIZE,
  total: 0,
  total_pages: 1,
  has_next: false,
  has_prev: false,
})

const MAX_CATS = 3
const expandedCats = reactive({})
let searchDebounce = null

function setCategories(list) {
  categorias.splice(0, categorias.length, ...(list || []))
}

const catsByRecipe = computed(() => {
  const map = Object.create(null)
  for (const cat of categorias) {
    const id = cat.recipe_id
    if (!map[id]) map[id] = []
    map[id].push(cat)
  }
  return map
})

let loadGen = 0

const props = defineProps({
  greeting: {
    type: String,
    required: true,
  },
  filterCriteria: {
    type: Object,
    default: null,
  },
  syncUrl: {
    type: Boolean,
    default: false,
  },
})

function readUrlState() {
  if (!props.syncUrl) return
  const q = typeof route.query.q === 'string' ? route.query.q : ''
  const sort = typeof route.query.sort === 'string' ? route.query.sort : 'rating-desc'
  const page = parseInt(String(route.query.page || '1'), 10)
  syncingUrl = true
  searchQuery.value = q
  if (['rating-desc', 'title-asc', 'author-asc'].includes(sort)) sortBy.value = sort
  currentPage.value = Number.isFinite(page) && page > 0 ? page : 1
  queueMicrotask(() => {
    syncingUrl = false
  })
}

function writeUrlState() {
  if (!props.syncUrl || syncingUrl) return
  const query = { ...route.query }
  const q = searchQuery.value.trim()
  if (q) query.q = q
  else delete query.q
  if (sortBy.value && sortBy.value !== 'rating-desc') query.sort = sortBy.value
  else delete query.sort
  if (currentPage.value > 1) query.page = String(currentPage.value)
  else delete query.page
  router.replace({ query }).catch(() => {})
}

const showToolbar = computed(
  () =>
    loading.value ||
    elementos.recetas.length > 0 ||
    searchQuery.value ||
    pagination.total > 0
)

const visibleRecipes = computed(() => elementos.recetas)

const pageButtons = computed(() => {
  const total = pagination.total_pages || 1
  const current = pagination.page || 1
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  const pages = new Set([1, total, current, current - 1, current + 1, current - 2, current + 2])
  const sorted = [...pages].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b)
  const out = []
  let prev = 0
  for (const p of sorted) {
    if (prev && p - prev > 1) out.push('…')
    out.push(p)
    prev = p
  }
  return out
})

const emptyTitle = computed(() => {
  if (props.greeting === 'favs') return 'No tienes favoritos'
  if (props.greeting === 'personal') return 'Aún no has publicado'
  if (props.greeting === 'filtred') return 'Sin resultados para el filtro'
  return 'Todavía no hay recetas'
})

const emptySubtitle = computed(() => {
  if (props.greeting === 'favs') {
    return 'Guarda recetas con el corazón para encontrarlas aquí.'
  }
  if (props.greeting === 'personal') {
    return 'Comparte tu primera creación con la comunidad.'
  }
  if (props.greeting === 'filtred') {
    return 'Prueba a quitar algún filtro o elige otras categorías.'
  }
  return 'Sé el primero en compartir una receta de la cocina española.'
})

const emptyLink = computed(() => {
  if (props.greeting === 'favs') return { to: '/', label: 'Explorar recetario' }
  if (props.greeting === 'personal' || props.greeting === 'all') {
    return { to: '/create', label: 'Crear receta' }
  }
  return null
})

watch(
  () => [props.greeting, props.filterCriteria],
  () => {
    currentPage.value = 1
    reloadList()
  },
  { deep: true }
)

watch(sortBy, () => {
  if (syncingUrl) return
  currentPage.value = 1
  writeUrlState()
  reloadList()
})

watch(searchQuery, () => {
  if (syncingUrl) return
  if (searchDebounce) clearTimeout(searchDebounce)
  searchDebounce = setTimeout(() => {
    currentPage.value = 1
    writeUrlState()
    reloadList()
  }, 350)
})

watch(
  () => [route.query.q, route.query.page, route.query.sort],
  () => {
    if (!props.syncUrl) return
    readUrlState()
    reloadList()
  }
)

onBeforeUnmount(() => {
  if (searchDebounce) clearTimeout(searchDebounce)
})

function selectFavorites(favorites_list) {
  Object.keys(favoritos).forEach((k) => {
    delete favoritos[k]
  })
  ;(favorites_list || []).forEach((recipe) => {
    const recipeId = recipe.id_recipe || recipe.id
    favoritos[recipeId] = true
  })
}

function selectReviews(reviews_list) {
  Object.keys(ratings).forEach((k) => {
    delete ratings[k]
  })
  ;(reviews_list || []).forEach((recipe) => {
    ratings[recipe.id_recipe] = recipe.review
  })
}

function applyPagination(meta) {
  const m = meta || {}
  pagination.page = m.page || currentPage.value || 1
  pagination.page_size = m.page_size || PAGE_SIZE
  pagination.total = m.total || 0
  pagination.total_pages = m.total_pages || 1
  pagination.has_next = !!m.has_next
  pagination.has_prev = !!m.has_prev
  currentPage.value = pagination.page
}

function applyListPayload(recipes, data = {}) {
  elementos.recetas = recipes || []
  selectFavorites(data.favorites_list || [])
  selectReviews(data.reviews_list || [])
  setCategories(data.categories_list)
  applyPagination(data.pagination)
}

function applyAverages(media) {
  ;(media || []).forEach((rating) => {
    average[rating.recipe_id] = rating.average_rating
  })
}

function listQuery() {
  return {
    page: currentPage.value,
    page_size: PAGE_SIZE,
    q: searchQuery.value.trim(),
    sort: sortBy.value,
  }
}

function reloadList() {
  if (props.greeting === 'favs') favoritesRecipes()
  else if (props.greeting === 'personal') personalRecipes()
  else if (props.greeting === 'filtred') filteredRecipes()
  else allRecipes()
}

function goToPage(page) {
  const next = Number(page)
  if (!Number.isFinite(next) || next < 1 || next > pagination.total_pages) return
  if (next === currentPage.value) return
  currentPage.value = next
  writeUrlState()
  reloadList()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function retryLoad() {
  loadError.value = ''
  reloadList()
}

onMounted(() => {
  readUrlState()
  reloadList()
  averageStars()
})

function openRecipe(id) {
  router.push({ path: '/recipe', query: { id } })
}

function categoryLabel(cat) {
  return labelForFilter(cat.category, cat.type)
}

function onCategoryClick(cat) {
  emit('seleccionarCategoria', {
    category: cat.category,
    type: cat.type,
  })
}

function catsFor(id) {
  return catsByRecipe.value[id] || []
}

function isCatsExpanded(id) {
  return !!expandedCats[id]
}

function expandCats(id) {
  expandedCats[id] = true
}

function collapseCats(id) {
  expandedCats[id] = false
}

function visibleCats(id) {
  const all = catsFor(id)
  return isCatsExpanded(id) ? all : all.slice(0, MAX_CATS)
}

function extraCatsCount(id) {
  return Math.max(0, catsFor(id).length - MAX_CATS)
}

function ratingLabel(id) {
  const v = average[id]
  if (v === undefined || v === null || Number.isNaN(Number(v))) return '—'
  return Number(v).toFixed(1)
}

function allRecipes() {
  loading.value = true
  loadError.value = ''
  const gen = ++loadGen
  axios
    .post(apiUrl('/viewAll'), listQuery())
    .then((response) => {
      if (gen !== loadGen) return
      const data = response.data || {}
      applyListPayload(data.recipes_list || [], data)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error en la solicitud:', error)
      elementos.recetas = []
      loadError.value =
        error.response?.data?.message || 'No se pudieron cargar las recetas. Comprueba la conexión.'
    })
    .finally(() => {
      if (gen === loadGen) loading.value = false
    })
}

function favoritesRecipes() {
  if (!userToken) {
    router.push({ name: 'login' })
    return
  }
  loading.value = true
  loadError.value = ''
  const gen = ++loadGen
  axios
    .post(apiUrl('/viewFavs'), listQuery())
    .then((response) => {
      if (gen !== loadGen) return
      const data = response.data || {}
      const recipes = data.favorites_list || []
      applyListPayload(recipes, {
        ...data,
        favorites_list: recipes.map((r) => ({ id_recipe: r.id })),
      })
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error en la solicitud:', error)
      elementos.recetas = []
      loadError.value = error.response?.data?.message || 'No se pudieron cargar favoritos'
    })
    .finally(() => {
      if (gen === loadGen) loading.value = false
    })
}

function personalRecipes() {
  if (!userToken) {
    router.push({ name: 'login' })
    return
  }
  loading.value = true
  loadError.value = ''
  const gen = ++loadGen
  axios
    .post(apiUrl('/viewRecipes'), listQuery())
    .then((response) => {
      if (gen !== loadGen) return
      const data = response.data || {}
      applyListPayload(data.message || [], data)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error al obtener las recetas:', error)
      elementos.recetas = []
      loadError.value = error.response?.data?.message || 'No se pudieron cargar tus recetas'
    })
    .finally(() => {
      if (gen === loadGen) loading.value = false
    })
}

function filteredRecipes() {
  const criteria = props.filterCriteria
  if (!criteria) {
    allRecipes()
    return
  }

  loading.value = true
  loadError.value = ''
  const gen = ++loadGen
  axios
    .post(apiUrl('/filterRecipe'), {
      ...listQuery(),
      typeeat: criteria.typeeat || '',
      ccaa: criteria.ccaa || '',
      time: criteria.time || '',
      proteins: Array.isArray(criteria.proteins) ? criteria.proteins : [],
    })
    .then((response) => {
      if (gen !== loadGen) return
      const data = response.data || {}
      applyListPayload(data.filtered_recipes || [], data)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error en la solicitud:', error)
      elementos.recetas = []
      loadError.value = error.response?.data?.message || 'No se pudieron filtrar las recetas'
    })
    .finally(() => {
      if (gen === loadGen) loading.value = false
    })
}

const toggleFavorite = (id) => {
  if (!userToken) {
    router.push({ name: 'login' })
    return
  }
  const payload = { idrecipe: id }
  if (favoritos[id]) {
    favoritos[id] = false
    invalidateRecipeCaches()
    axios.post(apiUrl('/deleteFavs'), payload).catch((error) => {
      favoritos[id] = true
      alert(error.response?.data?.message || 'No se pudo quitar de favoritos')
    })
  } else {
    favoritos[id] = true
    invalidateRecipeCaches()
    axios.post(apiUrl('/updateFavs'), payload).catch((error) => {
      favoritos[id] = false
      alert(error.response?.data?.message || 'No se pudo añadir a favoritos')
    })
  }
}

const isFavorite = (id) => favoritos[id] || false

const ratingChanged = (recipeId) => {
  return (newRating) => {
    if (!userToken) {
      router.push({ name: 'login' })
      return
    }
    ratings[recipeId] = newRating
    axios
      .post(apiUrl('/updateRating'), {
        idrecipe: recipeId,
        rating: newRating,
      })
      .then(() => {
        invalidateRecipeCaches()
        averageStars({ force: true })
      })
      .catch((error) => {
        alert(error.response?.data?.message || 'No se pudo guardar la valoración')
      })
  }
}

function averageStars({ force = false } = {}) {
  const cached = !force ? getAverageStarsCache() : null
  if (cached) applyAverages(cached)
  axios
    .post(apiUrl('/averageStars'))
    .then((response) => {
      const media = response.data.media || []
      setAverageStarsCache(media)
      applyAverages(media)
    })
    .catch((error) => {
      console.error('Error en la solicitud:', error)
    })
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.pager-btn {
  @apply inline-flex items-center justify-center px-3 py-2 rounded-full border border-amber-300 bg-white text-amber-900 text-sm font-medium hover:bg-amber-50 transition disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-white;
}
.pager-btn-active {
  @apply bg-amber-800 text-white border-amber-800 hover:bg-amber-900 hover:text-white;
}

:global(html.dark) .list-search,
:global(html.dark) .list-sort {
  background-color: #3d3128 !important;
  border-color: #6b5342 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .pager-btn {
  background-color: #3d3128 !important;
  border-color: #6b5342 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .pager-btn:hover:not(:disabled) {
  background-color: #4a3a2f !important;
}
:global(html.dark) .pager-btn-active {
  background-color: #d97706 !important;
  border-color: #d97706 !important;
  color: #2b211a !important;
}
</style>
