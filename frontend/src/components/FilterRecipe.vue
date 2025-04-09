<template>
  <div class="w-full bg-white rounded-xl shadow-sm border border-amber-200 p-4">
    <div class="flex flex-wrap gap-4">
      <!-- Filtro Tipo de Comida -->
      <div class="relative">
        <button 
          @click="toggleAccordion('tipoComida')"
          class="flex items-center px-3 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg transition-colors"
          :class="{ 'bg-amber-100': activeAccordion === 'tipoComida' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" />
          </svg>
          Tipo
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform" 
               :class="{ 'rotate-180': activeAccordion === 'tipoComida' }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div class="absolute z-10 mt-1 w-56 bg-white rounded-md shadow-lg border border-amber-200 transition-all duration-200 origin-top"
             :class="activeAccordion === 'tipoComida' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-2 space-y-1">
            <label v-for="type in foodTypes" :key="type.value" class="flex items-center px-3 py-2 hover:bg-amber-50 rounded cursor-pointer">
              <input type="radio" name="tipoComida" :value="type.value" v-model="tipoComida" class="text-amber-600 focus:ring-amber-500">
              <span class="ml-2 text-sm text-amber-800">{{ type.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Filtro CCAA -->
      <div class="relative">
        <button 
          @click="toggleAccordion('ccaa')"
          class="flex items-center px-3 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg transition-colors"
          :class="{ 'bg-amber-100': activeAccordion === 'ccaa' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Región
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform" 
               :class="{ 'rotate-180': activeAccordion === 'ccaa' }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div class="absolute z-10 mt-1 w-56 bg-white rounded-md shadow-lg border border-amber-200 max-h-96 overflow-y-auto transition-all duration-200 origin-top"
             :class="activeAccordion === 'ccaa' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-2 space-y-1">
            <label v-for="region in regions" :key="region.value" class="flex items-center px-3 py-2 hover:bg-amber-50 rounded cursor-pointer">
              <input type="radio" name="ccaa" :value="region.value" v-model="ccaa" class="text-amber-600 focus:ring-amber-500">
              <span class="ml-2 text-sm text-amber-800">{{ region.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Filtro Proteínas -->
      <div class="relative">
        <button 
          @click="toggleAccordion('proteinas')"
          class="flex items-center px-3 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg transition-colors"
          :class="{ 'bg-amber-100': activeAccordion === 'proteinas' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Proteínas
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform" 
               :class="{ 'rotate-180': activeAccordion === 'proteinas' }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div class="absolute z-10 mt-1 w-56 bg-white rounded-md shadow-lg border border-amber-200 transition-all duration-200 origin-top"
             :class="activeAccordion === 'proteinas' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-2 space-y-1">
            <label v-for="protein in proteins" :key="protein.value" class="flex items-center px-3 py-2 hover:bg-amber-50 rounded cursor-pointer">
              <input type="checkbox" :value="protein.value" v-model="proteinas" class="text-amber-600 focus:ring-amber-500 rounded">
              <span class="ml-2 text-sm text-amber-800">{{ protein.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Filtro Tiempo -->
      <div class="relative">
        <button 
          @click="toggleAccordion('tiempo')"
          class="flex items-center px-3 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg transition-colors"
          :class="{ 'bg-amber-100': activeAccordion === 'tiempo' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Tiempo
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform" 
               :class="{ 'rotate-180': activeAccordion === 'tiempo' }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div class="absolute z-10 mt-1 w-56 bg-white rounded-md shadow-lg border border-amber-200 transition-all duration-200 origin-top"
             :class="activeAccordion === 'tiempo' ? 'scale-y-100 opacity-100' : 'scale-y-95 opacity-0 pointer-events-none'">
          <div class="p-2 space-y-1">
            <label v-for="time in prepTimes" :key="time.value" class="flex items-center px-3 py-2 hover:bg-amber-50 rounded cursor-pointer">
              <input type="radio" name="tiempo" :value="time.value" v-model="tiempo" class="text-amber-600 focus:ring-amber-500">
              <span class="ml-2 text-sm text-amber-800">{{ time.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Botones de acción -->
      <div class="flex items-center gap-2 ml-auto">
        <button @click="limpiarFiltros" class="px-3 py-2 text-amber-700 hover:text-amber-900 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Limpiar
        </button>
        <button @click="buscarFiltros" class="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg flex items-center transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Buscar
        </button>
      </div>
    </div>

    <!-- Filtros seleccionados (chips) -->
    <div class="mt-3 flex flex-wrap gap-2" v-if="filtrosSeleccionados.length > 0">
      <div v-for="(filtro, index) in filtrosSeleccionados" :key="index" 
           class="inline-flex items-center px-3 py-1 bg-amber-100 text-amber-800 rounded-full text-sm">
        {{ filtro.label }}: {{ filtro.value }}
        <button @click="eliminarFiltro(filtro)" class="ml-2 text-amber-600 hover:text-amber-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed,defineEmits } from 'vue';
import axios from 'axios';

const emit = defineEmits(['enviarIdRecipe'])

const activeAccordion = ref('');

const toggleAccordion = (section) => {
  activeAccordion.value = activeAccordion.value === section ? '' : section;
};

const tipoComida = ref('');
const ccaa = ref('');
const tiempo = ref('');
const proteinas = ref([]);

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
  { value: 'res', label: 'Res / Ternera' },
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
  { value: 'menos15', label: 'Rápida', description: '<15 minutos' },
  { value: '15a30', label: 'Media', description: '15-30 minutos' },
  { value: '30a60', label: 'Lenta', description: '30-60 minutos' },
  { value: 'mas60', label: 'Muy lenta', description: '>1 hora' }
];

// Computed para mostrar los filtros seleccionados
const filtrosSeleccionados = computed(() => {
  const seleccionados = [];
  
  if (tipoComida.value) {
    const tipo = foodTypes.find(t => t.value === tipoComida.value);
    seleccionados.push({ category: 'tipo', label: 'Tipo', value: tipo.label });
  }
  
  if (ccaa.value) {
    const region = regions.find(r => r.value === ccaa.value);
    seleccionados.push({ category: 'ccaa', label: 'Región', value: region.label });
  }
  
  if (tiempo.value) {
    const tiempoSel = prepTimes.find(t => t.value === tiempo.value);
    seleccionados.push({ category: 'tiempo', label: 'Tiempo', value: tiempoSel.label });
  }
  
  if (proteinas.value.length > 0) {
    proteinas.value.forEach(p => {
      const proteina = proteins.find(pro => pro.value === p);
      seleccionados.push({ category: 'proteinas', label: 'Proteína', value: proteina.label });
    });
  }
  
  return seleccionados;
});

const eliminarFiltro = (filtro) => {
  switch(filtro.category) {
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
      proteinas.value = proteinas.value.filter(p => p !== filtro.value.toLowerCase());
      break;
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
  tipoComida.value= "";
  ccaa.value="";
  tiempo.value="";
  proteinas.value=[];
  emit('limpiarFiltros');

};

const buscarFiltros = () => {
  const payload = {
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: proteinas.value,
  }
  
  axios.post('http://localhost:5000/filterRecipe', payload)
    .then(response => {
      emit('enviarIdRecipe', response.data.message)
    })
    .catch(error => {
      console.log(error);
    });
} 
</script>

<style scoped>
/* Transiciones suaves */
.absolute {
  transition: all 0.2s ease-out;
  transform-origin: top center;
}

/* Scroll personalizado */
.max-h-96::-webkit-scrollbar {
  width: 6px;
}

.max-h-96::-webkit-scrollbar-track {
  background: #fffbeb;
}

.max-h-96::-webkit-scrollbar-thumb {
  background-color: #f59e0b;
  border-radius: 3px;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>