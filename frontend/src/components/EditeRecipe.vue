<template>
  <div class="container mx-auto mt-4 px-4">
    <h1 class="text-center mb-4 text-blue-600 text-3xl font-bold">Editar Receta</h1>
    <router-link to="/home"
      class="inline-block px-4 py-2 text-white bg-gray-500 rounded hover:bg-gray-600 mb-3">Atrás</router-link>

    <form @submit.prevent="submitEditeRecipe" class="shadow-lg p-6 rounded-lg bg-white">
      <!-- Nombre de la receta -->
      <div class="mb-4">
        <label for="titleRecipe" class="block text-lg font-semibold">Nombre de la receta</label>
        <input type="text" id="titleRecipe" v-model="title"
          class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" required />
      </div>

      <!-- Imagen de la receta -->
      <div class="mb-4">
        <label for="imageRecipe" class="block text-lg font-semibold">Imagen de la receta</label>
        <input type="file" id="imageRecipe" @change="handleImageChange"
          class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
      </div>

      <!-- Video de la receta -->
      <div class="mb-4">
        <label for="videoRecipe" class="block text-lg font-semibold">Video de la receta (Opcional)</label>
        <input type="file" id="videoRecipe" @change="handleVideoChange"
          class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
      </div>

      <!-- Descripción -->
      <div class="mb-4">
        <label for="descriptionRecipe" class="block text-lg font-semibold">Descripción de la receta</label>
        <textarea id="descriptionRecipe" rows="5" v-model="description"
          class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" required></textarea>
      </div>

      <!-- Ingredientes -->
      <div class="mb-4">
        <label class="block text-lg font-semibold">Ingredientes + Cantidades</label>
        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="flex mb-2">
          <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente"
            class="p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500 mr-2" />
          <input v-model="recipebook.quantities[index]" placeholder="Cantidad"
            class="p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500" />
        </div>
      </div>

      <!-- Pasos de preparación -->
      <div class="mb-4">
        <label class="block text-lg font-semibold">Pasos de preparación</label>
        <div v-for="(step, index) in recipebook.steps" :key="index" class="flex mb-2">
          <input v-model="recipebook.steps[index].title" placeholder="Titulo"
            class="p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500 mr-2">
          <input v-model="recipebook.steps[index].description" placeholder="Descripcion"
            class="p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500" />
          <input type="file" @change="handleStepImageChange($event, index)"
            class="p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
        </div>
      </div>

      <!-- Botón para enviar -->
      <div class="d-grid mt-6">
        <input type="submit" value="Actualizar Receta"
          class="w-full py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-500" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';

const route = useRoute();
const router = useRouter();
const recipeId = route.query.id;

const title = ref('');
const description = ref('');
const video = ref('');
const image = ref('');

const recipebook = reactive({
  ingredients: [],
  quantities: [],
  steps: []
});

onMounted(() => {
  axios.post('http://localhost:5000/viewRecipe', { idrecipe: recipeId })
    .then(response => {
      title.value = response.data.recipe_list[0].title
      description.value = response.data.recipe_list[0].description
      image.value = response.data.recipe_list[0].image
      video.value = response.data.recipe_list[0].video

      response.data.ingredient_list.forEach(element => {
        recipebook.ingredients.push(element.ingredients)
        recipebook.quantities.push(element.quantity)
      });

      response.data.step_list.forEach(element => {
        recipebook.steps.push(element)
      });

    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
    });
});

function handleImageChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      image.value = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function handleVideoChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      video.value = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function handleStepImageChange(event, index) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      recipebook.steps[index].image = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function submitEditeRecipe() {
  const payload = {
    idrecipe: recipeId,
    title: title.value,
    image: typeof image.value === 'object' ? image.value : { base64: null, name: image.value },
    video: typeof video.value === 'object' ? video.value : { base64: null, name: video.value },
    description: description.value,
    ingredients: recipebook.ingredients.length > 0 ? recipebook.ingredients : [],
    quantities: recipebook.quantities.length > 0 ? recipebook.quantities : [],
    steps: recipebook.steps.length > 0 ? recipebook.steps.map(step => ({
      title: step.title,
      description: step.description,
      image: typeof step.image === 'object' ? step.image : { base64: null, name: step.image }
    })) : [],
    idUser: localStorage.getItem("iduser"),
    token: localStorage.getItem("userToken")
  };

  axios.post('http://localhost:5000/editeRecipe', payload)
    .then(response => {
      console.log(response.data.message);
      router.push({ name: 'home' });
    })
    .catch(error => {
      console.error(error);
    });
}
</script>

<style scoped>
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