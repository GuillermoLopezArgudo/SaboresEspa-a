<template>
  <div>
    <PageHero
      title="Precios Mercadona"
      :subtitle="ingredientLabel ? `Productos para: ${ingredientLabel}` : 'Consulta precios de ingredientes'"
    >
      <button
        type="button"
        class="inline-flex items-center px-4 py-2 rounded-full bg-white/15 hover:bg-white/25 text-white text-sm font-medium border border-white/20 transition"
        @click="goBack"
      >
        ← Volver
      </button>
    </PageHero>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="text-amber-700 animate-pulse">
        Consultando la tienda de Mercadona…
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">
        {{ error }}
      </div>

      <div v-else-if="productos.length === 0" class="bg-white border border-amber-200 rounded-xl p-6 text-amber-700">
        No se han encontrado productos para este ingrediente.
        <p v-if="categoryName" class="text-sm mt-2 text-amber-600">
          Categoría usada: {{ categoryName }}
        </p>
      </div>

      <div v-else>
        <p class="text-sm text-amber-800/80 mb-4">
          {{ productos.length }} producto{{ productos.length === 1 ? '' : 's' }}
          <span v-if="categoryName"> · {{ categoryName }}</span>
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <article
            v-for="p in productos"
            :key="p.id || p.display_name"
            class="bg-white rounded-xl border border-amber-200 shadow-sm overflow-hidden hover:shadow-md transition"
          >
            <div class="h-40 bg-amber-50 flex items-center justify-center overflow-hidden">
              <img
                v-if="p.thumbnail"
                :src="p.thumbnail"
                :alt="p.display_name"
                class="max-h-full object-contain"
              />
              <span v-else class="text-amber-400 text-sm">Sin imagen</span>
            </div>
            <div class="p-4">
              <h2 class="font-semibold text-amber-900 text-sm leading-snug">
                {{ p.display_name }}
              </h2>
              <p v-if="p.packaging" class="text-xs text-amber-600 mt-1">{{ p.packaging }}</p>
              <p class="mt-3 text-lg font-bold text-amber-700">
                {{ formatPrice(p) }}
              </p>
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
  textMatchesIngredient,
} from '../utils/ingredientes'
import PageHero from './PageHero.vue'

const route = useRoute()
const router = useRouter()
const productos = ref([])
const loading = ref(true)
const error = ref('')
const categoryName = ref('')

const ingredientLabel = computed(() => {
  const q = route.query.ingredients
  return typeof q === 'string' ? q : Array.isArray(q) ? q[0] : ''
})

function goBack() {
  if (window.history.length > 1) router.back()
  else router.push({ name: 'landing' })
}

function formatPrice(p) {
  const price =
    p.price ??
    p.bulk_price ??
    p.price_instructions?.unit_price ??
    p.price_instructions?.bulk_price
  if (price === undefined || price === null || price === '') return 'Precio no disponible'
  const n = Number(price)
  if (Number.isNaN(n)) return `${price} €`
  return `${n.toFixed(2)} €`
}

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

function collectProducts(payload, palabra) {
  const found = []
  const seen = new Set()
  for (const category of payload?.categories || []) {
    for (const product of category.products || []) {
      if (!textMatchesIngredient(product.display_name, palabra)) continue
      const key = product.id || product.display_name
      if (seen.has(key)) continue
      seen.add(key)
      found.push(product)
    }
  }
  return found
}

async function load() {
  loading.value = true
  error.value = ''
  productos.value = []
  categoryName.value = ''
  const palabra = ingredientLabel.value
  if (!palabra) {
    error.value = 'No se ha indicado un ingrediente.'
    loading.value = false
    return
  }

  try {
    const categoria = resolveMercadonaCategory(palabra)
    if (!categoria) {
      error.value =
        'No tenemos mapeada una categoría de Mercadona para este ingrediente.'
      loading.value = false
      return
    }
    categoryName.value = categoria

    const cats = await axios.get(apiUrl('/categories'), { skipAuth: true })
    const categoryId = findCategoryId(cats.data.results, categoria)

    if (!categoryId) {
      error.value = `No se encontró la categoría "${categoria}" en Mercadona.`
      loading.value = false
      return
    }

    try {
      const search = await axios.post(
        apiUrl('/searchIngredient'),
        { q: palabra, category_id: categoryId },
        { skipAuth: true }
      )
      if (search.data.products?.length) {
        productos.value = search.data.products
        loading.value = false
        return
      }
    } catch {
      // fallback
    }

    const response = await axios.post(
      apiUrl('/productos'),
      { id: categoryId },
      { skipAuth: true }
    )
    productos.value = collectProducts(response.data, palabra)
  } catch (err) {
    console.error(err)
    error.value =
      err.response?.data?.error ||
      'No se pudo consultar Mercadona. Inténtalo más tarde.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => route.query.ingredients, load)
</script>
