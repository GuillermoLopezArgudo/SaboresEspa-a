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
          class="w-full rounded-full border border-amber-200 bg-white pl-10 pr-4 py-2.5 text-sm text-amber-950 placeholder:text-amber-700/50 shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
        />
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <span
          class="inline-flex items-center px-3 py-1.5 rounded-full bg-amber-900 text-amber-50 text-sm font-medium"
        >
          {{ visibleRecipes.length }}
          receta{{ visibleRecipes.length === 1 ? '' : 's' }}
        </span>
        <label class="inline-flex items-center gap-2 text-sm text-amber-900">
          <span class="text-amber-800/70 hidden sm:inline">Ordenar</span>
          <select
            v-model="sortBy"
            class="rounded-full border border-amber-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
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

          <img
            v-if="item.image"
            :src="mediaUrl(item.image)"
            :alt="item.title"
            class="w-full h-44 sm:h-52 object-cover transition duration-500 group-hover:scale-105"
            loading="lazy"
            decoding="async"
          />
          <div
            v-else
            class="h-44 sm:h-52 bg-gradient-to-br from-amber-100 to-amber-200 flex items-center justify-center text-amber-700/70"
          >
            <span class="font-serif text-lg">Sin imagen</span>
          </div>
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

    <!-- Sin resultados de búsqueda (hay recetas base) -->
    <div
      v-else-if="!loading && elementos.recetas.length && !visibleRecipes.length"
      class="rounded-2xl border border-amber-200 bg-white px-6 py-12 text-center"
    >
      <p class="font-serif text-xl font-bold text-amber-950">Sin coincidencias</p>
      <p class="mt-2 text-amber-800/80">
        No hay recetas para “{{ searchQuery }}”. Prueba otro término.
      </p>
      <button
        type="button"
        class="mt-5 inline-flex px-4 py-2 rounded-full border border-amber-300 text-amber-900 text-sm font-medium hover:bg-amber-50"
        @click="searchQuery = ''"
      >
        Limpiar búsqueda
      </button>
    </div>

    <!-- Vacío real -->
    <div
      v-else-if="!loading"
      class="rounded-2xl border border-amber-200 bg-white px-6 py-14 text-center"
    >
      <p class="font-serif text-2xl font-bold text-amber-950">
        {{ emptyTitle }}
      </p>
      <p class="mt-2 text-amber-800/80 max-w-md mx-auto">
        {{ emptySubtitle }}
      </p>
      <div class="mt-6">
        <router-link
          v-if="emptyLink"
          :to="emptyLink.to"
          class="inline-flex items-center px-5 py-2.5 rounded-full bg-amber-800 hover:bg-amber-900 text-white text-sm font-semibold transition"
        >
          {{ emptyLink.label }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted } from 'vue'
import StarRating from './StarRating.vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { apiUrl, mediaUrl } from '../api'
import {
  getAverageStarsCache,
  getViewAllCache,
  invalidateRecipeCaches,
  setAverageStarsCache,
  setViewAllCache,
} from '../utils/recipeCache'
import { labelForFilter } from '../utils/filterOptions'

const emit = defineEmits(['seleccionarCategoria'])

const favoritos = reactive({})
const ratings = reactive({})
const average = reactive({})
const userToken = localStorage.getItem('userToken')
const router = useRouter()
const elementos = reactive({ recetas: [] })
const categorias = reactive([])
const loading = ref(false)
const searchQuery = ref('')
const sortBy = ref('rating-desc')

const MAX_CATS = 3
const expandedCats = reactive({})

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
})

const showToolbar = computed(
  () => loading.value || elementos.recetas.length > 0 || searchQuery.value
)

const visibleRecipes = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  let list = [...elementos.recetas]
  if (q) {
    list = list.filter((r) => {
      const hay = `${r.title || ''} ${r.author || ''} ${r.description || ''}`.toLowerCase()
      return hay.includes(q)
    })
  }
  if (sortBy.value === 'title-asc') {
    return list.sort((a, b) =>
      String(a.title || '').localeCompare(String(b.title || ''), 'es')
    )
  }
  if (sortBy.value === 'author-asc') {
    return list.sort((a, b) =>
      String(a.author || '').localeCompare(String(b.author || ''), 'es')
    )
  }
  // rating-desc
  return list.sort((a, b) => {
    const ra = Number(average[a.id])
    const rb = Number(average[b.id])
    const na = Number.isFinite(ra) ? ra : -1
    const nb = Number.isFinite(rb) ? rb : -1
    return nb - na
  })
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
    if (props.greeting === 'filtred') applyLocalFilter()
    else if (props.greeting === 'all') allRecipes()
  },
  { deep: true }
)

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

