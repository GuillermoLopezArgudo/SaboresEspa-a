<template>
  <div class="min-h-screen bg-amber-50 py-12 px-4 sm:px-6 lg:px-8">
    <!-- Encabezado con efecto de receta -->
    <div class="max-w-4xl mx-auto text-center mb-12">
      <h1
        class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-4">
        Crear Nueva Receta
      </h1>
      <p class="text-lg text-amber-700">Comparte tu creación culinaria con la comunidad</p>
    </div>

    <!-- Botón de regreso -->
    <div class="max-w-4xl mx-auto mb-8">
      <router-link to="/home"
        class="inline-flex items-center px-6 py-3 bg-amber-800 hover:bg-amber-900 text-white rounded-xl transition duration-300 shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd" />
        </svg>
        Volver al inicio
      </router-link>
    </div>

    <!-- Formulario -->
    <form @submit.prevent="submitRecipe"
      class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-amber-200">
      <!-- Sección de información básica -->
      <div class="p-8 border-b border-amber-100 bg-gradient-to-r from-amber-50 to-white">
        <h2 class="text-2xl font-bold text-amber-800 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Información Básica
        </h2>

        <!--Ocultar o Mostrar-->
        <button @click.prevent="showBasicInfo = !showBasicInfo" class="text-amber-600 hover:text-amber-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="showBasicInfo" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </button>

        <!-- Título de la receta -->
        <div class="mb-6">
          <label for="titleRecipe" class="block text-lg font-medium text-amber-700 mb-2">Nombre de la receta*</label>
          <input type="text" id="titleRecipe" v-model="title" required
            class="w-full px-4 py-3 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
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
          <label for="descriptionRecipe" class="block text-lg font-medium text-amber-700 mb-2">Descripción*</label>
          <textarea id="descriptionRecipe" rows="4" v-model="description" required
            class="w-full px-4 py-3 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
            placeholder="Describe tu receta, su origen, características especiales..."></textarea>
        </div>
      </div>

      <!-- Sección de ingredientes -->
      <div class="p-8 border-b border-amber-100">
        <h2 class="text-2xl font-bold text-amber-800 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes
        </h2>

        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="grid md:grid-cols-2 gap-4 mb-4">
          <div>
            <label :for="'ingredient' + index" class="block text-sm font-medium text-amber-700 mb-1">Ingrediente {{
              index
              + 1 }}</label>
            <input :id="'ingredient' + index" v-model="recipebook.ingredients[index]" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Ej: Arroz bomba">
          </div>
          <div>
            <label :for="'quantity' + index" class="block text-sm font-medium text-amber-700 mb-1">Cantidad</label>
            <input :id="'quantity' + index" v-model="recipebook.quantities[index]" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Ej: 300 gramos">
          </div>
        </div>

        <button type="button" @click.prevent="moreIngredients"
          class="mt-4 flex items-center text-amber-600 hover:text-amber-800 transition duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir otro ingrediente
        </button>
      </div>

      <!-- Sección de pasos -->
      <div class="p-8">
        <h2 class="text-2xl font-bold text-amber-800 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Pasos de Preparación
        </h2>

        <div v-for="(step, index) in recipebook.steps" :key="index"
          class="mb-8 p-6 bg-amber-50 rounded-lg border border-amber-200">
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
          class="flex items-center text-amber-600 hover:text-amber-800 transition duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir otro paso
        </button>
      </div>

      <!-- Filtros -->

      <!-- Tipo de comida -->
      <div>
        <legend>Filtro Tipo de comida</legend>
        <div><input type="radio" id="starters" name="tipoComida" value="starters" v-model="tipoComida" /> <label
            for="starters">Entrantes</label></div>
        <div><input type="radio" id="maindishes" name="tipoComida" value="maindishes" v-model="tipoComida" /> <label
            for="maindishes">Platos principales</label></div>
        <div><input type="radio" id="accompaniments" name="tipoComida" value="accompaniments" v-model="tipoComida" />
          <label for="accompaniments">Acompañamientos</label></div>
        <div><input type="radio" id="dessert" name="tipoComida" value="dessert" v-model="tipoComida" /> <label
            for="dessert">Postres</label></div>
        <div><input type="radio" id="soups" name="tipoComida" value="soups" v-model="tipoComida" /> <label
            for="soups">Sopas</label></div>
        <div><input type="radio" id="salads" name="tipoComida" value="salads" v-model="tipoComida" /> <label
            for="salads">Ensaladas</label></div>
        <div><input type="radio" id="sauces" name="tipoComida" value="sauces" v-model="tipoComida" /> <label
            for="sauces">Salsas y aderezos</label></div>
        <div><input type="radio" id="breads" name="tipoComida" value="breads" v-model="tipoComida" /> <label
            for="breads">Panes y masas</label></div>
      </div>

      <!-- CCAA -->
      <div>
        <legend>Filtro CCAA</legend>
        <div><input type="radio" id="andalucia" name="ccaa" v-model="ccaa" value="andalucia" /> <label
            for="andalucia">Andalucía</label></div>
        <div><input type="radio" id="aragon" name="ccaa" v-model="ccaa" value="aragon" /> <label
            for="aragon">Aragón</label></div>
        <div><input type="radio" id="asturias" name="ccaa" v-model="ccaa" value="asturias" /> <label
            for="asturias">Asturias</label></div>
        <div><input type="radio" id="cantabria" name="ccaa" v-model="ccaa" value="cantabria" /> <label
            for="cantabria">Cantabria</label></div>
        <div><input type="radio" id="castillalamancha" name="ccaa" v-model="ccaa" value="castillalamancha" /> <label
            for="castillalamancha">Castilla-LaMancha</label></div>
        <div><input type="radio" id="castillaleon" name="ccaa" v-model="ccaa" value="castillaleon" /> <label
            for="castillaleon">Castilla y León</label></div>
        <div><input type="radio" id="catalunya" name="ccaa" v-model="ccaa" value="catalunya" /> <label
            for="catalunya">Cataluña</label></div>
        <div><input type="radio" id="valencia" name="ccaa" v-model="ccaa" value="valencia" /> <label
            for="valencia">Comunidad Valenciana</label></div>
        <div><input type="radio" id="extremadura" name="ccaa" v-model="ccaa" value="extremadura" /> <label
            for="extremadura">Extremadura</label></div>
        <div><input type="radio" id="galicia" name="ccaa" v-model="ccaa" value="galicia" /> <label
            for="galicia">Galicia</label></div>
        <div><input type="radio" id="baleares" name="ccaa" v-model="ccaa" value="baleares" /> <label
            for="baleares">Islas Baleares</label></div>
        <div><input type="radio" id="canarias" name="ccaa" v-model="ccaa" value="canarias" /> <label
            for="canarias">Islas Canarias</label></div>
        <div><input type="radio" id="larioja" name="ccaa" v-model="ccaa" value="larioja" /> <label for="larioja">La
            Rioja</label></div>
        <div><input type="radio" id="madrid" name="ccaa" v-model="ccaa" value="madrid" /> <label for="madrid">Comunidad
            de Madrid</label></div>
        <div><input type="radio" id="murcia" name="ccaa" v-model="ccaa" value="murcia" /> <label for="murcia">Región de
            Murcia</label></div>
        <div><input type="radio" id="navarra" name="ccaa" v-model="ccaa" value="navarra" /> <label
            for="navarra">Navarra</label></div>
        <div><input type="radio" id="paisvasco" name="ccaa" v-model="ccaa" value="paisvasco" /> <label
            for="paisvasco">País Vasco</label></div>
      </div>

      <!-- Tipo de proteína (permite selección múltiple) -->
      <div>
        <legend>Filtro Tipo de proteína</legend>
        <div><input type="checkbox" id="pollo" value="pollo" v-model="proteinas" /> <label for="pollo">Pollo</label>
        </div>
        <div><input type="checkbox" id="res" value="res" v-model="proteinas" /> <label for="res">Res</label></div>
        <div><input type="checkbox" id="cerdo" value="cerdo" v-model="proteinas" /> <label for="cerdo">Cerdo</label>
        </div>
        <div><input type="checkbox" id="pescado" value="pescado" v-model="proteinas" /> <label
            for="pescado">Pescado</label></div>
        <div><input type="checkbox" id="mariscos" value="mariscos" v-model="proteinas" /> <label
            for="mariscos">Mariscos</label></div>
        <div><input type="checkbox" id="huevo" value="huevo" v-model="proteinas" /> <label for="huevo">Huevo</label>
        </div>
        <div><input type="checkbox" id="vegetariana" value="vegetariana" v-model="proteinas" /> <label
            for="vegetariana">Vegetariana</label></div>
        <div><input type="checkbox" id="vegana" value="vegana" v-model="proteinas" /> <label for="vegana">Vegana</label>
        </div>
      </div>

      <!-- Tiempo de preparación -->
      <div>
        <legend>Filtro Tiempo de preparación</legend>
        <div><input type="radio" id="menos15" name="tiempo" v-model="tiempo" value="menos15" /> <label
            for="menos15">Rápidas (menos de 15 min)</label>
        </div>
        <div><input type="radio" id="15a30" name="tiempo" v-model="tiempo" value="15a30" /> <label for="15a30">15 – 30
            min</label></div>
        <div><input type="radio" id="30a60" name="tiempo" v-model="tiempo" value="30a60" /> <label for="30a60">30 – 60
            min</label></div>
        <div><input type="radio" id="mas60" name="tiempo" v-model="tiempo" value="mas60" /> <label for="mas60">Más de 1
            hora</label></div>
      </div>


      <!-- Botón de enviar -->
      <div class="px-8 pb-8">
        <button type="submit"
          class="w-full py-4 bg-gradient-to-r from-amber-600 to-red-600 hover:from-amber-700 hover:to-red-700 text-white font-bold rounded-lg shadow-lg transition duration-300 transform hover:scale-[1.02] flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Publicar Receta
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { useRouter } from "vue-router";

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
      image: step.image
    })) : [],
    idUser: localStorage.getItem("iduser"),
    token: localStorage.getItem("userToken"),
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: proteinas.value,
    visibility:showBasicInfo.value
  };
  axios.post('http://localhost:5000/create', payload)
    .then(response => {
      console.log(response.data.message);
      router.push({ name: "home" });
    })
    .catch(error => {
      console.log(error);
    });
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
