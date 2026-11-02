<template>
    <!-- Skeleton mientras carga la primera vez -->
    <div v-if="loading && !elementos.recetas.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="n in 6" :key="'sk-' + n" class="bg-white rounded-xl overflow-hidden border border-amber-100 animate-pulse">
            <div class="h-48 bg-amber-100" />
            <div class="p-5 space-y-3">
                <div class="h-5 bg-amber-100 rounded w-3/4" />
                <div class="h-4 bg-amber-50 rounded w-full" />
                <div class="h-4 bg-amber-50 rounded w-2/3" />
                <div class="h-10 bg-amber-100 rounded" />
            </div>
        </div>
    </div>

    <!-- Listado de recetas -->
    <div v-else-if="elementos.recetas.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(item) in elementos.recetas" :key="item.id"
            class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 border border-amber-100 transform hover:-translate-y-1">
            <div class="relative">
                <div class="absolute top-3 left-3 bg-amber-600 text-white rounded-full px-3 py-1 text-sm z-[1]">
                    {{ average[item.id] !== undefined && average[item.id] !== null ? Number(average[item.id]).toFixed(2)
                        : "Sin calificación" }} ★
                </div>

                <img v-if="item.image" :src="mediaUrl(item.image)" class="w-full h-48 object-cover"
                    alt="" loading="lazy" decoding="async">
                <div v-else class="h-48 bg-amber-200 flex items-center justify-center text-amber-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                            d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                </div>

                <button v-if="props.greeting !== 'personal'" @click="toggleFavorite(item.id)"
                    class="absolute top-3 right-3 p-2 bg-white bg-opacity-80 rounded-full shadow-md hover:bg-opacity-100 transition-all duration-300 transform hover:scale-110">
                    <i class="fa text-2xl"
                        :class="isFavorite(item.id) ? 'fa-heart text-red-500' : 'fa-heart-o text-amber-600'"></i>
                </button>
            </div>

            <div class="p-5">
                <h3 class="text-xl font-bold text-amber-800 font-serif line-clamp-1">{{ item.title }}</h3>
                <p v-if="item.author" class="mt-1 text-xs font-medium text-amber-800/70">
                    Por {{ item.author }}
                </p>
                <p class="text-amber-600 text-sm mt-2 line-clamp-2">{{ item.description }}</p>
                <div class="mt-4 pt-4 border-t border-amber-100" v-if="props.greeting != 'personal'">
                    <StarRating :rating="ratings[item.id] || 0" :onRatingChanged="ratingChanged(item.id)" />
                </div>

                <router-link :to="'/recipe?id=' + item.id"
                    class="inline-flex items-center justify-center w-full px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg font-medium hover:from-amber-600 hover:to-amber-700 transition duration-300 shadow-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    Ver Receta
                </router-link>

                <div class="text-sm text-amber-700 mt-2">
                    <span class="font-semibold">Categorías:</span>
                    <template v-if="(catsByRecipe[item.id] || []).length">
                        <span v-for="cat in catsByRecipe[item.id]"
                            :key="cat.type + cat.category"
                            class="inline-block bg-amber-100 text-amber-800 px-2 py-1 rounded-full text-xs mr-1 mb-1">
                            {{ cat.type }}
                        </span>
                    </template>
                    <span v-else class="text-amber-500 italic">No tiene categorías</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Mensaje si no hay recetas -->
    <div v-else-if="!loading" class="text-center py-12">
        <div class="max-w-md mx-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-16 w-16 text-amber-400" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>

            <!-- Mensaje para "all" -->
            <div v-if="props.greeting === 'all'">
                <h3 class="mt-4 text-lg font-medium text-amber-800">No hay recetas disponibles</h3>
                <p class="mt-2 text-amber-600">Parece que aún no hay recetas. ¡Sé el primero en compartir una!</p>
                <div class="mt-6">
                    <router-link to="/create"
                        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500">
                        <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        Crear nueva receta
                    </router-link>
                </div>
            </div>

            <!-- Mensaje para "favs" -->
            <div v-else-if="props.greeting === 'favs'">
                <h3 class="mt-4 text-lg font-medium text-amber-800">No tienes recetas favoritas</h3>
                <p class="mt-2 text-amber-600">Añade recetas a tus favoritos para encontrarlas fácilmente más tarde.</p>
                <div class="mt-6">
                    <router-link to="/"
                        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500">
                        <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                        Explorar recetas
                    </router-link>
                </div>
            </div>

            <!-- Mensaje para "personal" -->
            <div v-else-if="props.greeting === 'personal'">
                <h3 class="mt-4 text-lg font-medium text-amber-800">No has creado ninguna receta</h3>
                <p class="mt-2 text-amber-600">Comparte tus creaciones culinarias con la comunidad.</p>
                <div class="mt-6">
                    <router-link to="/create"
                        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500">
                        <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        Crear mi primera receta
                    </router-link>
                </div>
            </div>
            <!-- Mensaje para "filtred" -->
            <div v-else>
                <h3 class="mt-4 text-lg font-medium text-amber-800">No hay recetas que coincidan con tu filtro</h3>
                <p class="mt-2 text-amber-600">Intenta ajustar los filtros para encontrar lo que buscas.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted } from 'vue';
