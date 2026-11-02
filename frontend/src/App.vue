<template>
  <div id="app">
    <router-view v-slot="{ Component, route }">
      <keep-alive :include="cachedPages">
        <component :is="Component" :key="route.name" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script setup>
/** Páginas de listado: se conservan al navegar para no recargar ni parpadear. */
const cachedPages = ['MainPage', 'HomeRecipe', 'PersonalRecipes']
</script>

<style></style>
