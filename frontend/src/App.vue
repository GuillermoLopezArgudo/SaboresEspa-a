<template>
      <!-- Navbar Component -->
      <NavbarHome />
  <div id="app">
    <router-view></router-view>
  </div>
  <FooterPage></FooterPage>
</template>

<script setup>
import NavbarHome from './components/NavbarHome.vue';
import FooterPage from './components/FooterPage.vue';
</script>

<style></style>
