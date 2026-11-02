<template>
  <div class="min-h-screen bg-amber-50">
    <div class="relative bg-amber-900 py-12 px-4 sm:px-6 lg:px-8">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="relative max-w-7xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-white font-serif mb-4">Recetario de Cocina</h1>
        <p class="text-xl text-amber-100">Descubre y comparte tus recetas favoritas</p>
      </div>
    </div>

    <NavbarHome />
    <RecipeFilter @enviarIdRecipe="recibirIdRecipe" @limpiarFiltros="limpiarFiltros" />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <ListRecipes :greeting="greeting" :idRecipe="idRecipe" />
    </div>
  </div>
  <FooterPage />
</template>

<script setup>
import 'font-awesome/css/font-awesome.min.css';
import RecipeFilter from './FilterRecipe.vue';
import ListRecipes from './ListRecipes.vue';
import FooterPage from './FooterPage.vue';
import NavbarHome from './NavbarHome.vue';
import { ref } from 'vue';

const idRecipe = ref([]);
const greeting = ref('all');

function recibirIdRecipe(mensaje) {
  idRecipe.value = Array.isArray(mensaje) ? mensaje : [];
  greeting.value = 'filtred';
}

const limpiarFiltros = () => {
  greeting.value = 'all';
  idRecipe.value = [];
};
</script>

<style scoped></style>