import StarRating from './StarRating.vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { apiUrl, mediaUrl } from '../api';
import {
    getAverageStarsCache,
    getViewAllCache,
    invalidateRecipeCaches,
    setAverageStarsCache,
    setViewAllCache,
} from '../utils/recipeCache';

const favoritos = reactive({});
const ratings = reactive({});
const average = reactive({});
const userToken = localStorage.getItem('userToken');
const iduser = localStorage.getItem('iduser');
const router = useRouter();
const elementos = reactive({
    recetas: []
});
const categorias = reactive([]);
const loading = ref(false);

function setCategories(list) {
    categorias.splice(0, categorias.length, ...(list || []))
}

const catsByRecipe = computed(() => {
    const map = Object.create(null);
    for (const cat of categorias) {
        const id = cat.recipe_id;
        if (!map[id]) map[id] = [];
        map[id].push(cat);
    }
    return map;
});

/** Ignora respuestas obsoletas si el usuario cambió de modo / re-filtró. */
let loadGen = 0

const props = defineProps({
    greeting: {
        type: String,
        required: true
    },
    filterCriteria: {
        type: Object,
        default: null,
    },
});

watch(
    () => [props.greeting, props.filterCriteria],
    () => {
        if (props.greeting === 'filtred') {
            applyLocalFilter()
        } else if (props.greeting === 'all') {
            allRecipes()
        }
    },
    { deep: true }
)

function selectFavorites(favorites_list) {
    Object.keys(favoritos).forEach((k) => { delete favoritos[k] })
    ;(favorites_list || []).forEach(recipe => {
        const recipeId = recipe.id_recipe || recipe.id;
        favoritos[recipeId] = true;
    });
}

function selectReviews(reviews_list) {
    Object.keys(ratings).forEach((k) => { delete ratings[k] })
    ;(reviews_list || []).forEach(recipe => {
        ratings[recipe.id_recipe] = recipe.review;
    });
}

function applyViewAllPayload(data) {
    elementos.recetas = data.recipes_list || [];
    selectFavorites(data.favorites_list || [])
    selectReviews(data.reviews_list || [])
    setCategories(data.categories_list)
}

function applyAverages(media) {
    ;(media || []).forEach(rating => {
        average[rating.recipe_id] = rating.average_rating
    });
}

onMounted(() => {
    if (props.greeting === "all") {
        allRecipes()
    } else if (props.greeting === "favs") {
        favoritesRecipes()
    } else if (props.greeting === "personal") {
        personalRecipes()
    }
    averageStars();
});


