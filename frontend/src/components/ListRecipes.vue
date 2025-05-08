<template>
    <div class="min-h-screen bg-amber-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col hidden"
        ref="list">
        <!-- Contenido principal -->
        <div v-if="elementos.recetas.length > 0" class="flex-1 flex flex-col justify-between">
            <!-- Grid de recetas -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="item in paginatedRecipes" :key="item.id"
                    class="bg-white-0 dark:bg-gray-800 rounded-xl overflow-hidden shadow-lg hover:shadow-xl  border border-amber-100 dark:border-gray-700 transform hover:-translate-y-1">

                    <!-- Imagen con calificación y botón de favorito -->
                    <div class="relative">
                        <router-link :to="'/recipe?id=' + item.id"  @click="idRecipe = item.id">
                            <div class="absolute top-3 left-3 bg-amber-600 text-white rounded-full px-3 py-1 text-sm">
                                {{ average[item.id] !== undefined && average[item.id] !== null ?
                                    Number(average[item.id]).toFixed(2) : "Sin calificación" }} ★
                            </div>
                            <img v-if="item.image" :src="`http://48.217.185.80/api/${item.image}`"
                                class="w-full h-48 object-cover" alt="Imagen de receta">
                            <div v-else
                                class="h-48 bg-amber-200 dark:bg-gray-700 flex items-center justify-center text-amber-600 dark:text-gray-300">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                                        d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                </svg>
                            </div>
                        </router-link>

                        <button v-if="props.greeting !== 'personal'" @click="toggleFavorite(item.id)"
                            class="absolute top-3 right-3 p-2 bg-white dark:bg-gray-700 bg-opacity-80 dark:bg-opacity-70 rounded-xl shadow-md hover:bg-opacity-100 dark:hover:bg-opacity-90 transform hover:scale-110">
                            <i class="fa text-2xl"
                                :class="isFavorite(item.id) ? 'fa-heart text-red-500' : 'fa-heart-o text-amber-600 dark:text-amber-300'"></i>
                        </button>
                    </div>

                    <!-- Contenido -->
                    <div class="p-5">
                        <h3 class="text-xl font-bold text-amber-800 dark:text-amber-300 font-serif line-clamp-1">{{
                            item.title }}</h3>
                        <p class="text-amber-600 dark:text-gray-300 text-sm mt-2"
                            :class="{ 'line-clamp-2': !expanded[item.id], 'line-clamp-none': expanded[item.id] }">
                            {{ item.description }}
                        </p>
                        <button v-if="item.description.length > 100" @click="toggleExpand(item.id)"
                            class="text-amber-800 dark:text-amber-400 text-sm font-medium mt-2 underline focus:outline-none">
                            {{ expanded[item.id] ? 'Leer menos...' : 'Leer más...' }}
                        </button>

                        <div class="mt-4 pt-4 border-t border-amber-100 dark:border-gray-700">
                            <StarRating :rating="ratings[item.id] || 0" :onRatingChanged="ratingChanged(item.id)" />
                            <div v-if="ratings[item.id] === 0" class="text-amber-500 dark:text-amber-300 mt-2 text-sm">
                                ¡Sé el primero en calificar!</div>
                        </div>

                        <div class="my-4 border-t border-amber-200 dark:border-gray-700"></div>

                        <router-link :to="'/recipe?id=' + item.id"  @click="idRecipe = item.id"
                            class="inline-flex items-center justify-center w-full px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg font-medium hover:from-amber-600 hover:to-amber-700 shadow-sm">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                            Ver Receta
                        </router-link>

                        <div class="text-sm text-amber-700 dark:text-amber-300 mt-4 p-3 rounded-lg">
                            <template v-if="categorias.filter(c => c.recipe_id === item.id).length">
                                <button @click="filter(cat)"
                                    v-for="cat in categorias.filter(c => c.recipe_id === item.id)"
                                    :key="cat.type + cat.category"
                                    class="inline-block bg-amber-200 dark:bg-gray-700 text-amber-800 dark:text-amber-300 px-2 py-1 rounded-full text-xs mr-1 mb-1">
                                    {{ cat.type }}
                                </button>
                            </template>
                            <span v-else class="text-amber-500 dark:text-amber-300 italic">No tiene categorías</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Paginador -->
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

        <!-- Mensaje si no hay recetas -->
        <div v-else class="text-center py-12 dark:bg-gray-900">
            <div class="max-w-md mx-auto">
                <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-16 w-16 text-amber-400 dark:text-amber-500"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>

                <div v-if="props.greeting === 'all'">
                    <h3 class="mt-4 text-lg font-medium text-amber-800 dark:text-amber-200">No hay recetas disponibles
                    </h3>
                    <p class="mt-2 text-amber-600 dark:text-amber-400">Parece que aún no hay recetas. ¡Sé el primero en
                        compartir una!</p>
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

                <div v-else-if="props.greeting === 'favs'">
                    <h3 class="mt-4 text-lg font-medium text-amber-800 dark:text-amber-200">No tienes recetas favoritas
                    </h3>
                    <p class="mt-2 text-amber-600 dark:text-amber-400">Añade recetas a tus favoritos para encontrarlas
                        fácilmente más tarde.</p>
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

                <div v-else-if="props.greeting === 'personal'">
                    <h3 class="mt-4 text-lg font-medium text-amber-800 dark:text-amber-200">No has creado ninguna receta
                    </h3>
                    <p class="mt-2 text-amber-600 dark:text-amber-400">Comparte tus creaciones culinarias con la
                        comunidad.</p>
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

                <div v-else>
                    <h3 class="mt-4 text-lg font-medium text-amber-800 dark:text-amber-200">No hay recetas que coincidan
                        con tu
                        filtro</h3>
                    <p class="mt-2 text-amber-600 dark:text-amber-400">Intenta ajustar los filtros para encontrar lo que
                        buscas.
                    </p>
                </div>
            </div>
        </div>

    </div>
    <div ref="loading" class="flex flex-col items-center min-h-screen px-4">
        <div
            class="inline-block animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 md:h-16 md:w-16 border-t-2 border-b-2 border-amber-600 dark:border-amber-400">
        </div>
        <p class="mt-3 sm:mt-4 text-amber-700 dark:text-amber-300 text-sm sm:text-base md:text-lg text-center">Cargando
            recetas...</p>
    </div>
