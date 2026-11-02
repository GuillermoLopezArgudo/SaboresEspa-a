<template>
  <div>
    <PageHero
      title="Crear receta"
      subtitle="Comparte tu creación culinaria con la comunidad"
    >
      <router-link
        to="/"
        class="inline-flex items-center px-4 py-2 rounded-full bg-white/15 hover:bg-white/25 text-white text-sm font-medium border border-white/20 transition"
      >
        ← Volver al recetario
      </router-link>
    </PageHero>

    <div class="max-w-4xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
    <form @submit.prevent="submitRecipe" class="space-y-4 sm:space-y-5">
      <!-- Sección de información básica -->
      <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
        <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50 flex items-center justify-between gap-3">
          <h2 class="font-serif text-lg sm:text-xl font-bold text-amber-950">Información básica</h2>
          <button
            type="button"
            class="inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-semibold transition"
            :class="showBasicInfo
              ? 'border-emerald-300 bg-emerald-50 text-emerald-800'
              : 'border-amber-300 bg-amber-50 text-amber-800'"
            @click.prevent="showBasicInfo = !showBasicInfo"
          >
            {{ showBasicInfo ? 'Pública' : 'Oculta' }}
          </button>
        </div>
        <div class="p-4 sm:p-6 md:p-8">
        <!-- Título de la receta -->
        <div class="mb-6">
          <label for="titleRecipe" class="block text-sm font-medium text-amber-900 mb-1.5">Nombre de la receta*</label>
          <input type="text" id="titleRecipe" v-model="title" required
            class="w-full px-4 py-3 rounded-xl border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400"
            placeholder="Ej: Paella Valenciana">
        </div>

        <!-- Imagen y video -->
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Imagen de la receta -->
          <div>
            <label for="imageRecipe" class="block text-lg font-medium text-amber-700 mb-2">Imagen principal*</label>
            <div
              class="relative border-2 border-dashed border-amber-300 rounded-lg p-6 text-center hover:border-amber-400 transition duration-300 bg-amber-50">
              <input type="file" id="imageRecipe" @change="handleImageChange" required
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-amber-500" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="mt-2 text-sm text-amber-600">
                <span class="font-medium">Haz clic para subir</span> o arrastra una imagen
              </p>
              <p v-if="image" class="mt-1 text-xs text-amber-500">{{ image.name }}</p>
            </div>
          </div>

          <!-- Video de la receta (opcional) -->
          <div>
            <label for="videoRecipe" class="block text-lg font-medium text-amber-700 mb-2">Video (Opcional)</label>
            <div
              class="relative border-2 border-dashed border-amber-300 rounded-lg p-6 text-center hover:border-amber-400 transition duration-300 bg-amber-50">
              <input type="file" id="videoRecipe" @change="handleVideoChange"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-amber-500" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p class="mt-2 text-sm text-amber-600">
                <span class="font-medium">Haz clic para subir</span> un video tutorial
              </p>
              <p v-if="video" class="mt-1 text-xs text-amber-500">{{ video.name }}</p>
            </div>
          </div>
        </div>

        <!-- Descripción de la receta -->
        <div class="mt-6">
          <label for="descriptionRecipe" class="block text-sm font-medium text-amber-900 mb-1.5">Descripción*</label>
          <textarea id="descriptionRecipe" rows="4" v-model="description" required
            class="w-full px-4 py-3 rounded-xl border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400"
            placeholder="Describe tu receta, su origen, características especiales..."></textarea>
        </div>
        </div>
      </section>

      <!-- Sección de ingredientes -->
      <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
        <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50">
          <h2 class="font-serif text-lg sm:text-xl font-bold text-amber-950">Ingredientes</h2>
        </div>
        <div class="p-4 sm:p-6 md:p-8">

        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="grid grid-cols-1 sm:grid-cols-12 gap-3 sm:gap-4 mb-4">
          <div class="sm:col-span-5">
            <label :for="'ingredient' + index" class="block text-sm font-medium text-amber-700 mb-1">Ingrediente {{
              index + 1 }}</label>
            <div class="flex">
              <input :id="'ingredient' + index" v-model="recipebook.ingredients[index]" required
                class="w-full px-4 py-2 rounded-l-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
                placeholder="Ej: Arroz bomba">
              <button @click.prevent="removeIngredient(index)"
                class="px-3 bg-red-100 text-red-600 rounded-r-lg border border-l-0 border-amber-300 hover:bg-red-200 transition duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <div class="sm:col-span-5">
            <label :for="'quantity' + index" class="block text-sm font-medium text-amber-700 mb-1">Cantidad</label>
            <input :id="'quantity' + index" v-model="recipebook.quantities[index]" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Ej: 300 gramos">
          </div>
          <div class="hidden sm:block sm:col-span-2" />
        </div>

        <button type="button" @click.prevent="moreIngredients"
          class="mt-4 inline-flex items-center rounded-full border border-amber-300 px-4 py-2 text-sm font-medium text-amber-900 hover:bg-amber-50 transition">
          + Añadir ingrediente
        </button>
        </div>
      </section>

      <!-- Sección de pasos -->
      <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
        <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50">
          <h2 class="font-serif text-lg sm:text-xl font-bold text-amber-950">Pasos de preparación</h2>
        </div>
        <div class="p-4 sm:p-6 md:p-8">
        <div v-for="(step, index) in recipebook.steps" :key="index"
          class="mb-5 p-4 sm:p-5 bg-amber-50/60 rounded-xl border border-amber-200 relative">
          <button @click.prevent="removeStep(index)"
            class="absolute top-2 right-2 p-1 text-red-600 hover:text-red-800 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <h3 class="text-lg font-semibold text-amber-700 mb-3">Paso {{ index + 1 }}</h3>

          <div class="mb-4">
            <label :for="'stepTitle' + index" class="block text-sm font-medium text-amber-700 mb-1">Título del
              paso</label>
            <input :id="'stepTitle' + index" v-model="step.title" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Ej: Preparar el sofrito">
          </div>

          <div class="mb-4">
            <label :for="'stepDesc' + index" class="block text-sm font-medium text-amber-700 mb-1">Descripción
              detallada</label>
            <textarea :id="'stepDesc' + index" v-model="step.text" rows="3" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Describe este paso con detalle..."></textarea>
          </div>

          <div>
            <label :for="'stepImage' + index" class="block text-sm font-medium text-amber-700 mb-1">Imagen
              (Opcional)</label>
            <div class="relative">
              <input type="file" :id="'stepImage' + index" @change="handleStepImageChange($event, index)"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <div
                class="flex items-center justify-between px-4 py-2 bg-white rounded-lg border border-amber-300 shadow-sm">
                <span class="text-sm text-amber-600 truncate">
                  {{ step.image ? step.image.name : 'Seleccionar imagen...' }}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <button type="button" @click.prevent="moreSteps"
          class="inline-flex items-center rounded-full border border-amber-300 px-4 py-2 text-sm font-medium text-amber-900 hover:bg-amber-50 transition">
          + Añadir paso
        </button>
        </div>
      </section>

      <!-- Sección de Filtros -->
      <section class="rounded-2xl border border-amber-200 bg-white shadow-sm overflow-hidden">
        <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-amber-100 bg-amber-50">
          <h2 class="font-serif text-lg sm:text-xl font-bold text-amber-950">Categorías</h2>
          <p class="text-sm text-amber-800/70 mt-0.5">Ayudan a encontrar tu receta en el recetario</p>
        </div>
        <div class="p-4 sm:p-6 md:p-8 space-y-4">
          <!-- Tipo de comida -->
          <div class="bg-white rounded-xl shadow-sm border border-amber-200 overflow-hidden">
            <button type="button" @click="toggleAccordion('foodType')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700">Tipo de comida</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 transform transition-transform duration-200"
                :class="{ 'rotate-180': activeAccordion === 'foodType' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'foodType' }">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label v-for="(type, index) in foodTypes" :key="index"
                  class="flex items-center p-2 rounded-lg hover:bg-amber-50 cursor-pointer">
                  <input type="radio" name="tipoComida" :value="type.value" v-model="tipoComida"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300">
                  <span class="ml-3 text-sm text-amber-800">{{ type.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Comunidad Autónoma -->
          <div class="bg-white rounded-xl shadow-sm border border-amber-200 overflow-hidden">
            <button type="button" @click="toggleAccordion('region')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700">Comunidad Autónoma</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 transform transition-transform duration-200"
                :class="{ 'rotate-180': activeAccordion === 'region' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'region' }">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label v-for="(region, index) in regions" :key="index"
                  class="flex items-center p-2 rounded-lg hover:bg-amber-50 cursor-pointer">
                  <input type="radio" name="ccaa" :value="region.value" v-model="ccaa"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300">
                  <span class="ml-3 text-sm text-amber-800">{{ region.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Tipo de proteína -->
          <div class="bg-white rounded-xl shadow-sm border border-amber-200 overflow-hidden">
            <button type="button" @click="toggleAccordion('protein')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700">Tipo de proteína</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 transform transition-transform duration-200"
                :class="{ 'rotate-180': activeAccordion === 'protein' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'protein' }">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label v-for="(protein, index) in proteins" :key="index"
                  class="flex items-center p-2 rounded-lg hover:bg-amber-50 cursor-pointer">
                  <input type="checkbox" :value="protein.value" v-model="proteinas"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300 rounded">
                  <span class="ml-3 text-sm text-amber-800">{{ protein.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Tiempo de preparación -->
          <div class="bg-white rounded-xl shadow-sm border border-amber-200 overflow-hidden">
            <button type="button" @click="toggleAccordion('time')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700">Tiempo de preparación</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 transform transition-transform duration-200"
                :class="{ 'rotate-180': activeAccordion === 'time' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'time' }">
              <div class="grid grid-cols-2 gap-4">
                <label v-for="(time, index) in prepTimes" :key="index"
                  class="flex items-center p-3 bg-amber-50 rounded-lg border border-amber-200 cursor-pointer">
                  <input type="radio" name="tiempo" :value="time.value" v-model="tiempo"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300">
                  <div class="ml-3">
                    <span class="block text-sm font-medium text-amber-800">{{ time.label }}</span>
                    <span class="block text-xs text-amber-600">{{ time.description }}</span>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </section>

      <button
        type="submit"
        class="w-full rounded-full bg-amber-800 hover:bg-amber-900 text-white font-semibold py-3.5 shadow-sm transition"
      >
        Publicar receta
      </button>
    </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { apiUrl } from '../api';
import { useRouter } from "vue-router";
import PageHero from './PageHero.vue';

const title = ref('');
const image = ref('');
const video = ref('');
const description = ref('');
const recipebook = reactive({
  ingredients: [],
  quantities: [],
  steps: []
});
const router = useRouter();
const userToken = ref(localStorage.getItem("userToken"));
const tipoComida = ref('')
const ccaa = ref('')
const tiempo = ref('')
const proteinas = ref([]);
const showBasicInfo = ref(true);

if (userToken.value == null) {
  router.push({ name: "login" });
}

function handleImageChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      image.value = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }
}

function handleVideoChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      video.value = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }
}

function moreIngredients() {
  recipebook.ingredients.push('');
  recipebook.quantities.push('');
}

function moreSteps() {
  recipebook.steps.push({ title: '', text: '', image: null });
}

function handleStepImageChange(event, index) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      recipebook.steps[index].image = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }
}

