<template>
  <div>
    <PageHero
      :title="pageTitle"
      :subtitle="heroSubtitle"
      eyebrow="Precios"
    >
      <button type="button" class="hero-cta-ghost" @click="goBack">
        ← {{ fromRecipe ? 'Volver a la receta' : 'Volver al recetario' }}
      </button>
    </PageHero>

    <div class="max-w-6xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <!-- Buscador / filtros -->
      <form
        class="mb-6 rounded-2xl border border-amber-200 bg-white p-4 sm:p-5 shadow-sm space-y-3"
        @submit.prevent="onSearch"
      >
        <div class="grid grid-cols-1 sm:grid-cols-[1fr_minmax(0,14rem)_auto] gap-3">
          <label class="block min-w-0">
            <span class="sr-only">Buscar producto</span>
            <input
              v-model="searchInput"
              type="search"
              enterkeyhint="search"
              placeholder="Buscar producto o ingrediente…"
              class="w-full rounded-xl border border-amber-300 px-4 py-2.5 text-sm text-amber-950 placeholder:text-amber-700/40 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          <label class="block min-w-0">
            <span class="sr-only">Categoría</span>
            <select
              v-model="selectedCategoryId"
              class="w-full rounded-xl border border-amber-300 bg-white px-3 py-2.5 text-sm text-amber-950 focus:outline-none focus:ring-2 focus:ring-amber-500"
              @change="onCategoryChange"
            >
              <option value="">Todas las categorías</option>
              <option
                v-for="cat in flatCategories"
                :key="cat.id"
                :value="String(cat.id)"
              >
                {{ cat.name }}
              </option>
            </select>
          </label>
          <button
            type="submit"
            class="inline-flex items-center justify-center rounded-xl bg-amber-800 hover:bg-amber-900 text-white text-sm font-semibold px-5 py-2.5 transition"
            :disabled="loading"
          >
            Buscar
          </button>
        </div>
        <p class="text-xs text-amber-700/80">
          Precios orientativos de tienda online · pueden variar por zona
        </p>
      </form>

      <!-- Loading skeleton -->
      <div v-if="loading" class="space-y-5">
        <div class="h-10 w-64 rounded-full bg-amber-100 animate-pulse" />
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="n in 6"
            :key="'sk-' + n"
            class="rounded-2xl border border-amber-100 bg-white overflow-hidden animate-pulse"
          >
            <div class="h-44 bg-amber-50" />
            <div class="p-4 space-y-3">
              <div class="h-4 bg-amber-100 rounded w-4/5" />
              <div class="h-3 bg-amber-50 rounded w-1/2" />
              <div class="h-6 bg-amber-100 rounded w-1/3" />
            </div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="rounded-2xl border border-red-200 bg-red-50 px-5 py-6 text-red-800"
      >
        <p class="font-semibold">No se pudieron cargar los precios</p>
        <p class="mt-1 text-sm text-red-700/90">{{ error }}</p>
        <button
          type="button"
          class="mt-4 inline-flex px-4 py-2 rounded-full bg-red-700 text-white text-sm font-medium hover:bg-red-800 transition"
          @click="load"
        >
          Reintentar
        </button>
      </div>

      <!-- Idle: aún no hay búsqueda -->
      <div
        v-else-if="!hasQuery && !productos.length"
        class="rounded-2xl border border-amber-200 bg-white px-6 py-12 text-center"
      >
        <p class="font-serif text-xl font-bold text-amber-950">Explora el catálogo</p>
        <p class="mt-2 text-amber-800/80 max-w-md mx-auto text-sm">
          Escribe un producto o elige una categoría para ver precios orientativos.
        </p>
      </div>

      <!-- Empty results -->
      <div
        v-else-if="!productos.length"
        class="rounded-2xl border border-amber-200 bg-white px-6 py-12 text-center"
      >
        <p class="font-serif text-xl font-bold text-amber-950">Sin resultados</p>
        <p class="mt-2 text-amber-800/80 max-w-md mx-auto">
          No encontramos productos para
          <span class="font-semibold">{{ ingredientLabel || categoryName || 'esta búsqueda' }}</span>.
        </p>
      </div>

      <!-- Results -->
      <div v-else class="space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div class="flex flex-wrap items-center gap-2 text-sm">
            <span class="inline-flex items-center px-3 py-1.5 rounded-full bg-amber-900 text-amber-50 font-medium">
              {{ filteredProductos.length }} producto{{ filteredProductos.length === 1 ? '' : 's' }}
            </span>
            <span
              v-if="categoryName"
              class="inline-flex items-center px-3 py-1.5 rounded-full bg-amber-100 text-amber-900"
            >
              {{ categoryName }}
            </span>
            <span
              v-if="cheapest"
              class="inline-flex items-center px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200"
            >
              Desde {{ formatPrice(cheapest) }}
            </span>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <label class="inline-flex items-center gap-2 text-sm text-amber-900">
              <span class="text-amber-800/70 hidden sm:inline">Filtrar</span>
              <input
                v-model="localFilter"
                type="search"
                placeholder="Filtrar en resultados…"
                class="rounded-full border border-amber-300 bg-white px-3 py-1.5 text-sm w-40 sm:w-52 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </label>
            <label class="inline-flex items-center gap-2 text-sm text-amber-900">
              <span class="text-amber-800/70">Ordenar</span>
              <select
                v-model="sortBy"
                class="rounded-full border border-amber-300 bg-white px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              >
                <option value="price-asc">Precio: menor a mayor</option>
                <option value="price-desc">Precio: mayor a menor</option>
                <option value="name-asc">Nombre A–Z</option>
              </select>
            </label>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <article
            v-for="(p, idx) in sortedProductos"
            :key="p.id || p.display_name"
            class="group relative flex flex-col rounded-2xl border bg-white overflow-hidden shadow-sm hover:shadow-md transition"
            :class="isCheapest(p) ? 'border-emerald-300 ring-1 ring-emerald-200' : 'border-amber-200'"
          >
            <div
              v-if="isCheapest(p)"
              class="absolute top-3 left-3 z-[1] px-2.5 py-1 rounded-full bg-emerald-700 text-white text-[11px] font-semibold tracking-wide uppercase"
            >
              Más barato
            </div>

            <div class="h-44 bg-gradient-to-b from-amber-50 to-white flex items-center justify-center overflow-hidden px-4">
              <img
                v-if="p.thumbnail"
                :src="p.thumbnail"
                :alt="p.display_name"
                class="max-h-36 object-contain transition duration-300 group-hover:scale-105"
                loading="lazy"
              />
              <span v-else class="text-amber-400 text-sm">Sin imagen</span>
            </div>

            <div class="flex flex-1 flex-col p-4 pt-3">
              <h2 class="font-semibold text-amber-950 text-sm leading-snug line-clamp-2 min-h-[2.5rem]">
                {{ p.display_name }}
              </h2>

              <div class="mt-2 flex flex-wrap gap-1.5">
                <span
                  v-if="packagingLabel(p)"
                  class="inline-flex px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 text-[11px] border border-amber-100"
                >
                  {{ packagingLabel(p) }}
                </span>
                <span
                  v-if="unitLabel(p)"
                  class="inline-flex px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 text-[11px] border border-amber-100"
                >
                  {{ unitLabel(p) }}
                </span>
              </div>

              <div class="mt-auto pt-4 flex items-end justify-between gap-2">
                <div>
                  <p class="text-[11px] uppercase tracking-wide text-amber-700/70">Precio</p>
                  <p class="text-xl font-bold text-amber-900 tabular-nums">
                    {{ formatPrice(p) }}
                  </p>
                </div>
                <span class="text-[11px] text-amber-600/80">#{{ idx + 1 }}</span>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { apiUrl } from '../api'
