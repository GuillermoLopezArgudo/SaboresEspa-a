<template>
  <div id="app" class="se-page">
    <NavbarHome />
    <main class="flex-1 w-full min-w-0">
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
import { onMounted } from 'vue'
import NavbarHome from './components/NavbarHome.vue'
import FooterPage from './components/FooterPage.vue'
import { initTheme } from './utils/theme'

const cachedPages = ['MainPage', 'HomeRecipe', 'PersonalRecipes', 'ProfileUser']

onMounted(() => {
  initTheme()
})
</script>
