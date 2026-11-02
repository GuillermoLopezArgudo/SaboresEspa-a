<template>
  <div>
    <PageHero
      title="Recetario"
      subtitle="Descubre y comparte recetas de la cocina española"
    >
      <router-link
        v-if="loggedIn"
        to="/create"
        class="hero-cta-primary"
      >
        + Nueva receta
      </router-link>
      <router-link
        v-else
        to="/register"
        class="hero-cta-ghost"
      >
        Únete para compartir
      </router-link>
    </PageHero>

    <RecipeFilter
      :criteria="filterCriteria"
      @aplicarFiltros="aplicarFiltros"
      @limpiarFiltros="limpiarFiltros"
    />

    <div class="max-w-7xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <ListRecipes
        :greeting="greeting"
        :filterCriteria="filterCriteria"
        sync-url
        @seleccionarCategoria="onSeleccionarCategoria"
      />
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'MainPage' })

import PageHero from './PageHero.vue'
import RecipeFilter from './FilterRecipe.vue'
import ListRecipes from './ListRecipes.vue'
import { computed, ref } from 'vue'
import { isTokenValid } from '../api'
import {
  hasActiveFilters,
  mergeFilterCriteria,
} from '../utils/filterOptions'

const greeting = ref('all')
const filterCriteria = ref(null)
const loggedIn = computed(() => isTokenValid(localStorage.getItem('userToken')))

function aplicarFiltros(criteria) {
  filterCriteria.value = criteria
  greeting.value = 'filtred'
}

function limpiarFiltros() {
  filterCriteria.value = null
  greeting.value = 'all'
}

function onSeleccionarCategoria({ category, type }) {
  if (!category || !type) return
  const next = mergeFilterCriteria(filterCriteria.value, category, type)
  filterCriteria.value = next
  greeting.value = hasActiveFilters(next) ? 'filtred' : 'all'
}
</script>