import {
  normalizeText,
  resolveMercadonaCategory,
} from '../utils/ingredientes'
import PageHero from './PageHero.vue'

const route = useRoute()
const router = useRouter()
const productos = ref([])
const loading = ref(false)
const error = ref('')
const categoryName = ref('')
const sortBy = ref('price-asc')
const searchInput = ref('')
const localFilter = ref('')
const selectedCategoryId = ref('')
const flatCategories = ref([])
const categoriesRaw = ref(null)

const ingredientLabel = computed(() => {
  const q = route.query.ingredients || route.query.q
  return typeof q === 'string' ? q : Array.isArray(q) ? q[0] : ''
})

const fromRecipe = computed(() => Boolean(route.query.ingredients))

const hasQuery = computed(
  () => Boolean(ingredientLabel.value) || Boolean(selectedCategoryId.value)
)

const pageTitle = computed(() => {
  if (ingredientLabel.value) return ingredientLabel.value
  if (categoryName.value) return categoryName.value
  return 'Precios de productos'
})

const heroSubtitle = computed(() => {
  if (loading.value) return 'Consultando catálogo…'
  if (error.value) return 'Ha habido un problema al consultar precios'
  if (!hasQuery.value) return 'Busca o filtra por categoría'
  if (!productos.value.length) return 'Compara opciones de la tienda online'
  return `${filteredProductos.value.length} resultado${filteredProductos.value.length === 1 ? '' : 's'}`
})

