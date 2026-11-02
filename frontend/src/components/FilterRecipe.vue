<template>
  <div class="filter-bar sticky top-14 sm:top-16 z-40 border-b border-amber-200/80 bg-amber-50/95 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-2.5 sm:py-3">
      <!-- Barra principal -->
      <div class="flex items-center gap-2 min-w-0">
        <div class="filter-label hidden sm:flex items-center gap-1.5 text-amber-900/70 shrink-0 pr-2 border-r border-amber-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <span class="text-xs font-semibold tracking-wide uppercase">Filtrar</span>
        </div>

        <!-- Triggers desktop / tablet -->
        <div class="hidden md:flex flex-1 flex-wrap items-center gap-2 min-w-0">
          <div
            v-for="panel in panels"
            :key="panel.id"
            class="relative"
            :data-filter-panel="panel.id"
          >
            <button
              type="button"
              @click.stop="toggleAccordion(panel.id)"
              class="group inline-flex items-center gap-1.5 max-w-[14rem] px-3 py-2 rounded-full text-sm font-medium border transition"
              :class="triggerClass(panel)"
            >
              <span class="truncate">{{ triggerLabel(panel) }}</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-3.5 w-3.5 shrink-0 opacity-70 transition-transform"
                :class="{ 'rotate-180': activeAccordion === panel.id }"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div
              v-show="activeAccordion === panel.id"
              class="filter-dropdown absolute left-0 top-full mt-2 z-50 w-64 rounded-2xl border border-amber-200 bg-white shadow-xl shadow-amber-900/10 overflow-hidden"
              @click.stop
            >
              <div class="filter-dropdown-head px-3 py-2 border-b border-amber-100 bg-amber-50/80">
                <p class="text-xs font-semibold uppercase tracking-wide text-amber-800/80">{{ panel.title }}</p>
              </div>
              <div class="max-h-72 overflow-y-auto p-2 filter-scroll">
                <template v-if="panel.mode === 'radio'">
                  <button
                    v-for="opt in panel.options"
                    :key="opt.value"
                    type="button"
                    class="w-full text-left px-3 py-2.5 rounded-xl text-sm transition flex items-center justify-between gap-2"
                    :class="panel.model.value === opt.value
                      ? 'bg-amber-700 text-white'
                      : 'text-amber-900 hover:bg-amber-50'"
                    @click="selectRadio(panel, opt.value)"
                  >
                    <span>
                      {{ opt.label }}
                      <span v-if="opt.description" class="block text-xs opacity-70">{{ opt.description }}</span>
                    </span>
                    <span v-if="panel.model.value === opt.value" class="text-xs">✓</span>
                  </button>
                </template>
                <template v-else>
                  <button
                    v-for="opt in panel.options"
                    :key="opt.value"
                    type="button"
                    class="w-full text-left px-3 py-2.5 rounded-xl text-sm transition flex items-center justify-between gap-2"
                    :class="panel.model.value.includes(opt.value)
                      ? 'bg-amber-700 text-white'
                      : 'text-amber-900 hover:bg-amber-50'"
                    @click="toggleCheck(panel, opt.value)"
                  >
                    <span>{{ opt.label }}</span>
                    <span v-if="panel.model.value.includes(opt.value)" class="text-xs">✓</span>
                  </button>
                </template>
              </div>
            </div>
          </div>
        </div>

        <!-- Botón móvil: abre sheet -->
        <button
          type="button"
          class="filter-mobile-btn md:hidden inline-flex items-center gap-2 px-3 py-2 rounded-full border border-amber-300 bg-white text-amber-900 text-sm font-medium shadow-sm"
          @click="mobileOpen = true"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filtros
          <span
            v-if="filtrosSeleccionados.length"
            class="min-w-[1.25rem] h-5 px-1 rounded-full bg-amber-700 text-white text-xs flex items-center justify-center"
          >
            {{ filtrosSeleccionados.length }}
          </span>
        </button>

        <div class="ml-auto flex items-center gap-2 shrink-0">
          <button
            v-if="filtrosSeleccionados.length"
            type="button"
            class="inline-flex px-3 py-2 text-sm text-amber-800/80 hover:text-amber-950"
            @click="limpiarFiltros"
          >
            Limpiar
          </button>
        </div>
      </div>

      <!-- Chips activos -->
      <div v-if="filtrosSeleccionados.length" class="mt-2.5 flex flex-wrap gap-1.5">
        <button
          v-for="(filtro, index) in filtrosSeleccionados"
          :key="index"
          type="button"
          class="filter-chip inline-flex items-center gap-1.5 pl-2.5 pr-1.5 py-1 rounded-full bg-white border border-amber-200 text-amber-900 text-xs font-medium shadow-sm hover:border-amber-400 transition"
          @click="eliminarFiltro(filtro)"
          :title="'Quitar ' + filtro.value"
        >
          <span class="text-amber-600/80">{{ filtro.label }}</span>
          <span>{{ filtro.value }}</span>
          <span class="inline-flex h-5 w-5 items-center justify-center rounded-full hover:bg-amber-100 text-amber-700">×</span>
        </button>
      </div>
    </div>

    <!-- Mobile bottom sheet -->
    <Teleport to="body">
      <div v-if="mobileOpen" class="md:hidden fixed inset-0 z-[60]">
        <div class="absolute inset-0 bg-stone-900/40" @click="mobileOpen = false" />
        <div class="filter-sheet absolute inset-x-0 bottom-0 max-h-[85vh] rounded-t-3xl bg-amber-50 shadow-2xl flex flex-col overflow-hidden animate-sheet">
          <div class="filter-sheet-head flex items-center justify-between px-5 py-4 border-b border-amber-200">
            <div>
              <p class="text-lg font-semibold text-amber-950 font-serif">Filtros</p>
              <p class="text-xs text-amber-800/70">Afiná el recetario a tu gusto</p>
            </div>
            <button type="button" class="filter-sheet-close h-9 w-9 rounded-full bg-white border border-amber-200 text-amber-900" @click="mobileOpen = false">×</button>
          </div>

          <div class="flex-1 overflow-y-auto px-4 py-3 space-y-4 filter-scroll">
            <section v-for="panel in panels" :key="'m-' + panel.id" class="filter-sheet-panel rounded-2xl bg-white border border-amber-100 p-3">
              <h3 class="text-xs font-semibold uppercase tracking-wide text-amber-800/70 mb-2">{{ panel.title }}</h3>
              <div class="flex flex-wrap gap-2">
                <template v-if="panel.mode === 'radio'">
                  <button
                    v-for="opt in panel.options"
                    :key="'m-' + opt.value"
                    type="button"
                    class="px-3 py-1.5 rounded-full text-sm border transition"
                    :class="panel.model.value === opt.value
                      ? 'bg-amber-800 text-white border-amber-800'
                      : 'bg-amber-50 text-amber-900 border-amber-200'"
                    @click="selectRadio(panel, opt.value)"
                  >
                    {{ opt.label }}
                  </button>
                </template>
                <template v-else>
                  <button
                    v-for="opt in panel.options"
                    :key="'m-' + opt.value"
                    type="button"
                    class="px-3 py-1.5 rounded-full text-sm border transition"
                    :class="panel.model.value.includes(opt.value)
                      ? 'bg-amber-800 text-white border-amber-800'
                      : 'bg-amber-50 text-amber-900 border-amber-200'"
                    @click="toggleCheck(panel, opt.value)"
                  >
                    {{ opt.label }}
                  </button>
                </template>
              </div>
            </section>
          </div>

          <div class="filter-sheet-foot flex gap-2 p-4 border-t border-amber-200 bg-white">
            <button
              type="button"
              class="flex-1 py-3 rounded-xl border border-amber-300 text-amber-900 font-medium"
              @click="limpiarFiltros"
            >
              Limpiar
            </button>
            <button
              type="button"
              class="flex-1 py-3 rounded-xl bg-amber-800 text-white font-semibold"
              @click="mobileOpen = false"
            >
              Listo
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, onBeforeUnmount } from 'vue';
import {
  foodTypes,
  regions,
  proteins,
  prepTimes,
} from '../utils/filterOptions';

