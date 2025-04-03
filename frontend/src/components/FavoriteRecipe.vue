<template>
  <div class="min-h-screen bg-amber-50 py-8 px-4 sm:px-6 lg:px-8">
    <!-- Encabezado -->
    <div class="max-w-7xl mx-auto text-center mb-8">
      <h1 class="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-3">
        Mis Recetas Favoritas
      </h1>
      <p class="text-lg text-amber-700">Tus creaciones culinarias preferidas en un solo lugar</p>
    </div>

    <!-- Listado de recetas -->
    <div v-if="recetas.length > 0" class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="(item) in recetas" :key="item.id" 
           class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 border border-amber-100 transform hover:-translate-y-1">
        <!-- Imagen de la receta -->
        <div class="relative h-56 overflow-hidden">
          <img :src="`http://localhost:5000/${item.image}`" 
               class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
               alt="Imagen de receta">
          <div class="absolute top-3 right-3 bg-amber-600 text-white px-2 py-1 rounded-full text-xs font-semibold shadow-lg">
            <i class="fas fa-heart mr-1"></i> Favorita
          </div>
        </div>
        
        <!-- Contenido de la tarjeta -->
        <div class="p-5">
          <h3 class="text-xl font-bold text-amber-800 mb-2 font-serif line-clamp-1">{{ item.title }}</h3>
          <p class="text-amber-600 text-sm mb-4 line-clamp-2">{{ item.description }}</p>
          
          <!-- Botón para ver receta -->
          <router-link :to="'/recipe?id=' + item.id" 
                      class="inline-flex items-center justify-center w-full px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg font-medium hover:from-amber-600 hover:to-amber-700 transition duration-300 shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            Ver Receta
          </router-link>
        </div>
      </div>
    </div>

    <!-- Mensaje cuando no hay favoritos -->
    <div v-else class="max-w-2xl mx-auto text-center mt-12">
      <div class="p-6 bg-amber-100 border-l-4 border-amber-500 rounded-lg shadow-md">
        <div class="flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-amber-600 mr-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="text-xl font-bold text-amber-800 mb-1">No tienes recetas favoritas</h3>
            <p class="text-amber-700">Marca tus recetas preferidas con ❤️ y aparecerán aquí</p>
          </div>
        </div>
        <router-link to="/" 
                    class="mt-4 inline-flex items-center px-5 py-2 bg-amber-600 text-white rounded-lg font-medium hover:bg-amber-700 transition duration-300">
          Explorar Recetas
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userToken = localStorage.getItem('userToken');
const iduser = localStorage.getItem('iduser');

const recetas = ref([]);

// Cuando se crea el componente, si hay favoritos en localstorage, llama al backend para obtenerlos
onMounted(() => {
  const payload = {
    userToken: userToken,
    iduser: iduser
  };  

  axios
    .post('http://localhost:5000/viewFavs', payload)
    .then(response => {
      recetas.value = response.data.message;
    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
    });
});
</script>

<style scoped>
/* Efecto para las tarjetas */
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
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

/* Animación para el ícono de favorito */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.fa-heart {
  animation: pulse 1.5s infinite;
}
</style>