function goBack() {
  if (window.history.length > 1) router.back()
  else router.push({ name: 'landing' })
}

function numericPrice(p) {
  const price =
    p?.price ??
    p?.bulk_price ??
    p?.price_instructions?.unit_price ??
    p?.price_instructions?.bulk_price
  const n = Number(price)
  return Number.isFinite(n) ? n : null
}

function formatPrice(p) {
  const n = numericPrice(p)
  if (n === null) return 'No disponible'
  return `${n.toFixed(2)} €`
}

function packagingLabel(p) {
  return p.packaging || ''
}

function unitLabel(p) {
  const size = p.unit_size ?? p.price_instructions?.unit_size
  const format = p.size_format ?? p.price_instructions?.size_format
  if (size == null || size === '') return ''
  return format ? `${size} ${format}` : String(size)
}

const filteredProductos = computed(() => {
  const q = normalizeText(localFilter.value)
  if (!q) return productos.value
  return productos.value.filter((p) =>
    normalizeText(p.display_name || '').includes(q)
  )
})

const cheapest = computed(() => {
  let best = null
  let bestPrice = Infinity
  for (const p of filteredProductos.value) {
    const n = numericPrice(p)
    if (n === null) continue
    if (n < bestPrice) {
      bestPrice = n
      best = p
    }
  }
  return best
})

function isCheapest(p) {
  const c = cheapest.value
  if (!c) return false
  return (p.id && c.id && p.id === c.id) || p.display_name === c.display_name
}

const sortedProductos = computed(() => {
  const list = [...filteredProductos.value]
  if (sortBy.value === 'name-asc') {
    return list.sort((a, b) =>
      String(a.display_name || '').localeCompare(String(b.display_name || ''), 'es')
    )
  }
  const dir = sortBy.value === 'price-desc' ? -1 : 1
  return list.sort((a, b) => {
    const pa = numericPrice(a)
    const pb = numericPrice(b)
    if (pa === null && pb === null) return 0
    if (pa === null) return 1
    if (pb === null) return -1
    return (pa - pb) * dir
  })
})

function findCategoryId(results, categoria) {
  const target = normalizeText(categoria)
  let fuzzy = null
  for (const group of results || []) {
    for (const cat of group.categories || []) {
      const name = normalizeText(cat.name)
      if (name === target) return cat.id
      if (!fuzzy && (name.includes(target) || target.includes(name))) {
        fuzzy = cat.id
      }
    }
  }
  return fuzzy
}

function flattenCategories(results) {
  const out = []
  for (const group of results || []) {
    for (const cat of group.categories || []) {
      if (cat?.id && cat?.name) out.push({ id: cat.id, name: cat.name })
    }
  }
  return out.sort((a, b) => a.name.localeCompare(b.name, 'es'))
}