const props = defineProps({
  criteria: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['aplicarFiltros', 'limpiarFiltros']);

const activeAccordion = ref('');
const mobileOpen = ref(false);
let debounceTimer = null;
let syncingFromParent = false;

function closeAccordion() {
  activeAccordion.value = '';
}

function onDocumentPointerDown(event) {
  if (!activeAccordion.value) return;
  const openId = activeAccordion.value;
  const panel = document.querySelector(`[data-filter-panel="${openId}"]`);
  if (panel && panel.contains(event.target)) return;
  closeAccordion();
}

onMounted(() => {
  document.addEventListener('pointerdown', onDocumentPointerDown, true);
});

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', onDocumentPointerDown, true);
});

const tipoComida = ref('');
const ccaa = ref('');
const tiempo = ref('');
const proteinas = ref([]);

function applyCriteriaFromParent(criteria) {
  syncingFromParent = true;
  tipoComida.value = criteria?.typeeat || '';
  ccaa.value = criteria?.ccaa || '';
  tiempo.value = criteria?.time || '';
  proteinas.value = Array.isArray(criteria?.proteins) ? [...criteria.proteins] : [];
  queueMicrotask(() => {
    syncingFromParent = false;
  });
}

watch(
  () => props.criteria,
  (criteria) => {
    applyCriteriaFromParent(criteria);
  },
  { deep: true, immediate: true }
);

