<template>
    <div class="container mx-auto mt-4 px-4">
      <h1 class="text-center mb-4 text-blue-600 text-3xl font-bold">Editar Receta</h1>
      <router-link to="/home" class="inline-block px-4 py-2 text-white bg-gray-500 rounded hover:bg-gray-600 mb-3">Atrás</router-link>
      <form @submit.prevent="submitEditeRecipe" class="shadow-lg p-6 rounded-lg bg-white">
        <div class="mb-4">
          <label for="titleRecipe" class="block text-lg font-semibold">Nombre de la receta</label>
          <input type="text" id="titleRecipe" v-model="title" class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" required />
        </div>
        <div class="mb-4">
          <label for="imageRecipe" class="block text-lg font-semibold">Imagen de la receta</label>
          <input type="file" id="imageRecipe" @change="handleImageChange" class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
        </div>
        <div class="mb-4">
          <label for="videoRecipe" class="block text-lg font-semibold">Video de la receta (Opcional)</label>
          <input type="file" id="videoRecipe" @change="handleVideoChange" class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
        </div>
        <div class="mb-4">
          <label for="descriptionRecipe" class="block text-lg font-semibold">Descripción de la receta</label>
          <textarea id="descriptionRecipe" rows="5" v-model="description" class="mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" required></textarea>
        </div>
        <div class="mb-4">
          <label for="ingredientsRecipe" class="block text-lg font-semibold">Ingredientes + Cantidades</label>
          <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="flex mb-2">
            <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente" class="p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500 mr-2" />
            <input v-model="recipebook.quantities[index]" placeholder="Cantidad" class="p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500" />
          </div>
        </div>
        <div class="mb-4">
          <button type="button" @click.prevent="moreIngredients" class="text-blue-600 underline p-0">Añadir más ingredientes</button>
        </div>
        <div class="d-grid mt-6">
          <input type="submit" value="Actualizar Receta" class="w-full py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-500" />
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
  const img = ref('');
  
  const recipebook = reactive({
      ingredients: [],
      quantities: []
  });
  
  onMounted(() => {
      axios.post('http://localhost:5000/viewRecipe', { idrecipe: recipeId })
          .then(response => {
              if (response.data.message) {
                  const recipe = response.data.message;
                  title.value = recipe.title;
                  description.value = recipe.description;
                  video.value = recipe.video ? `${recipe.video}` : '';
                  img.value = recipe.image ? `${recipe.image}` : ''
              }
              if (response.data.message.quatities[0] == "[]") {
                  recipebook.ingredients = "";
                  recipebook.quantities = "";
              } else {
                  let parsedArrayIngredientes = JSON.parse(response.data.message.ingredients)
                  let parsedArrayQuantities = JSON.parse(response.data.message.quatities)
                  parsedArrayIngredientes.forEach(element => {
                      recipebook.ingredients.push(element)
                  });
                  parsedArrayQuantities.forEach(element => {
                      recipebook.quantities.push(element)
                  });
                  console.log(recipebook.ingredients)
              }
          })
          .catch(error => {
              console.error("Error en la solicitud:", error);
          });
  });
  
  function handleImageChange(event) {
      img.value = event.target.files[0];
  }
  
  function handleVideoChange(event) {
      video.value = event.target.files[0];
  }
  
  function moreIngredients() {
      recipebook.ingredients = []
      recipebook.quantities = []
      recipebook.ingredients.push('');
      recipebook.quantities.push('');
  }
  
  function submitEditeRecipe() {
      const formData = new FormData();
      formData.append('idrecipe', recipeId);
      formData.append('titulo', title.value);
      formData.append('imagen', img.value);
      formData.append('video', video.value);
      formData.append('descripcion', description.value);
      if (recipebook.ingredients.length === 0) {
          formData.append('ingredientes', JSON.stringify([]));
      } else {
          formData.append('ingredientes', JSON.stringify(recipebook.ingredients));
      }
      if (recipebook.quantities.length === 0) {
          formData.append('cantidades', JSON.stringify([]));
      } else {
          formData.append('cantidades', JSON.stringify(recipebook.quantities));
      }
      formData.append('ingredientes', JSON.stringify(recipebook.ingredients));
      formData.append('cantidades', JSON.stringify(recipebook.quantities));
  
      formData.append('userToken', localStorage.getItem('userToken'));
  
  
      axios.post('http://localhost:5000/editeRecipe', formData)
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
  