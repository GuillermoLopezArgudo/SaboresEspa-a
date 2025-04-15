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

    <RecipeFilter :type="type" :category="category" @enviarFiltros="recibirFiltros" @limpiarFiltros="limpiarFiltros" ></RecipeFilter>
    <!-- Contenido principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Barra de navegación actualizada -->
      <ListRecipes :greeting="greeting" :idRecipe="idRecipe"  @enviarFiltros="recibirFiltros"></ListRecipes>
    </div>
  </div>
</template>

<script setup>
import 'font-awesome/css/font-awesome.min.css';
import RecipeFilter from './FilterRecipe.vue';
import ListRecipes from './ListRecipes.vue';
import { ref } from 'vue';


const idRecipe = ref('')
const greeting = ref("all")
const type = ref("")
const category = ref('')

function recibirFiltros(datos) {
  idRecipe.value = datos.idRecipe;
  type.value = datos.type
  category.value = datos.category
  greeting.value = "";
  setTimeout(() => {
    greeting.value = datos.greeting;
  }, 1);
  
}

const limpiarFiltros = () => {

  greeting.value = "all";
}



</script>

<style scoped></style>