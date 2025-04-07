<template>
  <div class="min-h-screen bg-amber-50">
    <!-- Contenido principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Barra de navegación actualizada -->
    <NavbarHome/>

      <RecipeFilter @enviarIdRecipe="recibirIdRecipe" @limpiarFiltros="limpiarFiltros"></RecipeFilter>
      <ListRecipes :greeting="greeting" :idRecipe="idRecipe"></ListRecipes>
    </div>
  </div>
</template>

<script setup>
import 'font-awesome/css/font-awesome.min.css';
import RecipeFilter from './FilterRecipe.vue';
import ListRecipes from './ListRecipes.vue';
import NavbarHome from './NavbarHome.vue';
import { ref } from 'vue';


const idRecipe = ref('')
const greeting = ref("all")

function recibirIdRecipe(mensaje) {
  idRecipe.value = mensaje
  greeting.value = "filtred"
}

const limpiarFiltros = () => {
  greeting.value = "all";
}

</script>

<style scoped></style>