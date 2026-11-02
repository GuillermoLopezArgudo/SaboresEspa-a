<template>
  <div id="app" class="min-h-screen bg-amber-50 text-amber-950 flex flex-col">
    <NavbarHome />
    <main class="flex-1 w-full">
      <router-view v-slot="{ Component, route }">
        <keep-alive :include="cachedPages">
          <component :is="Component" :key="route.name" />
        </keep-alive>
      </router-view>
    </main>
    <FooterPage />
  </div>
</template>

<script setup>
import NavbarHome from './components/NavbarHome.vue'
import FooterPage from './components/FooterPage.vue'

const cachedPages = ['MainPage', 'HomeRecipe', 'PersonalRecipes', 'ProfileUser']
</script>
