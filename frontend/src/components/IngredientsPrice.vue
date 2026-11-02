<template>
  <div class="min-h-screen bg-amber-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto mb-6">
      <router-link
        to="/"
        class="inline-flex items-center px-4 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-lg transition"
      >
        ← Volver
      </router-link>
    </div>

    <div class="max-w-5xl mx-auto">
      <h1 class="text-3xl font-bold text-amber-800 font-serif mb-2">
        Precios Mercadona
      </h1>
      <p class="text-amber-700 mb-6">
        Buscando productos para:
        <span class="font-semibold">{{ ingredientLabel }}</span>
      </p>

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

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
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
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { apiUrl } from '../api'
import { resolveMercadonaCategory } from '../utils/ingredientes'

const route = useRoute()
const productos = ref([])
const loading = ref(true)
const error = ref('')
const categoryName = ref('')

const ingredientLabel = computed(() => {
  const q = route.query.ingredients
  return typeof q === 'string' ? q : Array.isArray(q) ? q[0] : ''
})

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

function variantsFor(word) {
  if (!word) return []
  const base = word.trim()
  const lower = base.toLowerCase()
  const capitalized = lower.charAt(0).toUpperCase() + lower.slice(1)
  const singular = lower.endsWith('s') ? lower.slice(0, -1) : lower
  return [...new Set([base, lower, capitalized, singular, singular + 's'])]
}

async function load() {
  loading.value = true
  error.value = ''
  productos.value = []
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
    let categoryId = null
    for (const group of cats.data.results || []) {
      for (const cat of group.categories || []) {
        if ((cat.name || '').includes(categoria) || categoria.includes(cat.name || '')) {
          categoryId = cat.id
          break
        }
      }
      if (categoryId) break
    }

    if (!categoryId) {
      error.value = `No se encontró la categoría "${categoria}" en Mercadona.`
      loading.value = false
      return
    }

    // Preferimos el endpoint optimizado del backend
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
      // fallback al endpoint legacy
    }

    const response = await axios.post(
      apiUrl('/productos'),
      { id: categoryId },
      { skipAuth: true }
    )
    const palabrasVariantes = variantsFor(palabra)
    const found = []
    for (const category of response.data.categories || []) {
      for (const product of category.products || []) {
        const name = (product.display_name || '').toLowerCase()
        if (palabrasVariantes.some((v) => name.includes(String(v).toLowerCase()))) {
          found.push(product)
        }
      }
    }
    productos.value = found
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
</script>