</template>

<script setup>

import { reactive, defineProps, watch, onMounted, ref, defineEmits, computed } from 'vue';
import StarRating from './StarRating.vue';
import { useRouter } from 'vue-router';
import axios from 'axios';


const favoritos = reactive({});
const ratings = reactive({});
const average = reactive({})
const userToken = localStorage.getItem('userToken');
const router = useRouter();
const elementos = reactive({
    recetas: []
});
const categorias = reactive([])

const props = defineProps({
    greeting: {
        type: String,
        required: true
    },
    idRecipe: {
        type: String,
        required: true
    },
    contentTop: {
        type: undefined,
        required: true
    }
});
const tipoComida = ref('');
const ccaa = ref('');
const tiempo = ref('');
const proteinas = ref([]);
const emit = defineEmits(['enviarFiltros'])
const expanded = reactive({});
const currentPage = ref(1);
const itemsPerPage = ref(6)
const darkMode = ref(false);
const loading = ref(null)
const list = ref(null)
const timeStart = ref(0)
const timeEnd = ref(0)
const timeTotal = ref(0)
const idRecipe = ref(0)

watch(() => props.greeting, (newGreeting) => {
    if (newGreeting === "filtred") {
        filterRecipe()
    } else if (props.greeting === "all") {
        allRecipes()
    }
})

watch(currentPage, () => {
  if (props.contentTop) {
    props.contentTop.scrollIntoView({ behavior: 'smooth' });
  }
});

watch(idRecipe, () => {
  if (props.contentTop) {
    props.contentTop.scrollIntoView({ behavior: 'smooth' });
  }
});

function selectFavorites(favorites_list) {

    favorites_list.forEach(recipe => {
        const recipeId = recipe.id_recipe || recipe.id;
        favoritos[recipeId] = true;
    });
}

function selectReviews(reviews_list) {
    reviews_list.forEach(recipe => {
        ratings[recipe.id_recipe] = recipe.review;
    });
}

onMounted(() => {
    timeStart.value = performance.now();
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode !== null) {
        darkMode.value = JSON.parse(savedMode);
        applyDarkMode();
    }
    if (props.greeting === "all") {
        allRecipes()
    } else if (props.greeting === "favs") {
        favoritesRecipes()
    } else if (props.greeting === "personal") {
        personalRecipes()
    }
    averageStars();
});


