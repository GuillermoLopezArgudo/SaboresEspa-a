<template>
  <div>
    <PageHero
      title="Tus favoritos"
      subtitle="Las recetas que has marcado para volver a ellas"
    />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <ListRecipes :greeting="'favs'" />
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'HomeRecipe' })

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageHero from './PageHero.vue'
import ListRecipes from './ListRecipes.vue'

const userToken = ref(localStorage.getItem('userToken'))
const router = useRouter()

if (userToken.value == null) {
  router.push({ name: 'login' })
}
</script>
