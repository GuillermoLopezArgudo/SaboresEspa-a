<template>
  <div>
    <PageHero
      title="Mis recetas"
      subtitle="Todo lo que has compartido con la comunidad"
    >
      <router-link
        to="/create"
        class="inline-flex items-center px-4 py-2 rounded-full bg-white text-amber-950 text-sm font-semibold shadow-sm hover:bg-amber-50 transition"
      >
        + Nueva receta
      </router-link>
      <router-link
        to="/"
        class="inline-flex items-center px-4 py-2 rounded-full bg-white/15 hover:bg-white/25 text-white text-sm font-medium border border-white/20 transition"
      >
        Ver recetario
      </router-link>
    </PageHero>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <ListRecipes :greeting="'personal'" />
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'PersonalRecipes' })

import PageHero from './PageHero.vue'
import ListRecipes from './ListRecipes.vue'
</script>