function allRecipes() {
    categorias.length = 0;

    const payload = {
        userToken: localStorage.getItem('userToken')
    }


    axios.post(`${process.env.VUE_APP_API_URL}/viewAll`, payload)
        .then(response => {
            elementos.recetas = response.data.recipes_list;
            response.data.categories_list.forEach(element => {
                categorias.push(element)

            });
            timeCharge()
            if (response.data.user_id) {
                selectFavorites(response.data.favorites_list)
                selectReviews(response.data.reviews_list)
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function favoritesRecipes() {
    const payload = {
        userToken: userToken
    };

    axios
        .post(`${process.env.VUE_APP_API_URL}/viewFavs`, payload)
        .then(response => {
            elementos.recetas = response.data.favorites_list;
            selectFavorites(response.data.favorites_list)
            selectReviews(response.data.reviews_list)
            response.data.categories_list.forEach(element => {
                categorias.push(element)
            });
            timeCharge()
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
            if (error.status == 500 || error.status == 401) {
                router.push({ name: 'login' });
                localStorage.removeItem('userToken')
            }
        });
}

function personalRecipes() {
    if (localStorage.getItem('userToken') == null) {
        router.push({ name: "login" });
    } else {
        const payload = {
            userToken: localStorage.getItem('userToken')
        }

        axios.post(`${process.env.VUE_APP_API_URL}/viewRecipes`, payload)
            .then(response => {
                if (response.data.recipes_list && response.data.recipes_list.length >= 0) {
                    elementos.recetas = response.data.recipes_list;

                    response.data.categories_list.forEach(element => {
                        categorias.push(element)
                    });
                    selectReviews(response.data.reviews_list);
                    timeCharge()
                }

            })
            .catch(error => {
                console.error("Error al obtener las recetas:", error);
                if (error.status == 500 || error.status == 401) {
                    router.push({ name: 'login' });
                    localStorage.removeItem('userToken')
                }

            });
    }
}

function filter(categorias) {
    if (categorias.category == "typeeat") {
        tipoComida.value = categorias.type
    } else if (categorias.category == "ccaa") {
        ccaa.value = categorias.type
    } else if (categorias.category == "time") {
        tiempo.value = categorias.type
    } else if (categorias.category == "protein") {
        proteinas.value = [categorias.type]
    }
    const payload = {
        typeeat: tipoComida.value,
        ccaa: ccaa.value,
        time: tiempo.value,
        proteins: proteinas.value,
    }

    axios.post(`${process.env.VUE_APP_API_URL}/filterRecipe`, payload)
        .then(response => {
            emit('enviarFiltros', {
                idRecipe: response.data.message,
                greeting: 'filtred',
                type: categorias.type,
                category: categorias.category
            });
        })
        .catch(error => {
            console.log(error);
        });
}

function filterRecipe() {
    const seen = new Set();
    const filtered = [];
    props.idRecipe.forEach(element => {
        const id = element["idrecipe"];
        if (!seen.has(id)) {
            seen.add(id);
            filtered.push(element);
        }
    });
    axios.post(`${process.env.VUE_APP_API_URL}/recipeFilter`, { filtered, userToken })
        .then(response => {
            elementos.recetas = response.data.filtered_recipes
            if (userToken) {
                selectFavorites(response.data.favorites_list)
                selectReviews(response.data.reviews_list)
                currentPage.value = 1;
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

// Cambiar el estado de favoritos
const toggleFavorite = (id) => {
    if (userToken) {
        const payload = {
            idrecipe: id,
            userToken,
            comment: "",
            idcomment: 0
        };

        if (favoritos[id]) {
            favoritos[id] = false;
            axios.post(`${process.env.VUE_APP_API_URL}/deleteFavs`, payload)
                .then(response => {
                    console.log(response.data.message);
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        } else {
            favoritos[id] = true;
            axios.post(`${process.env.VUE_APP_API_URL}/updateFavs`, payload)
                .then(response => {
                    console.log(response.data.message);
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        }
    } else {
        router.push({ name: "login" });
    }
};

// Comprobar si una receta es favorita
const isFavorite = (id) => {
    return favoritos[id] || false;
};

// Función para cambiar la calificación de una receta
const ratingChanged = (recipeId) => {
    if (userToken) {
        return (newRating) => {
            ratings[recipeId] = newRating;
            const payload = {
                idrecipe: recipeId,
                rating: newRating,
                userToken
            };
            axios.post(`${process.env.VUE_APP_API_URL}/updateRating`, payload)
                .then(() => {
                    averageStars()
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        };
    }
};

function averageStars() {
    axios.post(`${process.env.VUE_APP_API_URL}/averageStars`)
        .then(response => {
            response.data.media.forEach(rating => {
                average[rating.recipe_id] = rating.average_rating
            });
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

const toggleExpand = (id) => {
    expanded[id] = !expanded[id];
};

const paginatedRecipes = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return elementos.recetas.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(elementos.recetas.length / itemsPerPage.value);
});

function applyDarkMode() {
    if (darkMode.value) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

const timeCharge = () => {
    if (elementos.recetas.length >= 0) {
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

</script>

<style scoped>
/* Animación para el corazón de favoritos */
@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
}

.fa-heart {
    animation: pulse 1.5s infinite;
}

/* Efecto para el hover de la tarjeta */
.transform:hover\: -translate-y-1:hover {
    transform: translateY(-4px);
    transition: transform 0.3s ease;
}

/* Limitar líneas de texto */
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

/* Estilo cuando la descripción se expande */
.line-clamp-none {
    -webkit-line-clamp: unset;
}
</style>