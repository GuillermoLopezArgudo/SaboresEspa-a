<template>
  <div class="min-h-screen bg-amber-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col hidden"
    ref="list">
    <div class="flex-1 flex flex-col justify-between" v-if="productos.length > 0">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="producto in paginatedRecipes" :key="producto.id"
          class="bg-amber-50 dark:bg-gray-800 rounded-xl overflow-hidden shadow-lg hover:shadow-xl  border border-amber-100 dark:border-gray-700 transform hover:-translate-y-1">
          <div class="p-5">
            <div class="relative">
              <img :src="producto.thumbnail" alt="Imagen del producto" className="rounded-lg" class="object-cover">
            </div>
            <p class="text-amber-600 dark:text-gray-300 text-sm mt-2">{{ producto.display_name }}</p>
            <p class="text-amber-600 dark:text-gray-300 text-sm mt-2">{{ producto.price_instructions?.bulk_price }} €
            </p>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap justify-center items-center mt-6 gap-2 text-sm sm:text-base">
        <button @click="currentPage--" :disabled="currentPage === 1"
          class="px-3 py-1 bg-amber-300/80 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-amber-400">
          Anterior
        </button>
        <span
          class="px-4 py-1 bg-white/80 dark:bg-gray-700/80 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-gray-600 rounded shadow-sm">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button @click="currentPage++" :disabled="currentPage === totalPages"
          class="px-3 py-1 bg-amber-300/80 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-amber-400/80">
          Siguiente
        </button>
      </div>
    </div>
    <div v-else class="text-center py-12 dark:bg-gray-900 m-4">
      <div class="max-w-md mx-auto">
        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-16 w-16 text-amber-400 dark:text-amber-500" fill="none"
          viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-amber-800 dark:text-amber-200">No existe/encuentra el producto
        </h3>
        <p class="mt-2 text-amber-600 dark:text-amber-400">Prueba con otro o informe al administrador!</p>
        <div class="mt-6">
          <router-link to="/contacto"
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Reporte el error
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <div ref="loading" class="flex flex-col items-center min-h-screen px-4 m-4">
    <div
      class="inline-block animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 md:h-16 md:w-16 border-t-2 border-b-2 border-amber-600 dark:border-amber-400">
    </div>
    <p class="mt-3 sm:mt-4 text-amber-700 dark:text-amber-300 text-sm sm:text-base md:text-lg text-center">Cargando
      recetas...</p>
  </div>
</template>

<script setup>
import { ingredientes } from '@/utils/ingredientes.js'
import axios from 'axios'
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const id = ref(0)
const productos = ref([])
const loading = ref("")
const list = ref("")
const timeStart = ref(0)
const timeEnd = ref(0)
const timeTotal = ref(0)
const route = useRoute()
const palabra = route.query.ingredients
const currentPage = ref(1);
const itemsPerPage = ref(6)

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
      console.log("Categorias:")
      console.log(response.data)
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



      console.log('Productos encontrados:', productos.value.length);
      console.log('Términos buscados:', searchTerms, 'Variantes:', searchVariants);

    } catch (err) {
      console.error("Error fetching products:", err);
    }
  };

  const cargarCategorias = async () => {
    try {
      const response = await fetch(`${process.env.VUE_APP_API_URL}/categories`)
      const data = await response.json()

      timeCharge();
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