function allRecipes({ force = false } = {}) {
    const cached = !force ? getViewAllCache() : null
    if (cached) {
        applyViewAllPayload(cached)
        loading.value = false
    } else if (!elementos.recetas.length) {
        loading.value = true
    }

    const gen = ++loadGen
    axios.post(apiUrl('/viewAll'), {})
        .then(response => {
            if (gen !== loadGen) return
            const data = response.data || {}
            setViewAllCache(data)
            applyViewAllPayload(data)
        })
        .catch(error => {
            if (gen !== loadGen) return
            if (!elementos.recetas.length) {
                console.error("Error en la solicitud:", error);
                alert(error.response?.data?.message || 'No se pudieron cargar las recetas');
            }
        })
        .finally(() => {
            if (gen === loadGen) loading.value = false
        });
}

function favoritesRecipes() {
    if (!userToken) {
        router.push({ name: "login" });
        return;
    }
    if (!elementos.recetas.length) loading.value = true
    const gen = ++loadGen
    axios
        .post(apiUrl('/viewFavs'), {})
        .then(response => {
            if (gen !== loadGen) return
            elementos.recetas = response.data.favorites_list || [];
            selectFavorites(response.data.favorites_list || [])
            selectReviews(response.data.reviews_list || [])
            setCategories(response.data.categories_list)
        })
        .catch(error => {
            if (gen !== loadGen) return
            console.error("Error en la solicitud:", error);
            alert(error.response?.data?.message || 'No se pudieron cargar favoritos');
        })
        .finally(() => {
            if (gen === loadGen) loading.value = false
        });
}

function personalRecipes() {
    if (!userToken) {
        router.push({ name: "login" });
        return;
    }
    if (!elementos.recetas.length) loading.value = true
    const gen = ++loadGen
    axios.post(apiUrl('/viewRecipes'), {})
        .then(response => {
            if (gen !== loadGen) return
            elementos.recetas = response.data.message || [];
            setCategories(response.data.categories_list)
        })
        .catch(error => {
            if (gen !== loadGen) return
            console.error("Error al obtener las recetas:", error);
            alert(error.response?.data?.message || 'No se pudieron cargar tus recetas');
        })
        .finally(() => {
            if (gen === loadGen) loading.value = false
        });
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

    const matched = recipes.filter((r) => recipeMatchesCriteria(r.id, catsById, criteria))
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
    axios.post(apiUrl('/viewAll'), {})
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

// Cambiar el estado de favoritos
const toggleFavorite = (id) => {
    if (!userToken) {
        router.push({ name: "login" });
        return;
    }
    const payload = { idrecipe: id };
    if (favoritos[id]) {
        favoritos[id] = false;
        invalidateRecipeCaches();
        axios.post(apiUrl('/deleteFavs'), payload).catch((error) => {
            favoritos[id] = true;
            alert(error.response?.data?.message || 'No se pudo quitar de favoritos');
        });
    } else {
        favoritos[id] = true;
        invalidateRecipeCaches();
        axios.post(apiUrl('/updateFavs'), payload).catch((error) => {
            favoritos[id] = false;
            alert(error.response?.data?.message || 'No se pudo añadir a favoritos');
        });
    }
};

// Comprobar si una receta es favorita
const isFavorite = (id) => {
    return favoritos[id] || false;
};

// Función para cambiar la calificación de una receta (siempre callback válido)
const ratingChanged = (recipeId) => {
    return (newRating) => {
        if (!userToken) {
            router.push({ name: 'login' });
            return;
        }
        ratings[recipeId] = newRating;
        axios.post(apiUrl('/updateRating'), {
            idrecipe: recipeId,
            rating: newRating,
        })
            .then(() => {
                invalidateRecipeCaches();
                averageStars({ force: true });
            })
            .catch((error) => {
                alert(error.response?.data?.message || 'No se pudo guardar la valoración');
            });
    };
};

function averageStars({ force = false } = {}) {
    const cached = !force ? getAverageStarsCache() : null
    if (cached) {
        applyAverages(cached)
    }
    axios.post(apiUrl('/averageStars'))
        .then(response => {
            const media = response.data.media || []
            setAverageStarsCache(media)
            applyAverages(media)
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
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