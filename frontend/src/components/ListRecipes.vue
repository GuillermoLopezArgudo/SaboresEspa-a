<template>
    <!-- Listado de recetas -->
    <div v-if="elementos.recetas.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(item) in elementos.recetas" :key="item.id"
            class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 border border-amber-100 transform hover:-translate-y-1">
            <!-- Imagen con corazón superpuesto -->
            <div class="relative">
                <!-- Imagen de la receta -->
                <img v-if="item.image" :src="`http://localhost:5000/${item.image}`" class="w-full h-48 object-cover"
                    alt="Imagen de receta">
                <!-- Placeholder si no hay imagen -->
                <div v-else class="h-48 bg-amber-200 flex items-center justify-center text-amber-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                            d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                </div>

                <!-- Corazón de favorito (posición absoluta) -->
                <button v-if="props.greeting !== 'personal'" @click="toggleFavorite(item.id)"
                    class="absolute top-3 right-3 p-2 bg-white bg-opacity-80 rounded-full shadow-md hover:bg-opacity-100 transition-all duration-300 transform hover:scale-110">
                    <i class="fa text-2xl"
                        :class="isFavorite(item.id) ? 'fa-heart text-red-500' : 'fa-heart-o text-amber-600'"></i>
                </button>
            </div>

            <!-- Contenido de la tarjeta -->
            <div class="p-5">
                <h3 class="text-xl font-bold text-amber-800 font-serif line-clamp-1">{{ item.title }}</h3>
                <p class="text-amber-600 text-sm mt-2 line-clamp-2">{{ item.description }}</p>
                <!-- Valoración con estrellas -->
                <div class="mt-4 pt-4 border-t border-amber-100" v-if="props.greeting != 'personal'">
                    <StarRating :rating="ratings[item.id] || 0" :onRatingChanged="ratingChanged(item.id)" />
                </div>

                <!-- Botón para ver receta -->
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

                <!--Zona de Categorias-->
                <div class="text-sm text-amber-700 mt-2">
                    <span class="font-semibold">Categorías:</span>
                    <template v-if="categorias.filter(c => c.recipe_id === item.id).length > 0">
                        <span v-for="cat in categorias.filter(c => c.recipe_id === item.id)"
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
    <div v-else class="text-center py-12">
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

import { reactive, defineProps, watch, onMounted } from 'vue';
import StarRating from './StarRating.vue';
import { useRouter } from 'vue-router';
import axios from 'axios';


const favoritos = reactive({});
const ratings = reactive({});
const userToken = localStorage.getItem('userToken');
const iduser = localStorage.getItem('iduser');
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
    }
});

watch(() => props.greeting, (newGreeting) => {
    if (newGreeting === "filtred") {
        filterRecipe()
    } else if (props.greeting === "all") {
        // Solicitar todas las recetas y datos relacionados
        allRecipes()
    }
})

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
    if (props.greeting === "all") {
        allRecipes()
    } else if (props.greeting === "favs") {
        favoritesRecipes()
    } else if (props.greeting === "personal") {
        personalRecipes()
    }
});


function allRecipes() {
    axios.post('http://localhost:5000/viewAll', { iduser })
        .then(response => {
            elementos.recetas = response.data.recipes_list;
            if (iduser) {
                selectFavorites(response.data.favorites_list)
                selectReviews(response.data.reviews_list)
                response.data.categories_list.forEach(element => {
                    categorias.push(element)
                });
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function favoritesRecipes() {
    const payload = {
        userToken: userToken,
        iduser: iduser
    };

    axios
        .post('http://localhost:5000/viewFavs', payload)
        .then(response => {
            elementos.recetas = response.data.favorites_list;
            selectFavorites(response.data.favorites_list)
            selectReviews(response.data.reviews_list)
            response.data.categories_list.forEach(element => {
                    categorias.push(element)
            });
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function personalRecipes() {
    if (localStorage.getItem('userToken') == null) {
        router.push({ name: "login" });
    } else {
        const payload = {
            id: localStorage.getItem("iduser"),
            userToken: userToken.value
        }

        axios.post('http://localhost:5000/viewRecipes', payload)
            .then(response => {
                if (response.data.message && response.data.message.length > 0) {
                    elementos.recetas = response.data.message;
                    response.data.categories_list.forEach(element => {
                        categorias.push(element)
                    });
                }
            })
            .catch(error => {
                console.error("Error al obtener las recetas:", error);
            });
    }
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
    axios.post('http://localhost:5000/recipeFilter', { filtered, iduser })
        .then(response => {
            elementos.recetas = response.data.filtered_recipes
            if (iduser) {
                selectFavorites(response.data.favorites_list)
                selectReviews(response.data.reviews_list)
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
            iduser,
            idcomment: 0
        };

        if (favoritos[id]) {
            favoritos[id] = false;
            axios.post('http://localhost:5000/deleteFavs', payload)
                .then(response => {
                    console.log(response.data.message);
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        } else {
            favoritos[id] = true;
            axios.post('http://localhost:5000/updateFavs', payload)
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
                userToken,
                iduser
            };

            localStorage.setItem('ratings', JSON.stringify(ratings));
            axios.post('http://localhost:5000/updateRating', payload)
                .then(response => {
                    console.log(response.data.message);
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        };
    }
};
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
.transform:hover\:-translate-y-1:hover {
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
</style>