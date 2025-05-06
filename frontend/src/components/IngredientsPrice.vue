<template>
  <div class="min-h-screen bg-amber-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col">
    <!-- Contenido cuando hay productos -->
    <div v-if="productos.length > 0" class="flex-1 flex flex-col justify-between p-4 hiden" ref="list">
      <!-- Grid de productos -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
        <div 
          v-for="producto in paginatedRecipes" 
          :key="producto.id"
          class="bg-white/80 dark:bg-gray-800 rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300 border border-amber-100 dark:border-gray-700 hover:-translate-y-1 transition-transform"
        >
          <div class="p-4 space-y-3">
            <div class="relative aspect-square overflow-hidden rounded-md">
              <img 
                :src="producto.thumbnail" 
                :alt="producto.display_name" 
                class="w-full h-full object-cover hover:scale-105 transition-transform"
              >
            </div>
            <h3 class="text-lg font-medium text-amber-800 dark:text-amber-200 line-clamp-2">
              {{ producto.display_name }}
            </h3>
            <p class="text-amber-600 dark:text-amber-400 font-semibold">
              {{ producto.price_instructions?.unit_price }} €
            </p>
          </div>
        </div>
      </div>

      <!-- Paginación -->
      <div class="flex justify-center items-center mt-8 gap-2">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-amber-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-amber-600 transition-colors flex items-center gap-1"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          Anterior
        </button>
        
        <span class="px-4 py-2 bg-white dark:bg-gray-700 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-gray-600 rounded-lg shadow-sm">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="px-4 py-2 bg-amber-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-amber-600 transition-colors flex items-center gap-1"
        >
          Siguiente
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Estado vacío -->
    <div v-else class="flex-1 flex items-center justify-center p-8">
      <div class="max-w-md text-center space-y-4">
        <div class="mx-auto w-16 h-16 text-amber-400 dark:text-amber-500">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-xl font-medium text-amber-800 dark:text-amber-200">
          No se encontraron productos
        </h3>
        <p class="text-amber-600 dark:text-amber-400">
          Intenta con otro término o contacta al administrador
        </p>
        <router-link 
          to="/contacto"
          class="inline-flex items-center px-4 py-2 mt-4 bg-amber-500 hover:bg-amber-600 text-white rounded-lg transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Reportar problema
        </router-link>
      </div>
    </div>

    <!-- Estado de carga -->
    <div 
      v-show="loading" 
      class="fixed inset-0 flex flex-col items-center justify-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-50"
      ref="loading">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500 dark:border-amber-400" ></div>
      <p class="mt-4 text-amber-700 dark:text-amber-300">Cargando productos...</p>
    </div>
  </div>
</template>

<script setup>
import { ingredientes } from '@/utils/ingredientes.js'
import axios from 'axios'
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const id = ref(0)
const productos = ref([])
const loading = ref(null)
const list = ref(null)
const timeStart = ref(0)
const timeEnd = ref(0)
const timeTotal = ref(0)
const route = useRoute()
const palabra = route.query.ingredients
const currentPage = ref(1);
const itemsPerPage = ref(8)

if (palabra && typeof palabra === 'string' && palabra.length > 0) {
  const palabrasVariantes = [
    palabra.charAt(0).toUpperCase() + palabra.slice(1),
    palabra.charAt(0).toUpperCase() + palabra.slice(1) + "s",
    palabra.toLowerCase(),
    palabra.toLowerCase() + "s"
  ];

  const producto = async () => {
    try {
      const response = await axios.post(`${process.env.VUE_APP_API_URL}/productos`, { id: id.value });
      timeCharge();
      const searchTerms = palabra.toLowerCase().split(' ');
      const searchVariants = palabrasVariantes.map(v => v.toLowerCase());

      const matchesSearch = (text) => {
        const normalizedText = text.toLowerCase();
        if (searchVariants.some(variant => normalizedText.includes(variant))) {
          return true;
        }

        return searchTerms.every(term => normalizedText.includes(term));
      };

      const uniqueProducts = new Map();

      response.data.categories?.forEach(category => {
        const categoryMatches = matchesSearch(category.name);

        category.products?.forEach(product => {
          if (categoryMatches || matchesSearch(product.display_name)) {
            if (!uniqueProducts.has(product.id)) {
              uniqueProducts.set(product.id, product);
            }
          }
        });
      });

      productos.value = Array.from(uniqueProducts.values());

    } catch (err) {
      console.error("Error fetching products:", err);
    }
  };

  const cargarCategorias = async () => {
    try {
      const response = await fetch(`${process.env.VUE_APP_API_URL}/categories`)
      timeCharge();
      const data = await response.json()
      const categoriasBuscadasRaw = ingredientes[palabrasVariantes[0]];
      const categoriasBuscadas = Array.isArray(categoriasBuscadasRaw)
        ? categoriasBuscadasRaw
        : [categoriasBuscadasRaw];
      data.results.forEach(element => {

        element.categories.forEach(cat => {
          if (categoriasBuscadas.some(c => cat.name.includes(c))) {
            id.value = cat.id
            if (id.value > 0) {
              producto()
            }
          }
        })
      })
    } catch (err) {
      console.error("Error fetching categories:", err)
    }
  }

  cargarCategorias()

} else {
  console.error('No se ha pasado un ingrediente válido en la URL.')
}

const timeCharge = () => {
  if (productos.value.length >= 0) {
    timeEnd.value = performance.now();
    timeTotal.value = timeEnd.value - timeStart.value;
    setTimeout(() => {
      loading.value.classList.add("hidden");
      list.value.classList.remove("hidden");
    }, timeTotal.value)
  } else {
    loading.value.classList.add("hidden");
    list.value.classList.remove("hidden");
  }
}

const paginatedRecipes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return productos.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(productos.value.length / itemsPerPage.value);
});


</script>