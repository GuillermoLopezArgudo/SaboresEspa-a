<template>
  <footer class="bg-amber-950 border-t border-amber-900">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex flex-col sm:flex-row items-center justify-between gap-2 text-sm">
      <p class="font-serif font-semibold text-amber-50">
        Sabores España
      </p>
      <p class="text-amber-200/60">
        © {{ year }} · Cocina española para compartir
      </p>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>
