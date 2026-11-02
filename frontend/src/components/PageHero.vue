<template>
  <header class="page-hero relative overflow-hidden" :class="isDark ? 'page-hero--night' : 'page-hero--day'">
    <div class="page-hero__bg absolute inset-0" aria-hidden="true" />
    <div class="page-hero__glow page-hero__glow--a absolute -top-24 left-1/2 -translate-x-1/2 h-[28rem] w-[42rem] rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
    <div class="page-hero__glow page-hero__glow--b absolute -bottom-24 -left-10 h-72 w-72 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
    <div class="page-hero__edge absolute inset-x-0 bottom-0 h-px" aria-hidden="true" />

    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12 md:py-16 text-center">
      <div class="hero-enter mx-auto max-w-3xl">
        <div v-if="eyebrow" class="inline-flex items-center gap-3 mb-4 sm:mb-5">
          <span class="page-hero__rule hidden xs:block h-px w-8" aria-hidden="true" />
          <p class="page-hero__eyebrow text-[11px] sm:text-xs font-semibold tracking-[0.22em] uppercase">
            {{ eyebrow }}
          </p>
          <span class="page-hero__rule hidden xs:block h-px w-8" aria-hidden="true" />
        </div>

        <h1 class="page-hero__title text-3xl sm:text-4xl md:text-5xl font-bold font-serif leading-[1.1] tracking-tight px-1">
          {{ title }}
        </h1>

        <p
          v-if="subtitle"
          class="page-hero__subtitle mt-3 sm:mt-4 text-sm sm:text-base md:text-lg max-w-2xl mx-auto leading-relaxed px-1"
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
import { useTheme } from '../utils/theme'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  eyebrow: { type: String, default: 'Sabores España' },
})

const { isDark } = useTheme()
</script>

<style scoped>
/* ── Día ── */
.page-hero--day .page-hero__bg {
  background: linear-gradient(145deg, #fff7ed 0%, #fdba74 55%, #f59e0b 100%);
}
.page-hero--day .page-hero__glow--a {
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, transparent 68%);
}
.page-hero--day .page-hero__glow--b {
  background: radial-gradient(circle, rgba(251, 191, 36, 0.45) 0%, transparent 70%);
}
.page-hero--day .page-hero__edge {
  background: linear-gradient(to right, transparent, rgba(120, 53, 15, 0.28), transparent);
}
.page-hero--day .page-hero__rule {
  background: rgba(120, 53, 15, 0.4);
}
.page-hero--day .page-hero__eyebrow {
  color: #78350f;
}
.page-hero--day .page-hero__title {
  color: #451a03;
}
.page-hero--day .page-hero__subtitle {
  color: rgba(69, 26, 3, 0.8);
}

/* ── Noche: cálida e iluminada (no apagón) ── */
.page-hero--night .page-hero__bg {
  background: linear-gradient(145deg, #ea580c 0%, #f59e0b 42%, #9a3412 100%);
}
.page-hero--night .page-hero__glow--a {
  background: radial-gradient(circle, rgba(254, 243, 199, 0.55) 0%, transparent 68%);
}
.page-hero--night .page-hero__glow--b {
  background: radial-gradient(circle, rgba(253, 224, 71, 0.45) 0%, transparent 70%);
}
.page-hero--night .page-hero__edge {
  background: linear-gradient(to right, transparent, rgba(254, 243, 199, 0.45), transparent);
}
.page-hero--night .page-hero__rule {
  background: rgba(254, 243, 199, 0.55);
}
.page-hero--night .page-hero__eyebrow {
  color: #fef3c7 !important;
}
.page-hero--night .page-hero__title {
  color: #ffffff !important;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.45);
}
.page-hero--night .page-hero__subtitle {
  color: #fef3c7 !important;
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