function collectAllProducts(payload) {
  const found = []
  const seen = new Set()
  for (const category of payload?.categories || []) {
    for (const product of category.products || []) {
      const key = product.id || product.display_name
      if (!key || seen.has(key)) continue
      seen.add(key)
      found.push(product)
    }
  }
  return found
}

async function ensureCategories() {
  if (categoriesRaw.value) return categoriesRaw.value
  const cats = await axios.get(apiUrl('/categories'), { skipAuth: true })
  categoriesRaw.value = cats.data
  flatCategories.value = flattenCategories(cats.data.results)
  return cats.data
}

function onSearch() {
  const q = searchInput.value.trim()
  const query = {}
  if (q) {
    // Nueva búsqueda por texto: no arrastrar la categoría anterior
    // (se infiere otra vez con el mapeo de ingredientes).
    query.q = q
  } else if (selectedCategoryId.value) {
    query.category = selectedCategoryId.value
  }
  const name = route.name === 'ingredients' ? 'ingredients' : 'precios'
  router.replace({ name, query })
}

function onCategoryChange() {
  const q = searchInput.value.trim()
  const query = {}
  if (q) query.q = q
  if (selectedCategoryId.value) query.category = selectedCategoryId.value
  const name = route.name === 'ingredients' ? 'ingredients' : 'precios'
  router.replace({ name, query })
}

async function loadByCategoryId(categoryId, filterText = '') {
  const response = await axios.post(
    apiUrl('/productos'),
    { id: categoryId },
    { skipAuth: true }
  )
  const all = collectAllProducts(response.data)
  if (filterText) {
    const q = normalizeText(filterText)
    productos.value = all.filter((p) =>
      normalizeText(p.display_name || '').includes(q)
    )
  } else {
    productos.value = all
  }
  const hit = flatCategories.value.find((c) => String(c.id) === String(categoryId))
  categoryName.value = hit?.name || ''
}

async function load() {
  loading.value = true
  error.value = ''
  productos.value = []
  categoryName.value = ''

  const palabra = ingredientLabel.value
  const catFromUrl =
    typeof route.query.category === 'string' ? route.query.category : ''

  searchInput.value = palabra || searchInput.value
  if (catFromUrl) selectedCategoryId.value = catFromUrl

  try {
    await ensureCategories()

    if (!palabra && !selectedCategoryId.value) {
      loading.value = false
      return
    }

    if (palabra) {
      // Búsqueda global en catálogo (no limita a una sola categoría)
      const categoria = resolveMercadonaCategory(palabra)
      let categoryId = selectedCategoryId.value
        ? Number(selectedCategoryId.value)
        : null

      // Sugerencia suave de categoría en el select (no bloquea resultados)
      if (!categoryId && categoria) {
        const mapped = findCategoryId(categoriesRaw.value.results, categoria)
        if (mapped) {
          categoryId = mapped
          selectedCategoryId.value = String(mapped)
          categoryName.value = categoria
        }
      } else if (categoryId) {
        const hit = flatCategories.value.find(
          (c) => String(c.id) === String(categoryId)
        )
        categoryName.value = hit?.name || ''
      }

      const payload = { q: palabra }
      if (categoryId) payload.category_id = categoryId

      const search = await axios.post(apiUrl('/searchIngredient'), payload, {
        skipAuth: true,
      })
      productos.value = search.data.products || []
      loading.value = false
      return
    }

    // Solo categoría (sin texto)
    await loadByCategoryId(selectedCategoryId.value)
  } catch (err) {
    console.error(err)
    error.value =
      err.response?.data?.error ||
      'No se pudieron consultar los precios. Inténtalo más tarde.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    await ensureCategories()
  } catch {
    /* load() también lo intentará */
  }
  await load()
})

watch(
  () => [route.query.ingredients, route.query.q, route.query.category],
  () => {
    load()
  }
)
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