function applyViewAllPayload(data) {
  elementos.recetas = data.recipes_list || []
  selectFavorites(data.favorites_list || [])
  selectReviews(data.reviews_list || [])
  setCategories(data.categories_list)
}

function applyAverages(media) {
  ;(media || []).forEach((rating) => {
    average[rating.recipe_id] = rating.average_rating
  })
}

onMounted(() => {
  if (props.greeting === 'all') allRecipes()
  else if (props.greeting === 'favs') favoritesRecipes()
  else if (props.greeting === 'personal') personalRecipes()
  else if (props.greeting === 'filtred') applyLocalFilter()
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

function allRecipes({ force = false } = {}) {
  const cached = !force ? getViewAllCache() : null
  if (cached) {
    applyViewAllPayload(cached)
    loading.value = false
  } else if (!elementos.recetas.length) {
    loading.value = true
  }

  const gen = ++loadGen
  axios
    .post(apiUrl('/viewAll'), {})
    .then((response) => {
      if (gen !== loadGen) return
      const data = response.data || {}
      setViewAllCache(data)
      applyViewAllPayload(data)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      if (!elementos.recetas.length) {
        console.error('Error en la solicitud:', error)
        alert(error.response?.data?.message || 'No se pudieron cargar las recetas')
      }
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
  if (!elementos.recetas.length) loading.value = true
  const gen = ++loadGen
  axios
    .post(apiUrl('/viewFavs'), {})
    .then((response) => {
      if (gen !== loadGen) return
      elementos.recetas = response.data.favorites_list || []
      selectFavorites(response.data.favorites_list || [])
      selectReviews(response.data.reviews_list || [])
      setCategories(response.data.categories_list)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error en la solicitud:', error)
      alert(error.response?.data?.message || 'No se pudieron cargar favoritos')
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
  if (!elementos.recetas.length) loading.value = true
  const gen = ++loadGen
  axios
    .post(apiUrl('/viewRecipes'), {})
    .then((response) => {
      if (gen !== loadGen) return
      elementos.recetas = response.data.message || []
      setCategories(response.data.categories_list)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error al obtener las recetas:', error)
      alert(error.response?.data?.message || 'No se pudieron cargar tus recetas')
    })
    .finally(() => {
      if (gen === loadGen) loading.value = false
    })
}

function recipeMatchesCriteria(recipeId, catsById, criteria) {
  if (!criteria) return true
  const cats = catsById.get(recipeId) || []
  const has = (category, type) =>
    cats.some((c) => c.category === category && c.type === type)

  if (criteria.typeeat && !has('typeeat', criteria.typeeat)) return false
  if (criteria.ccaa && !has('ccaa', criteria.ccaa)) return false
  if (criteria.time && !has('time', criteria.time)) return false

  const proteins = Array.isArray(criteria.proteins) ? criteria.proteins : []
  for (const protein of proteins) {
    if (protein && !has('protein', protein)) return false
  }
  return true
}

function filterPayload(data, criteria) {
  const recipes = data.recipes_list || []
  const categories = data.categories_list || []
  const catsById = new Map()
  for (const cat of categories) {
    const id = cat.recipe_id
    if (!catsById.has(id)) catsById.set(id, [])
    catsById.get(id).push(cat)
  }

  const matched = recipes.filter((r) =>
    recipeMatchesCriteria(r.id, catsById, criteria)
  )
  const matchedIds = new Set(matched.map((r) => r.id))

  elementos.recetas = matched
  selectFavorites(data.favorites_list || [])
  selectReviews(data.reviews_list || [])
  setCategories(categories.filter((c) => matchedIds.has(c.recipe_id)))
}

function applyLocalFilter() {
  const criteria = props.filterCriteria
  if (!criteria) {
    allRecipes()
    return
  }

  const cached = getViewAllCache()
  if (cached) {
    loadGen += 1
    filterPayload(cached, criteria)
    loading.value = false
    return
  }

  loading.value = true
  const gen = ++loadGen
  axios
    .post(apiUrl('/viewAll'), {})
    .then((response) => {
      if (gen !== loadGen) return
      const data = response.data || {}
      setViewAllCache(data)
      filterPayload(data, criteria)
    })
    .catch((error) => {
      if (gen !== loadGen) return
      console.error('Error en la solicitud:', error)
      alert(error.response?.data?.message || 'No se pudieron filtrar las recetas')
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
</style>
