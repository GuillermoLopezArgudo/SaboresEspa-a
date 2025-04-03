<template>
  <div class="container mx-auto mt-8 px-4">
    <h1 class="text-center mb-6 text-4xl font-bold text-orange-600">Crear una Receta</h1>
    
    <!-- Back Button -->
    <router-link to="/home" class="mb-6 inline-block px-6 py-2 text-white bg-gray-600 rounded-lg hover:bg-gray-700 transition duration-300">
      Atrás
    </router-link>
    
    <!-- Formulario -->
    <form @submit.prevent="submitRecipe" class="shadow-lg p-8 rounded-lg bg-white">
      
      <!-- Título de la receta -->
      <div class="mb-6">
        <label for="titleRecipe" class="block text-lg font-semibold text-gray-700">Nombre de la receta</label>
        <input type="text" id="titleRecipe" v-model="title" class="mt-2 p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none" />
      </div>
      
      <!-- Imagen de la receta -->
      <div class="mb-6">
        <label for="imageRecipe" class="block text-lg font-semibold text-gray-700">Imagen de la receta</label>
        <input type="file" id="imageRecipe" @change="handleImageChange" class="mt-2 p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none" />
      </div>
      
      <!-- Video de la receta (opcional) -->
      <div class="mb-6">
        <label for="videoRecipe" class="block text-lg font-semibold text-gray-700">Video de la receta (Opcional)</label>
        <input type="file" id="videoRecipe" @change="handleVideoChange" class="mt-2 p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none" />
      </div>
      
      <!-- Descripción de la receta -->
      <div class="mb-6">
        <label for="descriptionRecipe" class="block text-lg font-semibold text-gray-700">Descripción de la receta</label>
        <textarea id="descriptionRecipe" rows="5" v-model="description" class="mt-2 p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none"></textarea>
      </div>
      
      <!-- Ingredientes + Cantidades -->
      <div class="mb-6">
        <label for="ingredientsRecipe" class="block text-lg font-semibold text-gray-700">Ingredientes + Cantidades</label>
        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="flex mb-4">
          <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente" class="p-3 w-1/2 rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none mr-2" />
          <input v-model="recipebook.quantities[index]" placeholder="Cantidad" class="p-3 w-1/2 rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none" />
        </div>
      </div>
      
      <!-- Añadir más ingredientes -->
      <div class="mb-6">
        <button type="button" @click.prevent="moreIngredients" class="text-blue-600 underline hover:text-blue-700 transition duration-300">
          Añadir más ingredientes
        </button>
      </div>
      
      <!-- Pasos de la receta -->
      <div class="mb-6">
        <label for="stepsRecipe" class="block text-lg font-semibold text-gray-700">Pasos de la receta</label>
        <div v-for="(step, index) in recipebook.steps" :key="index" class="flex flex-col mb-4">
          <input v-model="step.title" placeholder="Título del paso" class="p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none mb-2" />
          <input v-model="step.text" placeholder="Descripción del paso" class="p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none mb-2" />
          <input type="file" @change="handleStepImageChange($event, index)" class="p-3 w-full rounded-lg border border-gray-300 focus:ring-orange-500 focus:outline-none mb-2" />
          <span v-if="step.image" class="text-sm text-gray-500">Imagen seleccionada: {{ step.image.name }}</span>
        </div>
      </div>
      
      <!-- Añadir más pasos -->
      <div class="mb-6">
        <button type="button" @click.prevent="moreSteps" class="text-blue-600 underline hover:text-blue-700 transition duration-300">
          Añadir más pasos
        </button>
      </div>
      
      <!-- Botón de enviar -->
      <div class="d-grid mt-8">
        <input type="submit" value="Crear Receta" class="w-full py-3 bg-orange-600 text-white rounded-lg cursor-pointer hover:bg-orange-500 transition duration-300" />
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
    token: localStorage.getItem("userToken")
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
/* Estilos adicionales si se requieren */
.container {
  max-width: 900px;
}

form {
  background-color: #f9f9f9;
  border-radius: 8px;
}

button {
  color: #007bff;
  text-decoration: underline;
}

button:hover {
  cursor: pointer;
  color: #0056b3;
}

.d-grid {
  margin-top: 20px;
}
</style>
