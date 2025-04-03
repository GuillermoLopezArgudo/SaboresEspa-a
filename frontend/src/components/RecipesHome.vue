<template>
    <div class="max-w-xs mx-auto my-4 overflow-hidden bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-[1.02] border border-amber-100">
      <!-- Imagen de la receta -->
      <div class="relative h-48 overflow-hidden">
        <img 
          :src="`http://localhost:5000/${item.image}`" 
          class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
          alt="Imagen de la receta"
          v-if="item.image"
        />
        <!-- Placeholder si no hay imagen -->
        <div v-else class="w-full h-full bg-amber-100 flex items-center justify-center text-amber-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
      </div>
  
      <!-- Contenido de la tarjeta -->
      <div class="p-5">
        <div class="mb-3">
          <h5 class="text-xl font-bold text-amber-800 font-serif line-clamp-1">{{ item.title }}</h5>
          <p 
            class="text-amber-600 text-sm mt-2 line-clamp-2" 
            :title="item.description"
          >
            {{ item.description }}
          </p>
        </div>
        
        <button 
          @click="OnClickRecipe" 
          class="w-full py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 text-white font-medium rounded-lg hover:from-amber-600 hover:to-amber-700 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2 transition-all duration-300 flex items-center justify-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          Ver Receta
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from "vue";
  import { useRouter } from "vue-router";
  
  const props = defineProps({
    item: {
      type: Object,   
      required: true
    }
  });
  
  const router = useRouter();
  
  function OnClickRecipe() {
    router.push({ name: "recipe", query: { id: props.item.id } });
  }
  </script>
  
  <style scoped>
  /* Efecto para el hover de la imagen */
  img:hover {
    transform: scale(1.1);
    transition: transform 0.5s ease;
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
  
  /* Animación para la tarjeta al cargar */
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .card-enter-active {
    animation: fadeIn 0.5s ease-out;
  }
  </style>