function submitRecipe() {
  const payload = {
    title: title.value,
    image: image.value,
    video: video.value,
    description: description.value,
    ingredients: recipebook.ingredients.length > 0 ? recipebook.ingredients : [],
    quantities: recipebook.quantities.length > 0 ? recipebook.quantities : [],
    steps: recipebook.steps.length > 0 ? recipebook.steps.map(step => ({
      title: step.title,
      text: step.text,
      description: step.text,
      image: step.image
    })) : [],
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: proteinas.value,
    visibility: showBasicInfo.value
  };
  axios.post(apiUrl('/create'), payload)
    .then(() => {
      router.push({ name: "home" });
    })
    .catch((error) => {
      alert(error.response?.data?.message || 'No se pudo crear la receta');
    });
}

const activeAccordion = ref(null);

const toggleAccordion = (section) => {
  activeAccordion.value = activeAccordion.value === section ? null : section;
};

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

// Función para eliminar ingrediente
function removeIngredient(index) {

    recipebook.ingredients.splice(index, 1);
    recipebook.quantities.splice(index, 1);

}

// Función para eliminar paso
function removeStep(index) {

    recipebook.steps.splice(index, 1);

}
</script>

<style scoped>
/* Efectos adicionales */
form {
  transition: all 0.3s ease;
}

form:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Animación para los pasos */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-enter-active {
  animation: fadeIn 0.5s ease-out;
}
</style>
