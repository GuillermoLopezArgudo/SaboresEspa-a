<template>
  <div class="w-full md:w-72 flex-shrink-0">
    <div class="bg-white rounded-lg shadow-lg p-4 border border-amber-200 bg-gradient-to-b from-amber-50 to-white">
      <h2 class="text-2xl font-bold text-amber-800 mb-4 font-serif flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-amber-600" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Filtrar Recetas
      </h2>

      <!-- Acordeón -->
      <div class="space-y-3">
        <!-- Tipo de comida -->
        <div class="border-b border-amber-100 pb-1">
          <button @click="toggleAccordion('tipoComida')"
            class="w-full flex justify-between items-center py-3 px-2 text-left font-medium text-amber-800 hover:bg-amber-50 rounded-lg transition-colors duration-200 focus:outline-none">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-amber-600" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" />
              </svg>
              <span>Tipo de comida</span>
            </div>
            <svg class="w-5 h-5 transform transition-transform duration-300 text-amber-500"
              :class="{ 'rotate-180': activeAccordion === 'tipoComida' }" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div class="overflow-hidden transition-all duration-300 ease-in-out"
            :class="activeAccordion === 'tipoComida' ? 'max-h-96' : 'max-h-0'">
            <div class="py-2 space-y-2 pl-2 ml-6">
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="starters" name="tipoComida" value="starters"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="starters" class="ml-2 text-amber-700">Entrantes</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="maindishes" name="tipoComida" value="maindishes"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="maindishes" class="ml-2 text-amber-700">Platos principales</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="accompaniments" name="tipoComida" value="accompaniments"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="accompaniments" class="ml-2 text-amber-700">Acompañamientos</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="dessert" name="tipoComida" value="dessert"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="dessert" class="ml-2 text-amber-700">Postres</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="soups" name="tipoComida" value="soups"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="soups" class="ml-2 text-amber-700">Sopas</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="salads" name="tipoComida" value="salads"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="salads" class="ml-2 text-amber-700">Ensaladas</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="sauces" name="tipoComida" value="sauces"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="sauces" class="ml-2 text-amber-700">Salsas y aderezos</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="breads" name="tipoComida" value="breads"
                  class="text-amber-600 focus:ring-amber-500" v-model="tipoComida" />
                <label for="breads" class="ml-2 text-amber-700">Panes y masas</label>
              </div>
            </div>
          </div>
        </div>

        <!-- CCAA -->
        <div class="border-b border-amber-100 pb-1">
          <button @click="toggleAccordion('ccaa')"
            class="w-full flex justify-between items-center py-3 px-2 text-left font-medium text-amber-800 hover:bg-amber-50 rounded-lg transition-colors duration-200 focus:outline-none">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-amber-600" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Comunidad Autónoma</span>
            </div>
            <svg class="w-5 h-5 transform transition-transform duration-300 text-amber-500"
              :class="{ 'rotate-180': activeAccordion === 'ccaa' }" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div class="overflow-hidden transition-all duration-300 ease-in-out"
            :class="activeAccordion === 'ccaa' ? 'max-h-96' : 'max-h-0'">
            <div class="py-2 space-y-2 pl-2 ml-6">
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="andalucia" name="ccaa" value="andalucia"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="andalucia" class="ml-2 text-amber-700">Andalucía</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="aragon" name="ccaa" value="aragon" class="text-amber-600 focus:ring-amber-500"
                  v-model="ccaa" />
                <label for="aragon" class="ml-2 text-amber-700">Aragón</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="asturias" name="ccaa" value="asturias"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="asturias" class="ml-2 text-amber-700">Asturias</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="cantabria" name="ccaa" value="cantabria"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="cantabria" class="ml-2 text-amber-700">Cantabria</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="castillalamancha" name="ccaa" value="castillalamancha"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="castillalamancha" class="ml-2 text-amber-700">Castilla-La Mancha</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="castillaleon" name="ccaa" value="castillaleon"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="castillaleon" class="ml-2 text-amber-700">Castilla y León</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="catalunya" name="ccaa" value="catalunya"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="catalunya" class="ml-2 text-amber-700">Cataluña</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="valencia" name="ccaa" value="valencia"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="valencia" class="ml-2 text-amber-700">Comunidad Valenciana</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="extremadura" name="ccaa" value="extremadura"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="extremadura" class="ml-2 text-amber-700">Extremadura</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="galicia" name="ccaa" value="galicia" class="text-amber-600 focus:ring-amber-500"
                  v-model="ccaa" />
                <label for="galicia" class="ml-2 text-amber-700">Galicia</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="baleares" name="ccaa" value="baleares"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="baleares" class="ml-2 text-amber-700">Islas Baleares</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="canarias" name="ccaa" value="canarias"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="canarias" class="ml-2 text-amber-700">Islas Canarias</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="larioja" name="ccaa" value="larioja" class="text-amber-600 focus:ring-amber-500"
                  v-model="ccaa" />
                <label for="larioja" class="ml-2 text-amber-700">La Rioja</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="madrid" name="ccaa" value="madrid" class="text-amber-600 focus:ring-amber-500"
                  v-model="ccaa" />
                <label for="madrid" class="ml-2 text-amber-700">Comunidad de Madrid</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="murcia" name="ccaa" value="murcia" class="text-amber-600 focus:ring-amber-500"
                  v-model="ccaa" />
                <label for="murcia" class="ml-2 text-amber-700">Región de Murcia</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="navarra" name="ccaa" value="navarra" class="text-amber-600 focus:ring-amber-500"
                  v-model="ccaa" />
                <label for="navarra" class="ml-2 text-amber-700">Navarra</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="paisvasco" name="ccaa" value="paisvasco"
                  class="text-amber-600 focus:ring-amber-500" v-model="ccaa" />
                <label for="paisvasco" class="ml-2 text-amber-700">País Vasco</label>
              </div>
            </div>
          </div>
        </div>

        <!-- Tipo de proteína -->
        <div class="border-b border-amber-100 pb-1">
          <button @click="toggleAccordion('proteinas')"
            class="w-full flex justify-between items-center py-3 px-2 text-left font-medium text-amber-800 hover:bg-amber-50 rounded-lg transition-colors duration-200 focus:outline-none">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-amber-600" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span>Tipo de proteína</span>
            </div>
            <svg class="w-5 h-5 transform transition-transform duration-300 text-amber-500"
              :class="{ 'rotate-180': activeAccordion === 'proteinas' }" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div class="overflow-hidden transition-all duration-300 ease-in-out"
            :class="activeAccordion === 'proteinas' ? 'max-h-96' : 'max-h-0'">
            <div class="py-2 space-y-2 pl-2 ml-6">
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="pollo" name="proteinas" value="pollo"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="pollo" class="ml-2 text-amber-700">Pollo</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="res" name="proteinas" value="res"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="res" class="ml-2 text-amber-700">Res</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="cerdo" name="proteinas" value="cerdo"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="cerdo" class="ml-2 text-amber-700">Cerdo</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="pescado" name="proteinas" value="pescado"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="pescado" class="ml-2 text-amber-700">Pescado</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="mariscos" name="proteinas" value="mariscos"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="mariscos" class="ml-2 text-amber-700">Mariscos</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="huevo" name="proteinas" value="huevo"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="huevo" class="ml-2 text-amber-700">Huevo</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="vegetariana" name="proteinas" value="vegetariana"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="vegetariana" class="ml-2 text-amber-700">Vegetariana</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="checkbox" id="vegana" name="proteinas" value="vegana"
                  class="text-amber-600 focus:ring-amber-500 rounded" v-model="proteinas" />
                <label for="vegana" class="ml-2 text-amber-700">Vegana</label>
              </div>
            </div>
          </div>
        </div>

        <!-- Tiempo de preparación -->
        <div class="border-b border-amber-100 pb-1">
          <button @click="toggleAccordion('tiempo')"
            class="w-full flex justify-between items-center py-3 px-2 text-left font-medium text-amber-800 hover:bg-amber-50 rounded-lg transition-colors duration-200 focus:outline-none">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-amber-600" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Tiempo de preparación</span>
            </div>
            <svg class="w-5 h-5 transform transition-transform duration-300 text-amber-500"
              :class="{ 'rotate-180': activeAccordion === 'tiempo' }" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div class="overflow-hidden transition-all duration-300 ease-in-out"
            :class="activeAccordion === 'tiempo' ? 'max-h-96' : 'max-h-0'">
            <div class="py-2 space-y-2 pl-2 ml-6">
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="menos15" name="tiempo" value="menos15"
                  class="text-amber-600 focus:ring-amber-500" v-model="tiempo" />
                <label for="menos15" class="ml-2 text-amber-700">Rápidas (menos de 15 min)</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="15a30" name="tiempo" value="15a30" class="text-amber-600 focus:ring-amber-500"
                  v-model="tiempo" />
                <label for="15a30" class="ml-2 text-amber-700">15 – 30 min</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="30a60" name="tiempo" value="30a60" class="text-amber-600 focus:ring-amber-500"
                  v-model="tiempo" />
                <label for="30a60" class="ml-2 text-amber-700">30 – 60 min</label>
              </div>
              <div class="flex items-center py-1 hover:bg-amber-50 rounded px-2">
                <input type="radio" id="mas60" name="tiempo" value="mas60" class="text-amber-600 focus:ring-amber-500"
                  v-model="tiempo" />
                <label for="mas60" class="ml-2 text-amber-700">Más de 1 hora</label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Botón para limpiar filtros -->
      <button @click="limpiarFiltros"
        class="mt-6 w-full py-2 px-4 bg-amber-100 hover:bg-amber-200 text-amber-800 rounded-lg font-medium transition-colors duration-300 flex items-center justify-center shadow-sm hover:shadow-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Limpiar filtros
      </button>

      <!-- Botón para buscar recetas -->
      <button @click="buscarFiltros"
        class="mt-6 w-full py-2 px-4 bg-amber-100 hover:bg-amber-200 text-amber-800 rounded-lg font-medium transition-colors duration-300 flex items-center justify-center shadow-sm hover:shadow-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        Buscar
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const activeAccordion = ref('');
const tipoComida = ref('')
const ccaa = ref('')
const tiempo = ref('')
const proteinas = ref([]);

const toggleAccordion = (section) => {
  activeAccordion.value = activeAccordion.value === section ? '' : section;
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
      console.log(response.data.message);
    })
    .catch(error => {
      console.log(error);
    });
}   
</script>

<style scoped>
/* Transiciones mejoradas para el acordeón */
.overflow-hidden {
  transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Estilo para las flechas del acordeón con animación más suave */
.rotate-180 {
  transform: rotate(180deg);
  transition: transform 0.3s ease-out;
}

/* Efecto hover para los items del filtro */
.hover\:bg-amber-50:hover {
  background-color: rgba(254, 243, 199, 0.5);
  transition: background-color 0.2s ease;
}

/* Estilo para los checkboxes y radios personalizados */
input[type="checkbox"],
input[type="radio"] {
  accent-color: #d97706;
}

/* Sombra suave al pasar el mouse en los botones */
.hover\:shadow-md:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.3s ease;
}
</style>