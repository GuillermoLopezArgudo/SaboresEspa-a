<template>
  <div class="container mx-auto mt-4 px-4">
    <h1 class="text-center mb-4 text-blue-600 text-3xl font-bold">Crear una Receta</h1>
    <router-link to="/home"
      class="btn btn-secondary mb-3 inline-block px-4 py-2 text-white bg-gray-500 rounded hover:bg-gray-600">Atrás</router-link>
    <form @submit.prevent="submitRecipe" class="shadow-lg p-6 rounded-lg bg-white">
      <div class="mb-4">
        <label for="titleRecipe" class="block text-lg font-semibold">Nombre de la receta</label>
        <input type="text" id="titleRecipe" v-model="title"
          class="form-control mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
      </div>
      <div class="mb-4">
        <label for="imageRecipe" class="block text-lg font-semibold">Imagen de la receta</label>
        <input type="file" id="imageRecipe" @change="handleImageChange"
          class="form-control mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
      </div>
      <div class="mb-4">
        <label for="videoRecipe" class="block text-lg font-semibold">Video de la receta (Opcional)</label>
        <input type="file" id="videoRecipe" @change="handleVideoChange"
          class="form-control mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500" />
      </div>
      <div class="mb-4">
        <label for="descriptionRecipe" class="block text-lg font-semibold">Descripción de la receta</label>
        <textarea id="descriptionRecipe" rows="5" v-model="description"
          class="form-control mt-2 p-2 w-full rounded border border-gray-300 focus:ring-blue-500"></textarea>
      </div>
      <div class="mb-4">
        <label for="ingredientsRecipe" class="block text-lg font-semibold">Ingredientes + Cantidades</label>
        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="flex mb-2">
          <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente"
            class="form-control p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500 mr-2" />
          <input v-model="recipebook.quantities[index]" placeholder="Cantidad"
            class="form-control p-2 w-1/2 rounded border border-gray-300 focus:ring-blue-500" />
        </div>
      </div>
      <div class="mb-4">
        <button type="button" @click.prevent="moreIngredients" class="text-blue-600 underline p-0">Añadir más
          ingredientes</button>
      </div>
      <div class="d-grid mt-6">
        <input type="submit" value="Crear Receta"
          class="w-full py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-500" />
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
  quantities: []
});
const router = useRouter();
const userToken = ref(localStorage.getItem("userToken"));

//Si no existe el token en el localstorage lo vuelve a la pagina de login
if (userToken.value == null) {
  router.push({ name: "login" });
}

//Mete la imagen dentro de lo obtenido de la seleccion de la img
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

//Mete el video dentro de lo obtenido de la seleccion de el video
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

//Mete los ingredientes y las cantidades de los arrays
function moreIngredients() {
  recipebook.ingredients.push('');
  recipebook.quantities.push('');
}

//Cuando pulsa en enviar crea un objeto formData en el cual se mete todos los valores obtenidos en el formulario
//Llamamos al back por referencia /create, con el argumento de formData si la respuesta es correcta nos devolvera un mensaje y nevegamos el home
function submitRecipe() {

  const payload = {
    title: title.value,
    image: image.value,
    video: video.value,
    description: description.value,
    ingredients: recipebook.ingredients.length > 0 ? recipebook.ingredients : [],
    quantities: recipebook.quantities.length > 0 ? recipebook.quantities : [],
    idUser: localStorage.getItem("iduser"),
    token: localStorage.getItem("userToken")
  }
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