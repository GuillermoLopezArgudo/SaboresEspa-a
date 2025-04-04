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
  
        <RecipeFilter @enviarIdRecipe="recibirMensaje"></RecipeFilter>
        <ListRecipes :greeting="greeting"></ListRecipes>

      </div>
    </div>
  </template>
  
  <script setup>

  import 'font-awesome/css/font-awesome.min.css';
  import RecipeFilter from './FilterRecipe.vue';
  import ListRecipes from './ListRecipes.vue';
  import { ref } from 'vue';

  const userToken = localStorage.getItem('userToken');
  const a = ref('')
  const greeting = ref("all")
  function recibirMensaje(mensaje) {
    a.value= mensaje
    greeting.value="a"
  }

  </script>
  
  <style scoped>

  </style>