<template>
    <div class="container mt-4">
      <h1 class="text-center mb-4">Editar Receta</h1>
      <router-link to="/home" class="btn btn-secondary mb-3">Atrás</router-link>
  
      <form @submit.prevent="submitEditeRecipe" class="shadow-lg p-4 rounded bg-white">
        <div class="mb-3">
          <label for="titleRecipe" class="form-label">Nombre de la receta</label>
          <input type="text" id="titleRecipe" v-model="title" class="form-control" required />
        </div>
  
        <div class="mb-3">
          <label for="imageRecipe" class="form-label">Imagen de la receta</label>
          <input type="file" id="imageRecipe" @change="handleImageChange" class="form-control" />
        </div>
  
        <div class="mb-3">
          <label for="videoRecipe" class="form-label">Video de la receta (Opcional)</label>
          <input type="file" id="videoRecipe" @change="handleVideoChange" class="form-control" />
        </div>
  
        <div class="mb-3">
          <label for="descriptionRecipe" class="form-label">Descripción de la receta</label>
          <textarea id="descriptionRecipe" rows="5" v-model="description" class="form-control" required></textarea>
        </div>
        <div class="mb-3">
          <label for="ingredientsRecipe" class="form-label">Ingredientes + Cantidades</label>
          <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="d-flex mb-2">
            <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente" class="form-control me-2" />
            <input v-model="recipebook.quantities[index]" placeholder="Cantidad" class="form-control" />
          </div>
        </div>
  
        <div class="mb-3">
          <button type="button" @click.prevent="moreIngredients" class="btn btn-link p-0">Añadir más ingredientes</button>
        </div>
  
        <div class="d-grid">
          <input type="submit" value="Actualizar Receta" class="btn btn-primary" />
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
  
  // Cargar receta para editar
  onMounted(() => {
    axios.post('http://localhost:5000/viewRecipe', { idrecipe: recipeId })
      .then(response => {
        console.log(response.data.message)
        if (response.data.message) {
          const recipe = response.data.message;
          title.value = recipe.titulo;
          description.value = recipe.descripcion;
          recipebook.ingredients = recipe.ingredientes;
          recipebook.quantities = recipe.cantidades;
          video.value = recipe.video ? `${recipe.video}` : '';
          img.value = recipe.img ? `${recipe.img}`:''
        }
      })
      .catch(error => {
        console.error("Error en la solicitud:", error);
      });
  });
  
  // Función para manejar la selección de imagen
  function handleImageChange(event) {
    img.value = event.target.files[0];
  }
  
  // Función para manejar la selección de video
  function handleVideoChange(event) {
    video.value = event.target.files[0];
  }
  
  // Añadir más ingredientes
  function moreIngredients() {
    recipebook.ingredients.push('');
    recipebook.quantities.push('');
  }
  
  // Enviar la receta editada
  function submitEditeRecipe() {
    const formData = new FormData();
    formData.append('idrecipe', recipeId);
    formData.append('titulo', title.value);
    formData.append('imagen', img.value);
    formData.append('video', video.value);
    formData.append('descripcion', description.value);
    formData.append('ingredientes', JSON.stringify(recipebook.ingredients));
    formData.append('cantidades', JSON.stringify(recipebook.quantities));
    formData.append('userToken', localStorage.getItem('userToken'));
    
    axios.post('http://localhost:5000/editeRecipe', formData)
      .then(response => {
        console.log(response.data.message);
        router.push({ name: 'home' }); // Redirigir al Home después de actualizar
      })
      .catch(error => {
        console.error(error);
      });
  }
  </script>
  