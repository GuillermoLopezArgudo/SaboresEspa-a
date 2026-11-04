<template>
  <div>
    <PageHero
      title="Mis recetas"
      subtitle="Todo lo que has compartido con la comunidad"
    >
      <router-link to="/create" class="hero-cta-primary">
        + Nueva receta
      </router-link>
      <router-link to="/" class="hero-cta-ghost">
        Ver recetario
      </router-link>
    </PageHero>
    <div class="max-w-7xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <ListRecipes :greeting="'personal'" />
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'PersonalRecipes' })

import PageHero from './PageHero.vue'
import ListRecipes from './ListRecipes.vue'
</script>
