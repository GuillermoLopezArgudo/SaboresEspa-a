<template>
  <div>
    <PageHero
      title="Recetario"
      subtitle="Descubre y comparte recetas de la cocina española"
    />
    <RecipeFilter @aplicarFiltros="aplicarFiltros" @limpiarFiltros="limpiarFiltros" />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <ListRecipes :greeting="greeting" :filterCriteria="filterCriteria" />
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'MainPage' })

import PageHero from './PageHero.vue'
import RecipeFilter from './FilterRecipe.vue'
import ListRecipes from './ListRecipes.vue'
import { ref } from 'vue'

const greeting = ref('all')
const filterCriteria = ref(null)

function aplicarFiltros(criteria) {
  filterCriteria.value = criteria
  greeting.value = 'filtred'
}

function limpiarFiltros() {
  filterCriteria.value = null
  greeting.value = 'all'
}
</script>
