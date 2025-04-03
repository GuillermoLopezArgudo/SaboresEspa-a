<template>
    <div class="min-h-screen bg-amber-50 py-8 px-4 sm:px-6 lg:px-8">
      <!-- Encabezado -->
      <div class="max-w-7xl mx-auto text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-3">
          Tus Creaciones Culinarias
        </h1>
        <p class="text-lg text-amber-700">Todas las recetas que has compartido con la comunidad</p>
      </div>
  
      <!-- Botón de regreso -->
      <div class="max-w-7xl mx-auto mb-6">
        <router-link to="/home" class="inline-flex items-center px-5 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg transition duration-300 shadow-md">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          Volver al inicio
        </router-link>
      </div>
  
      <!-- Listado de recetas -->
      <div v-if="elementos.recetas.length > 0" class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(item, index) in elementos.recetas[0]" :key="index" class="transform hover:-translate-y-1 transition duration-300">
          <Recipe :item="item" class="h-full" />
        </div>
      </div>
  
      <!-- Mensaje cuando no hay recetas -->
      <div v-else class="max-w-2xl mx-auto text-center mt-12">
        <div class="p-6 bg-amber-100 border-l-4 border-amber-500 rounded-lg shadow-md">
          <div class="flex flex-col items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-amber-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 class="text-xl font-bold text-amber-800 mb-2">No has creado recetas aún</h3>
            <p class="text-amber-700 mb-4">Comparte tus creaciones culinarias con la comunidad</p>
            <router-link to="/create" class="inline-flex items-center px-5 py-2 bg-amber-600 text-white rounded-lg font-medium hover:bg-amber-700 transition duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Crear primera receta
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import axios from 'axios';
  import Recipe from './RecipesHome.vue';
  import { useRouter } from 'vue-router';
  
  const userToken = ref(localStorage.getItem("userToken"));
  const router = useRouter();
  const elementos = reactive({
    recetas: []
  });
  
  // Comprueba si el token esta guardado en el localstorage
  onMounted(() => {
    if (userToken.value == null) {
      router.push({ name: "login" });
    } else {
      const payload = {
        id: localStorage.getItem("iduser"),
        userToken: userToken.value
      }
  
      axios.post('http://localhost:5000/viewRecipes', payload)
        .then(response => {
          if (response.data.message && response.data.message.length > 0) {
            elementos.recetas.push(response.data.message);
          }
        })
        .catch(error => {
          console.error("Error al obtener las recetas:", error);
        });
    }
  });
  </script>
  
  <style scoped>
  /* Animación para las tarjetas al cargar */
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .grid > div {
    animation: fadeInUp 0.5s ease-out;
    animation-fill-mode: both;
  }
  
  /* Efecto escalonado para las animaciones */
  .grid > div:nth-child(1) { animation-delay: 0.1s; }
  .grid > div:nth-child(2) { animation-delay: 0.2s; }
  .grid > div:nth-child(3) { animation-delay: 0.3s; }
  .grid > div:nth-child(4) { animation-delay: 0.4s; }
  .grid > div:nth-child(5) { animation-delay: 0.5s; }
  .grid > div:nth-child(6) { animation-delay: 0.6s; }
  </style>