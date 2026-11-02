<template>
  <div>
    <PageHero
      title="Recetario"
      subtitle="Descubre y comparte recetas de la cocina española"
    />
    <RecipeFilter @enviarIdRecipe="recibirIdRecipe" @limpiarFiltros="limpiarFiltros" />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <ListRecipes :greeting="greeting" :idRecipe="idRecipe" />
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'MainPage' })

import PageHero from './PageHero.vue'
import RecipeFilter from './FilterRecipe.vue'
import ListRecipes from './ListRecipes.vue'
import { ref } from 'vue'

const idRecipe = ref([])
const greeting = ref('all')

function recibirIdRecipe(mensaje) {
  idRecipe.value = Array.isArray(mensaje) ? mensaje : []
  greeting.value = 'filtred'
}

const limpiarFiltros = () => {
  greeting.value = 'all'
  idRecipe.value = []
}
</script>
