<template>
  <footer class="bg-amber-950 text-amber-100/90 border-t border-amber-900">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-sm">
      <router-link to="/" class="font-serif font-semibold text-amber-50 hover:text-white transition">
        Sabores España
      </router-link>
      <p class="text-amber-200/70">© {{ year }} · Recetas de la cocina española</p>
      <div class="flex gap-4">
        <router-link to="/" class="hover:text-white transition">Recetario</router-link>
        <router-link to="/create" class="hover:text-white transition">Crear</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>