const panels = computed(() => [
  { id: 'tipoComida', title: 'Tipo de plato', mode: 'radio', model: tipoComida, options: foodTypes, placeholder: 'Tipo' },
  { id: 'ccaa', title: 'Región', mode: 'radio', model: ccaa, options: regions, placeholder: 'Región' },
  { id: 'proteinas', title: 'Proteína', mode: 'check', model: proteinas, options: proteins, placeholder: 'Proteína' },
  { id: 'tiempo', title: 'Tiempo', mode: 'radio', model: tiempo, options: prepTimes, placeholder: 'Tiempo' },
]);

const filtrosSeleccionados = computed(() => {
  const seleccionados = [];
  if (tipoComida.value) {
    const tipo = foodTypes.find((t) => t.value === tipoComida.value);
    if (tipo) seleccionados.push({ category: 'tipo', label: 'Tipo', value: tipo.label });
  }
  if (ccaa.value) {
    const region = regions.find((r) => r.value === ccaa.value);
    if (region) seleccionados.push({ category: 'ccaa', label: 'Región', value: region.label });
  }
  if (tiempo.value) {
    const tiempoSel = prepTimes.find((t) => t.value === tiempo.value);
    if (tiempoSel) seleccionados.push({ category: 'tiempo', label: 'Tiempo', value: tiempoSel.label });
  }
  if (Array.isArray(proteinas.value) && proteinas.value.length) {
    proteinas.value.forEach((p) => {
      const proteina = proteins.find((pro) => pro.value === p);
      if (proteina) {
        seleccionados.push({
          category: 'proteinas',
          label: 'Proteína',
          value: proteina.label,
          key: proteina.value,
        });
      }
    });
  }
  return seleccionados;
});

function triggerLabel(panel) {
  if (panel.mode === 'radio') {
    if (!panel.model.value) return panel.placeholder;
    return panel.options.find((o) => o.value === panel.model.value)?.label || panel.placeholder;
  }
  if (!panel.model.value.length) return panel.placeholder;
  if (panel.model.value.length === 1) {
    return panel.options.find((o) => o.value === panel.model.value[0])?.label || panel.placeholder;
  }
  return `${panel.placeholder} · ${panel.model.value.length}`;
}

function triggerClass(panel) {
  const active =
    panel.mode === 'radio' ? Boolean(panel.model.value) : panel.model.value.length > 0;
  const open = activeAccordion.value === panel.id;
  if (active) {
    return 'filter-trigger filter-trigger-active bg-amber-800 text-white border-amber-800 shadow-sm';
  }
  if (open) {
    return 'filter-trigger filter-trigger-open bg-white text-amber-900 border-amber-400 shadow-sm';
  }
  return 'filter-trigger bg-white/80 text-amber-900 border-amber-200 hover:border-amber-400';
}

