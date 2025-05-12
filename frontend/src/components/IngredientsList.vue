<template>
    <!-- Contenedor principal con modo noche -->
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300" @click="closeAllMenus">

        <!-- Categorías principales -->
        <div class="flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4">
            <div class="p-4" @click.stop>
                <!-- Hacer visible CascadeSelect en móviles y pantallas más grandes -->
                <CascadeSelect v-model="selectedCategory" :options="categorias" optionLabel="name"
                    optionGroupLabel="name" :optionGroupChildren="['categories', 'subcategories', 'subsubcategories']"
                    class="w-full sm:w-full md:w-96 lg:w-[450px] xl:w-[500px] dark:text-gray-200"
                    placeholder="Selecciona una categoría" @change="onCategorySelect"
                    panelClass="bg-white dark:bg-gray-800 dark:text-gray-200"
                    subpanelClass="bg-white dark:bg-gray-800 dark:text-gray-200" />
            </div>
        </div>

        <!-- Cards de productos -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 px-6 pb-10">
            <div v-for="product in paginatedRecipes" :key="product.id"
                class="bg-white/80 rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition-all dark:bg-gray-800 dark:hover:shadow-gray-700/50">
                <div class="relative aspect-square overflow-hidden">
                    <img :src="product.thumbnail" :alt="product.display_name"
                        class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                        loading="lazy" />
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold text-gray-800 mb-1 dark:text-gray-200">{{ product.display_name }}
                    </h3>
                    <p class="text-gray-600 dark:text-gray-400">{{ product.price_instructions?.unit_price }} €</p>
                </div>
            </div>
        </div>

        <!-- Paginación -->
        <div class="flex flex-wrap justify-center items-center mt-8 gap-4 pb-8" v-if="products.length > 0">
            <button @click="currentPage--" :disabled="currentPage === 1"
                class="flex items-center gap-2 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition disabled:opacity-50 disabled:cursor-not-allowed dark:bg-amber-600 dark:hover:bg-amber-700">
                Anterior
            </button>

            <span
                class="px-4 py-2 text-amber-800 font-medium bg-white/80 border border-amber-300 rounded-lg shadow-sm dark:bg-gray-800 dark:text-amber-300 dark:border-amber-600">
                Página {{ currentPage }} de {{ totalPages }}
            </span>

            <button @click="currentPage++" :disabled="currentPage === totalPages"
                class="flex items-center gap-2 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition disabled:opacity-50 disabled:cursor-not-allowed dark:bg-amber-600 dark:hover:bg-amber-700">
                Siguiente
            </button>
        </div>
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

const onCategorySelect = async (event) => {
    const response = await axios.post(`${process.env.VUE_APP_API_URL}/productos`, { id: event.value.id });
    subsubcategories.value = response.data.categories || [];

    products.value = [];
    subsubcategories.value.forEach(element => {
        prueba(element.products);
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

const prueba = (productsArray) => {
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

<style></style>
