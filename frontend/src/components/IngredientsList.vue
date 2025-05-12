<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300" @click="closeAllMenus" v-if="products.length > 0">
    
    <!-- Selector de Categorías -->
    <div class="flex justify-center bg-gray-100 dark:bg-gray-900 py-6 px-4">
      <div class="w-full max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl" @click.stop>
        <CascadeSelect
          v-model="selectedCategory"
          :options="categorias"
          optionLabel="name"
          id="cascade"
          optionGroupLabel="name"
          :optionGroupChildren="['categories', 'subcategories']"
          class="w-full dark:text-gray-200"
          placeholder="Selecciona una categoría"
          @change="onCategorySelect"
          panelClass="custom-panel bg-white/80 dark:bg-gray-800/80"
        />
      </div>
    </div>

    <!-- Grid de Productos -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 px-4 sm:px-6 pb-10">
      <div
        v-for="product in paginatedRecipes"
        :key="product.id"
        class="bg-white/80 dark:bg-gray-800 rounded-2xl shadow hover:shadow-lg transition overflow-hidden"
      >
        <div class="relative aspect-square overflow-hidden">
          <img
            :src="product.thumbnail"
            :alt="product.display_name"
            class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            loading="lazy"
          />
        </div>
        <div class="p-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-1">{{ product.display_name }}</h3>
          <p class="text-gray-600 dark:text-gray-400">{{ product.price_instructions?.unit_price }} €</p>
        </div>
      </div>
    </div>

    <!-- Paginación -->
    <div v-if="products.length > 0" class="flex flex-wrap justify-center items-center gap-4 mt-8 pb-8">
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition disabled:opacity-50 disabled:cursor-not-allowed dark:bg-amber-600 dark:hover:bg-amber-700"
      >
        Anterior
      </button>

      <span class="px-4 py-2 bg-white/80 border rounded-lg shadow-sm text-amber-800 font-medium dark:bg-gray-800 dark:text-amber-300 dark:border-amber-600">
        Página {{ currentPage }} de {{ totalPages }}
      </span>

      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition disabled:opacity-50 disabled:cursor-not-allowed dark:bg-amber-600 dark:hover:bg-amber-700"
      >
        Siguiente
      </button>
    </div>
  </div>
  <div v-show="loading" v-else
      class="fixed inset-0 flex flex-col items-center justify-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-50"
      ref="loading">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500 dark:border-amber-400">
      </div>
      <p class="mt-4 text-amber-700 dark:text-amber-300">Cargando productos...</p>
    </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
import CascadeSelect from 'primevue/cascadeselect';

const categorias = ref([])
const subcategories = ref([])
const subsubcategories = ref([])
const products = ref([])
const activeCategoryId = ref(null)
const activeSubcategoryId = ref(null)
const currentPage = ref(1);
const itemsPerPage = ref(8)
const router = useRouter();
const loading = ref(null)

const onCategorySelect = async (event) => {
    const response = await axios.post(`${process.env.VUE_APP_API_URL}/productos`, { id: event.value.id });
    subsubcategories.value = response.data.categories || [];

    products.value = [];
    subsubcategories.value.forEach(element => {
        productos(element.products);
    });

    closeAllMenus();
    currentPage.value = 1;
};

onMounted(async () => {
    if (localStorage.getItem('userToken')) {
        try {
            const response = await fetch(`${process.env.VUE_APP_API_URL}/categories`)
            const data = await response.json()
            categorias.value = data.results
            const allCategories = data.results.flatMap(item => item.categories || []);
            const randomCategory = allCategories[Math.floor(Math.random() * allCategories.length)];
            activeCategoryId.value = randomCategory.id;
            loadProductsFromCategory(activeCategoryId.value);
        } catch (e) {
            console.error(e)
        }
    } else {
        router.push({ name: 'login' });
        localStorage.removeItem('userToken')
    }
})

const closeAllMenus = () => {
    activeCategoryId.value = null
    activeSubcategoryId.value = null
    subcategories.value = []
    subsubcategories.value = []
}

const productos = (productsArray) => {
    if (!Array.isArray(productsArray)) return;
    products.value.push(...productsArray);
};

const loadProductsFromCategory = async (categoryId) => {
    try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/productos`, { id: categoryId });
        response.data.categories.forEach(element => {
            products.value = element.products || []
        });
    } catch (e) {
        console.error(e);
    }
};

const paginatedRecipes = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return products.value.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(products.value.length / itemsPerPage.value);
});
</script>

<style>
@media (max-width: 640px) {
  div.p-cascadeselect-mobile-active >div {
    top: auto !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    position: absolute !important;
    transform: none !important;
  }

   div.p-cascadeselect-overlay.p-cascadeselect-mobile-active > div {
    margin-top: 0 !important;
  }

  .p-cascadeselect {
        width: 100% !important;
        max-width: 500px;
        margin: 0 auto;
    }

    .p-cascadeselect-overlay {
        width: 50% !important;
    }

/*p-cascadeselect-list p-cascadeselect-overlay p-cascadeselect-option-list*/
}


.p-cascadeselect-option-content {
    background-color: white !important;
    color: black !important;
}

.p-cascadeselect-option-content:hover {
    background-color: #f3f4f6 !important;
    color: black !important;
}

/* Modo oscuro */
.dark .p-cascadeselect-option-content {
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
}

.dark .p-cascadeselect-option-content:hover {
    background-color: #374151 !important;
    color: #e5e7eb !important;
}

.p-cascadeselect-list > .p-cascadeselect-option > .p-cascadeselect-option-content{
    background-color: aqua;
}
.p-cascadeselect-option-content{
    background-color: aqua;
}

.p-cascadeselect-list {
    max-width: 300px;
}

</style>
