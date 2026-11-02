<template>
  <header class="page-hero relative overflow-hidden isolate">
    <div class="page-hero-base absolute inset-0" aria-hidden="true" />
    <div class="page-hero-glow page-hero-glow-a absolute -top-24 left-1/2 -translate-x-1/2 h-[28rem] w-[42rem] rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
    <div class="page-hero-glow page-hero-glow-b absolute -bottom-28 -left-16 h-72 w-72 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
    <div class="page-hero-glow page-hero-glow-c absolute -bottom-20 -right-10 h-64 w-80 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
    <div class="page-hero-grain absolute inset-0 pointer-events-none" aria-hidden="true" />
    <div class="page-hero-edge absolute inset-x-0 bottom-0 h-px" aria-hidden="true" />

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12 md:py-16 text-center">
      <div class="hero-enter mx-auto max-w-3xl">
        <div v-if="eyebrow" class="inline-flex items-center gap-3 mb-4 sm:mb-5">
          <span class="page-hero-rule hidden xs:block h-px w-8" aria-hidden="true" />
          <p class="page-hero-eyebrow text-[11px] sm:text-xs font-semibold tracking-[0.22em] uppercase">
            {{ eyebrow }}
          </p>
          <span class="page-hero-rule hidden xs:block h-px w-8" aria-hidden="true" />
        </div>

        <h1 class="page-hero-title text-3xl sm:text-4xl md:text-5xl font-bold font-serif leading-[1.1] tracking-tight px-1">
          {{ title }}
        </h1>

        <p
          v-if="subtitle"
          class="page-hero-subtitle mt-3 sm:mt-4 text-sm sm:text-base md:text-lg max-w-2xl mx-auto leading-relaxed px-1"
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
/* ─── Modo claro: banner cálido diurno ─── */
.page-hero-base {
  background: linear-gradient(145deg, #fff7ed 0%, #fed7aa 42%, #fdba74 78%, #f59e0b 100%);
}
.page-hero-glow-a {
  background: radial-gradient(circle, rgba(255, 255, 255, 0.7) 0%, transparent 68%);
}
.page-hero-glow-b {
  background: radial-gradient(circle, rgba(251, 191, 36, 0.45) 0%, transparent 70%);
}
.page-hero-glow-c {
  background: radial-gradient(circle, rgba(217, 119, 6, 0.3) 0%, transparent 70%);
}
.page-hero-grain {
  opacity: 0.08;
  mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
  background-size: 180px 180px;
}
.page-hero-edge {
  background: linear-gradient(to right, transparent, rgba(146, 64, 14, 0.25), transparent);
}
.page-hero-rule {
  background-color: rgba(146, 64, 14, 0.35);
}
.page-hero-eyebrow {
  color: rgba(120, 53, 15, 0.85);
}
.page-hero-title {
  color: #451a03;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.35);
}
.page-hero-subtitle {
  color: rgba(69, 26, 3, 0.78);
}

/* ─── Modo noche: banner profundo ─── */
:global(html.dark) .page-hero-base {
  background: linear-gradient(145deg, #3b1f12 0%, #6b3419 45%, #1a0f0a 100%);
}
:global(html.dark) .page-hero-glow-a {
  background: radial-gradient(circle, rgba(251, 191, 36, 0.28) 0%, transparent 68%);
}
:global(html.dark) .page-hero-glow-b {
  background: radial-gradient(circle, rgba(180, 83, 9, 0.35) 0%, transparent 70%);
}
:global(html.dark) .page-hero-glow-c {
  background: radial-gradient(circle, rgba(120, 53, 15, 0.45) 0%, transparent 70%);
}
:global(html.dark) .page-hero-grain {
  opacity: 0.14;
  mix-blend-mode: soft-light;
}
:global(html.dark) .page-hero-edge {
  background: linear-gradient(to right, transparent, rgba(253, 230, 138, 0.35), transparent);
}
:global(html.dark) .page-hero-rule {
  background-color: rgba(253, 230, 138, 0.5);
}
:global(html.dark) .page-hero-eyebrow {
  color: rgba(254, 243, 199, 0.9);
}
:global(html.dark) .page-hero-title {
  color: #ffffff;
  text-shadow: 0 2px 18px rgba(0, 0, 0, 0.35);
}
:global(html.dark) .page-hero-subtitle {
  color: rgba(255, 251, 235, 0.85);
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
