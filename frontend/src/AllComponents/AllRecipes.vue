<template>
  <div class="min-h-screen bg-amber-50">
    <!-- Header con imagen de fondo -->
    <div class="relative bg-amber-900 py-12 px-4 sm:px-6 lg:px-8">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="relative max-w-7xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-white font-serif mb-4">Recetario de Cocina</h1>
        <p class="text-xl text-amber-100">Descubre y comparte tus recetas favoritas</p>
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Barra de navegación -->
      <nav class="bg-white rounded-lg shadow-md mb-8 p-4 border border-amber-200">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span class="text-xl font-semibold text-amber-800 font-serif">Mis Recetas</span>
          </div>
          <div v-if="!userToken" class="flex space-x-3">
            <router-link to="/login" class="px-5 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-medium transition-colors duration-300 shadow-sm hover:shadow-md flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
              Iniciar Sesión
            </router-link>
            <router-link to="/register" class="px-5 py-2 bg-white border border-amber-600 text-amber-700 hover:bg-amber-50 rounded-lg font-medium transition-colors duration-300 shadow-sm hover:shadow-md flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6z" />
              </svg>
              Registrar
            </router-link>
          </div>
          <div v-else>
            <router-link to="/home" class="px-5 py-2 bg-amber-800 hover:bg-amber-900 text-white rounded-lg font-medium transition-colors duration-300 shadow-sm hover:shadow-md flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
              </svg>
              Mi Cocina
            </router-link>
          </div>
        </div>
      </nav>

      <RecipeFilter></RecipeFilter>

      <!-- Listado de recetas -->
      <div v-if="elementos.recetas.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(item) in elementos.recetas" :key="item.id" class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 border border-amber-100 transform hover:-translate-y-1">
          <!-- Imagen con corazón superpuesto -->
          <div class="relative">
            <!-- Imagen de la receta -->
            <img v-if="item.image" :src="`http://localhost:5000/${item.image}`" 
                 class="w-full h-48 object-cover" alt="Imagen de receta">
            <!-- Placeholder si no hay imagen -->
            <div v-else class="h-48 bg-amber-200 flex items-center justify-center text-amber-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            
            <!-- Corazón de favorito (posición absoluta) -->
            <button @click="toggleFavorite(item.id)" 
                    class="absolute top-3 right-3 p-2 bg-white bg-opacity-80 rounded-full shadow-md hover:bg-opacity-100 transition-all duration-300 transform hover:scale-110">
              <i class="fa text-2xl" :class="isFavorite(item.id) ? 'fa-heart text-red-500' : 'fa-heart-o text-amber-600'"></i>
            </button>
          </div>
          
          <!-- Contenido de la tarjeta -->
          <div class="p-5">
            <h3 class="text-xl font-bold text-amber-800 font-serif line-clamp-1">{{ item.title }}</h3>
            <p class="text-amber-600 text-sm mt-2 line-clamp-2">{{ item.description }}</p>
            
            <!-- Valoración con estrellas -->
            <div class="mt-4 pt-4 border-t border-amber-100">
              <StarRating :rating="ratings[item.id] || 0" :onRatingChanged="ratingChanged(item.id)" />
            </div>
          </div>
        </div>
      </div>

      <!-- Mensaje si no hay recetas -->
      <div v-else class="text-center py-12">
        <div class="max-w-md mx-auto">
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-16 w-16 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-amber-800">No hay recetas disponibles</h3>
          <p class="mt-2 text-amber-600">Parece que aún no hay recetas. ¡Sé el primero en compartir una!</p>
          <div class="mt-6">
            <router-link to="/create" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Crear nueva receta
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { reactive } from 'vue';
import StarRating from './StarRating.vue';
import 'font-awesome/css/font-awesome.min.css';
import { useRouter } from 'vue-router';
import RecipeFilter from './RecipeFilter.vue';

const elementos = reactive({
  recetas: []
});
const favoritos = reactive({});
const ratings = reactive({});
const userToken = localStorage.getItem('userToken');
const iduser = localStorage.getItem('iduser');
const router = useRouter();

// Solicitar todas las recetas y datos relacionados
axios.post('http://localhost:5000/viewAll', { iduser })
  .then(response => {
    elementos.recetas = response.data.recipes_list;
    if (iduser) {
      response.data.favorites_list.forEach(id => {
        favoritos[id.id_recipe] = true;
      });
      response.data.reviews_list.forEach(id => {
        ratings[id.id_recipe] = id.review;
      });
    }
  })
  .catch(error => {
    console.error("Error en la solicitud:", error);
  });

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
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
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