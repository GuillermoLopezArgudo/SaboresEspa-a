<template>
  <div
    class="w-full bg-white/80 dark:bg-neutral-900 rounded-b-xl shadow-sm  p-3 sm:p-4">
    <div class="flex flex-wrap items-stretch gap-2 sm:gap-3 md:gap-4">

      <!-- Filtro Tipo de Comida -->
      <div class="relative flex-1 min-w-[120px]" ref="tipoRef">
        <button @click="toggleAccordion('tipoComida')"
          class="flex items-center justify-between w-full px-2 py-1.5 sm:px-3 sm:py-2 bg-amber-50 dark:bg-neutral-800 hover:bg-amber-100 dark:hover:bg-neutral-700 text-amber-800 dark:text-amber-200 rounded-lg text-xs sm:text-sm"
          :class="{ 'bg-amber-100 dark:bg-neutral-700': activeAccordion === 'tipoComida' }">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" />
            </svg>
            <span>Tipo</span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 ml-1 transform"
            :class="{ 'rotate-180': activeAccordion === 'tipoComida' }" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          class="absolute z-10 mt-1 w-full bg-white/80 dark:bg-neutral-800 rounded-md shadow-lg border border-amber-200 dark:border-neutral-700  origin-top"
          :class="activeAccordion === 'tipoComida' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-1 space-y-1 max-h-60 overflow-y-auto text-xs sm:text-sm text-neutral-800 dark:text-neutral-100">
            <label v-for="type in foodTypes" :key="type.value"
              class="flex items-center px-2 py-1.5 hover:bg-amber-50 dark:hover:bg-neutral-700 rounded cursor-pointer">
              <input type="radio" name="tipoComida" :value="type.value" v-model="tipoComida"
                class="text-amber-600 focus:ring-amber-500 h-3 w-3">
              <span class="ml-2">{{ type.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Filtro CCAA -->
      <div class="relative flex-1 min-w-[120px]" ref="ccaaRef">
        <button @click="toggleAccordion('ccaa')"
          class="flex items-center justify-between w-full px-2 py-1.5 sm:px-3 sm:py-2 bg-amber-50 dark:bg-neutral-800 hover:bg-amber-100 dark:hover:bg-neutral-700 text-amber-800 dark:text-amber-200 rounded-lg  text-xs sm:text-sm"
          :class="{ 'bg-amber-100 dark:bg-neutral-700': activeAccordion === 'ccaa' }">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Región</span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 ml-1 transform "
            :class="{ 'rotate-180': activeAccordion === 'ccaa' }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          class="absolute z-10 mt-1 w-full bg-white/80 dark:bg-neutral-800 rounded-md shadow-lg border border-amber-200 dark:border-neutral-700 max-h-60 sm:max-h-96 overflow-y-auto  origin-top"
          :class="activeAccordion === 'ccaa' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-1 space-y-1 text-xs sm:text-sm text-neutral-800 dark:text-neutral-100">
            <label v-for="region in regions" :key="region.value"
              class="flex items-center px-2 py-1.5 hover:bg-amber-50 dark:hover:bg-neutral-700 rounded cursor-pointer">
              <input type="radio" name="ccaa" :value="region.value" v-model="ccaa"
                class="text-amber-600 focus:ring-amber-500 h-3 w-3">
              <span class="ml-2">{{ region.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Filtro Proteínas -->
      <div class="relative flex-1 min-w-[120px]" ref="proteinasRef">
        <button @click="toggleAccordion('proteinas')"
          class="flex items-center justify-between w-full px-2 py-1.5 sm:px-3 sm:py-2 bg-amber-50 dark:bg-neutral-800 hover:bg-amber-100 dark:hover:bg-neutral-700 text-amber-800 dark:text-amber-200 rounded-lg  text-xs sm:text-sm"
          :class="{ 'bg-amber-100 dark:bg-neutral-700': activeAccordion === 'proteinas' }">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>Proteínas</span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 ml-1 transform "
            :class="{ 'rotate-180': activeAccordion === 'proteinas' }" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          class="absolute z-10 mt-1 w-full bg-white/80 dark:bg-neutral-800 rounded-md shadow-lg border border-amber-200 dark:border-neutral-700  origin-top"
          :class="activeAccordion === 'proteinas' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-1 space-y-1 max-h-60 overflow-y-auto text-xs sm:text-sm text-neutral-800 dark:text-neutral-100">
            <label v-for="protein in proteins" :key="protein.value"
              class="flex items-center px-2 py-1.5 hover:bg-amber-50 dark:hover:bg-neutral-700 rounded cursor-pointer">
              <input type="checkbox" :value="protein.value" v-model="proteinas"
                class="text-amber-600 focus:ring-amber-500 rounded h-3 w-3">
              <span class="ml-2">{{ protein.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Filtro Tiempo -->
      <div class="relative flex-1 min-w-[120px]" ref="tiempoRef">
        <button @click="toggleAccordion('tiempo')"
          class="flex items-center justify-between w-full px-2 py-1.5 sm:px-3 sm:py-2 bg-amber-50 dark:bg-neutral-800 hover:bg-amber-100 dark:hover:bg-neutral-700 text-amber-800 dark:text-amber-200 rounded-lg  text-xs sm:text-sm"
          :class="{ 'bg-amber-100 dark:bg-neutral-700': activeAccordion === 'tiempo' }">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Tiempo</span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 ml-1 transform "
            :class="{ 'rotate-180': activeAccordion === 'tiempo' }" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          class="absolute z-10 mt-1 w-full bg-white/80 dark:bg-neutral-800 rounded-md shadow-lg border border-amber-200 dark:border-neutral-700 duration-200 origin-top"
          :class="activeAccordion === 'tiempo' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-1 space-y-1 text-xs sm:text-sm text-neutral-800 dark:text-neutral-100">
            <label v-for="time in prepTimes" :key="time.value"
              class="flex items-center px-2 py-1.5 hover:bg-amber-50 dark:hover:bg-neutral-700 rounded cursor-pointer">
              <input type="radio" name="tiempo" :value="time.value" v-model="tiempo"
                class="text-amber-600 focus:ring-amber-500 h-3 w-3">
              <span class="ml-2">{{ time.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Botones de acción -->
      <div class="flex items-stretch gap-2 w-full sm:w-auto">
        <button @click="limpiarFiltros"
          class="flex-1 sm:flex-none px-3 py-1.5 sm:py-2 text-amber-700 dark:text-amber-300 hover:text-amber-900 dark:hover:text-amber-100 flex items-center justify-center text-xs sm:text-sm border border-amber-300 dark:border-neutral-600 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Limpiar
        </button>
        <button @click="buscarFiltros"
          class="flex-1 sm:flex-none px-3 py-1.5 sm:py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg flex items-center justify-center  text-xs sm:text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Buscar
        </button>
      </div>
    </div>

    <!-- Chips -->
    <div class="mt-3 flex flex-wrap gap-2" v-if="filtrosSeleccionados.length > 0">
      <div v-for="(filtro, index) in filtrosSeleccionados" :key="index"
        class="inline-flex items-center px-3 py-1 bg-amber-100 dark:bg-neutral-700 text-amber-800 dark:text-amber-200 rounded-full text-xs sm:text-sm">
        {{ filtro.label }}: {{ filtro.value }}
        <button @click="eliminarFiltro(filtro)"
          class="ml-2 text-amber-600 hover:text-amber-800 dark:hover:text-amber-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, defineEmits, defineProps, watch, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const props = defineProps({
  type: {
    type: String,
    required: true
  },
  category: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['enviarFiltros'])

const activeAccordion = ref('');

const toggleAccordion = (section) => {
  activeAccordion.value = activeAccordion.value === section ? '' : section;

};

const tipoComida = ref('');
const ccaa = ref('');
const tiempo = ref('');
const proteinas = ref([]);
const tipoRef = ref(null);
const ccaaRef = ref(null);
const proteinasRef = ref(null);
const tiempoRef = ref(null);
const darkMode = ref(false);

// Watch para tipoComida (filtro de tipo de comida)
watch(() => props.type, (newType) => {
  if (props.category === 'typeeat' && newType) {
    tipoComida.value = newType;
  }
});

// Watch para ccaa (filtro de región)
watch(() => props.type, (newType) => {
  if (props.category === 'ccaa' && newType) {
    ccaa.value = newType;
  }
});

// Watch para tiempo (filtro de tiempo de preparación)
watch(() => props.type, (newType) => {
  if (props.category === 'time' && newType) {
    tiempo.value = newType;
  }
});

// Watch para proteinas (filtro de proteínas)
watch(() => props.type, (newType) => {
  if (props.category === 'protein' && newType) {
    // Usamos concat para añadir los nuevos valores de proteínas correctamente
    proteinas.value = proteinas.value.concat(newType.split(','));
    console.log(proteinas.value);  // Para depuración
  }
});

// Datos para los filtros
const foodTypes = [
  { value: 'starters', label: 'Entrantes' },
  { value: 'maindishes', label: 'Platos principales' },
  { value: 'accompaniments', label: 'Acompañamientos' },
  { value: 'dessert', label: 'Postres' },
  { value: 'soups', label: 'Sopas' },
  { value: 'salads', label: 'Ensaladas' },
  { value: 'sauces', label: 'Salsas' },
  { value: 'breads', label: 'Panes y masas' }
];

const regions = [
  { value: 'andalucia', label: 'Andalucía' },
  { value: 'aragon', label: 'Aragón' },
  { value: 'asturias', label: 'Asturias' },
  { value: 'cantabria', label: 'Cantabria' },
  { value: 'castillalamancha', label: 'Castilla-La Mancha' },
  { value: 'castillaleon', label: 'Castilla y León' },
  { value: 'catalunya', label: 'Cataluña' },
  { value: 'valencia', label: 'Com. Valenciana' },
  { value: 'extremadura', label: 'Extremadura' },
  { value: 'galicia', label: 'Galicia' },
  { value: 'baleares', label: 'Baleares' },
  { value: 'canarias', label: 'Canarias' },
  { value: 'larioja', label: 'La Rioja' },
  { value: 'madrid', label: 'Madrid' },
  { value: 'murcia', label: 'Murcia' },
  { value: 'navarra', label: 'Navarra' },
  { value: 'paisvasco', label: 'País Vasco' }
];

const proteins = [
  { value: 'pollo', label: 'Pollo' },
  { value: 'res', label: 'Ternera' },
  { value: 'cerdo', label: 'Cerdo / Ibérico' },
  { value: 'cordero', label: 'Cordero' },
  { value: 'conejo', label: 'Conejo' },
  { value: 'pato', label: 'Pato' },
  { value: 'pescado', label: 'Pescado blanco' },
  { value: 'atun', label: 'Atún' },
  { value: 'bacalao', label: 'Bacalao' },
  { value: 'salmon', label: 'Salmón' },
  { value: 'anguila', label: 'Anguila' },
  { value: 'mariscos', label: 'Mariscos' },
  { value: 'pulpo', label: 'Pulpo' },
  { value: 'calamar', label: 'Calamar / Sepia' },
  { value: 'huevo', label: 'Huevo' },
  { value: 'queso', label: 'Queso' },
  { value: 'legumbres', label: 'Legumbres (lentejas, garbanzos)' },
  { value: 'setas', label: 'Setas / Champiñones' },
  { value: 'vegetariana', label: 'Vegetariana' },
  { value: 'vegana', label: 'Vegana' },
];

const prepTimes = [
  { value: "<15'⏱️", label: 'Rápida', description: '<15 minutos' },
  { value: '15-30 ⏱️', label: 'Media', description: '15-30 minutos' },
  { value: "30'-60' ⏱️", label: 'Lenta', description: '30-60 minutos' },
  { value: ">60' ⏱️", label: 'Muy lenta', description: '>1 hora' }
];

// Computed para mostrar los filtros seleccionados
const filtrosSeleccionados = computed(() => {
  const seleccionados = [];
  if (tipoComida.value) {
    const tipo = foodTypes.find(t => t.value === tipoComida.value);
    closeAllAccordions()
    if (tipo) {
      seleccionados.push({ category: 'tipo', label: 'Tipo', value: tipo.label });
    }
  }

  if (ccaa.value) {
    const region = regions.find(r => r.value === ccaa.value);
    closeAllAccordions()
    if (region) {
      seleccionados.push({ category: 'ccaa', label: 'Región', value: region.label });
    }
  }

  if (tiempo.value) {
    const tiempoSel = prepTimes.find(t => t.value === tiempo.value);
    closeAllAccordions()
    if (tiempoSel) {
      seleccionados.push({ category: 'tiempo', label: 'Tiempo', value: tiempoSel.label });
    }
  }

  if (proteinas.value.length > 0) {
    proteinas.value.forEach(p => {
      const proteina = proteins.find(pro => pro.value === p);
      if (proteina) {
        seleccionados.push({ category: 'proteinas', label: 'Proteína', value: proteina.label });
      }
    });
  }

  return seleccionados;
});

const eliminarFiltro = (filtro) => {
  if (filtro.label === 'Tipo') { tipoComida.value = ''; buscarFiltros(); }
  else if (filtro.label === 'Región') { ccaa.value = ''; buscarFiltros(); }
  else if (filtro.label === 'Tiempo') { tiempo.value = ''; buscarFiltros(); }
  else if (filtro.label === 'Proteína') {
    const prot = proteins.find(p => p.label === filtro.value);
    if (prot) {
      proteinas.value = proteinas.value.filter(p => p !== prot.value);
    }
    buscarFiltros()
  }
  if (filtrosSeleccionados.value.length == 0) {
    limpiarFiltros()
  }
};

const limpiarFiltros = () => {

  // Limpiar radio buttons
  document.querySelectorAll('input[type="radio"]').forEach(radio => {
    radio.checked = false;
  });

  // Limpiar checkboxes
  document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.checked = false;
  });
  closeAllAccordions();
  tipoComida.value = "";
  ccaa.value = "";
  tiempo.value = "";
  proteinas.value = [];
  emit('limpiarFiltros');

};

const buscarFiltros = () => {
  const isEmpty = !tipoComida.value && !ccaa.value && !tiempo.value && proteinas.value.length === 0;
  if (isEmpty) {
    limpiarFiltros();
    return;
  }
  closeAllAccordions();
  const payload = {
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: proteinas.value,
  }

  axios.post(`${process.env.VUE_APP_API_URL}/filterRecipe`, payload)
    .then(response => {
      emit('enviarFiltros', { idRecipe: response.data.message, greeting: 'filtred' });
    })
    .catch(error => {
      console.log(error);
    });
}

const closeAllAccordions = () => {
  activeAccordion.value = '';
};

const handleClickOutside = (event) => {
  const refs = {
    tipoComida: tipoRef,
    ccaa: ccaaRef,
    proteinas: proteinasRef,
    tiempo: tiempoRef
  };

  const currentRef = refs[activeAccordion.value];
  if (currentRef?.value && !currentRef.value.contains(event.target)) {
    activeAccordion.value = '';
  }
};

onMounted(() => {
  const savedMode = localStorage.getItem('darkMode');
  if (savedMode !== null) {
    darkMode.value = JSON.parse(savedMode);
    applyDarkMode();
  }

  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  
  document.removeEventListener('click', handleClickOutside);
});

function applyDarkMode() {
  if (darkMode.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

</script>

<style scoped>
/* Transiciones suaves */
.absolute {
  transition: all 0.2s ease-out;
  transform-origin: top center;
}

/* Scroll personalizado */
.max-h-60::-webkit-scrollbar,
.max-h-96::-webkit-scrollbar {
  width: 4px;
}

.max-h-60::-webkit-scrollbar-track,
.max-h-96::-webkit-scrollbar-track {
  background: #fffbeb;
}

.max-h-60::-webkit-scrollbar-thumb,
.max-h-96::-webkit-scrollbar-thumb {
  background-color: #f59e0b;
  border-radius: 2px;
}

/* Efecto hover para los botones de filtro */
button:hover {
  transform: translateY(-1px);
  transition: all 0.2s ease;
}

/* Animación para los chips de filtros */
.inline-flex {
  transition: all 0.2s ease;
}

.inline-flex:hover {
  transform: translateY(-1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Mejorar la legibilidad en móviles */
@media (max-width: 640px) {
  .flex-wrap {
    gap: 0.5rem;
  }

  .relative {
    flex: 1 1 45%;
    min-width: 0;
  }

  button {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0.5rem;
  }
}
</style>