function toggleAccordion(section) {
  activeAccordion.value = activeAccordion.value === section ? '' : section;
}

function hasActiveFilters() {
  return Boolean(
    tipoComida.value ||
      ccaa.value ||
      tiempo.value ||
      (Array.isArray(proteinas.value) && proteinas.value.length)
  );
}

function selectRadio(panel, value) {
  panel.model.value = panel.model.value === value ? '' : value;
  closeAccordion();
  scheduleSearch(0);
}

function toggleCheck(panel, value) {
  const list = [...panel.model.value];
  const idx = list.indexOf(value);
  if (idx >= 0) list.splice(idx, 1);
  else list.push(value);
  panel.model.value = list;
  // Agrupa clicks rápidos en proteínas
  scheduleSearch(60);
}

function eliminarFiltro(filtro) {
  switch (filtro.category) {
    case 'tipo':
      tipoComida.value = '';
      break;
    case 'ccaa':
      ccaa.value = '';
      break;
    case 'tiempo':
      tiempo.value = '';
      break;
    case 'proteinas':
      proteinas.value = proteinas.value.filter((p) => p !== (filtro.key || filtro.value));
      break;
  }
  scheduleSearch(0);
}

function limpiarFiltros() {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
    debounceTimer = null;
  }
  tipoComida.value = '';
  ccaa.value = '';
  tiempo.value = '';
  proteinas.value = [];
  activeAccordion.value = '';
  emit('limpiarFiltros');
}

function scheduleSearch(delayMs = 0) {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    debounceTimer = null;
    emitirFiltros();
  }, delayMs);
}

function emitirFiltros() {
  if (syncingFromParent) return;
  if (!hasActiveFilters()) {
    limpiarFiltros();
    return;
  }
  emit('aplicarFiltros', {
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: [...proteinas.value],
  });
}
</script>

<style scoped>
.filter-scroll::-webkit-scrollbar {
  width: 6px;
}
.filter-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.filter-scroll::-webkit-scrollbar-thumb {
  background-color: #d97706;
  border-radius: 999px;
}

@keyframes sheet-up {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
.animate-sheet {
  animation: sheet-up 0.28s ease-out;
}

:global(html.dark) .filter-bar {
  background-color: rgb(28 20 16 / 0.94) !important;
  border-color: #4a372c !important;
}
:global(html.dark) .filter-label {
  color: rgb(253 230 138 / 0.75) !important;
  border-color: #4a372c !important;
}
:global(html.dark) .filter-trigger {
  background-color: #2a211c !important;
  border-color: #5c4638 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .filter-trigger:hover {
  border-color: #b45309 !important;
  background-color: #3d2e24 !important;
}
:global(html.dark) .filter-trigger-open {
  border-color: #d97706 !important;
  background-color: #3d2e24 !important;
}
:global(html.dark) .filter-trigger-active {
  background-color: #d97706 !important;
  border-color: #d97706 !important;
  color: #1c1410 !important;
}
:global(html.dark) .filter-dropdown {
  background-color: #2a211c !important;
  border-color: #5c4638 !important;
}
:global(html.dark) .filter-dropdown-head {
  background-color: #1c1410 !important;
  border-color: #4a372c !important;
}
:global(html.dark) .filter-mobile-btn {
  background-color: #2a211c !important;
  border-color: #5c4638 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .filter-chip {
  background-color: #2a211c !important;
  border-color: #5c4638 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .filter-sheet {
  background-color: #1c1410 !important;
}
:global(html.dark) .filter-sheet-head {
  border-color: #4a372c !important;
}
:global(html.dark) .filter-sheet-close {
  background-color: #2a211c !important;
  border-color: #5c4638 !important;
  color: #fef3c7 !important;
}
:global(html.dark) .filter-sheet-panel {
  background-color: #2a211c !important;
  border-color: #4a372c !important;
}
:global(html.dark) .filter-sheet-foot {
  background-color: #2a211c !important;
  border-color: #4a372c !important;
}
</style>
