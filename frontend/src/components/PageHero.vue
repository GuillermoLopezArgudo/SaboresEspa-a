<template>
  <header class="relative overflow-hidden bg-amber-900">
    <div class="absolute inset-0 bg-gradient-to-br from-amber-950/40 via-transparent to-black/25" />
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 md:py-10 text-center">
      <p v-if="eyebrow" class="text-amber-200/80 text-[10px] sm:text-xs font-semibold tracking-[0.18em] uppercase mb-2">
        {{ eyebrow }}
      </p>
      <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold text-white font-serif leading-tight px-1">
        {{ title }}
      </h1>
      <p v-if="subtitle" class="mt-2 text-amber-100/90 text-sm sm:text-base md:text-lg max-w-2xl mx-auto px-1">
        {{ subtitle }}
      </p>
      <div v-if="$slots.default" class="mt-4 sm:mt-5 flex flex-wrap justify-center gap-2">
        <slot />
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  eyebrow: { type: String, default: 'Sabores España' },
})
</script>
