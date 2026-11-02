<template>
  <header class="relative overflow-hidden isolate">
    <!-- Día: ámbar claro · Noche: terracota iluminada (no apagada) -->
    <div
      class="absolute inset-0 bg-gradient-to-br from-orange-50 via-amber-200 to-amber-400 dark:from-[#5c331a] dark:via-[#a3541c] dark:to-[#2a160e]"
    />
    <div
      class="absolute -top-24 left-1/2 -translate-x-1/2 h-[28rem] w-[42rem] rounded-full blur-2xl pointer-events-none bg-[radial-gradient(circle,rgba(255,255,255,0.75)_0%,transparent_68%)] dark:bg-[radial-gradient(circle,rgba(253,230,138,0.45)_0%,transparent_68%)]"
      aria-hidden="true"
    />
    <div
      class="absolute -bottom-28 -left-16 h-72 w-72 rounded-full blur-2xl pointer-events-none bg-[radial-gradient(circle,rgba(251,191,36,0.4)_0%,transparent_70%)] dark:bg-[radial-gradient(circle,rgba(245,158,11,0.4)_0%,transparent_70%)]"
      aria-hidden="true"
    />
    <div
      class="absolute -bottom-20 -right-10 h-64 w-80 rounded-full blur-2xl pointer-events-none bg-[radial-gradient(circle,rgba(217,119,6,0.28)_0%,transparent_70%)] dark:bg-[radial-gradient(circle,rgba(180,83,9,0.4)_0%,transparent_70%)]"
      aria-hidden="true"
    />
    <div class="page-hero-grain absolute inset-0 opacity-[0.07] dark:opacity-[0.12] mix-blend-multiply dark:mix-blend-soft-light pointer-events-none" aria-hidden="true" />
    <div
      class="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-amber-800/25 to-transparent dark:via-amber-200/40"
      aria-hidden="true"
    />

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12 md:py-16 text-center">
      <div class="hero-enter mx-auto max-w-3xl">
        <div v-if="eyebrow" class="inline-flex items-center gap-3 mb-4 sm:mb-5">
          <span class="hidden xs:block h-px w-8 bg-amber-800/35 dark:bg-amber-100/50" aria-hidden="true" />
          <p class="text-amber-900/85 dark:text-amber-100 text-[11px] sm:text-xs font-semibold tracking-[0.22em] uppercase">
            {{ eyebrow }}
          </p>
          <span class="hidden xs:block h-px w-8 bg-amber-800/35 dark:bg-amber-100/50" aria-hidden="true" />
        </div>

        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold font-serif leading-[1.1] tracking-tight px-1 text-amber-950 dark:text-white drop-shadow-sm dark:drop-shadow-[0_2px_16px_rgba(0,0,0,0.45)]">
          {{ title }}
        </h1>

        <p
          v-if="subtitle"
          class="mt-3 sm:mt-4 text-sm sm:text-base md:text-lg max-w-2xl mx-auto leading-relaxed px-1 text-amber-950/75 dark:text-amber-50"
        >
          {{ subtitle }}
        </p>

        <div v-if="$slots.default" class="mt-6 sm:mt-7 flex flex-wrap justify-center gap-2.5">
          <slot />
        </div>
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

<style scoped>
.page-hero-grain {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
  background-size: 180px 180px;
}

.hero-enter {
  animation: hero-rise 0.55s ease-out both;
}

@keyframes hero-rise {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-enter {
    animation: none;
  }
}
</style>
