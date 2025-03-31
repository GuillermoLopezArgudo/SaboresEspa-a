<template>
    <div class="container mt-4">
        <h1 class="text-center mb-4">Crear una Receta</h1>

        <router-link to="/home" class="btn btn-secondary mb-3">Atrás</router-link>

        <form @submit.prevent="submitRecipe" class="shadow-lg p-4 rounded bg-white">
            <div class="mb-3">
                <label for="titleRecipe" class="form-label">Nombre de la receta</label>
                <input type="text" id="titleRecipe" v-model="title" class="form-control" required />
            </div>

            <div class="mb-3">
                <label for="imageRecipe" class="form-label">Imagen de la receta</label>
                <input type="file" id="imageRecipe" @change="handleImageChange" class="form-control" required />
            </div>

            <div class="mb-3">
                <label for="videoRecipe" class="form-label">Video de la receta (Opcional)</label>
                <input type="file" id="videoRecipe" @change="handleVideoChange" class="form-control" />
            </div>

            <div class="mb-3">
                <label for="descriptionRecipe" class="form-label">Descripción de la receta</label>
                <textarea id="descriptionRecipe" rows="5" v-model="description" class="form-control"
                    required></textarea>
            </div>
            <div class="mb-3">
                <label for="ingredientsRecipe" class="form-label">Ingredientes + Cantidades</label>
                <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="d-flex mb-2">
                    <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente"
                        class="form-control me-2" />
                    <input v-model="recipebook.quantities[index]" placeholder="Cantidad" class="form-control" />
                </div>
            </div>

            <div class="mb-3">
                <button type="button" @click.prevent="moreIngredients" class="btn btn-link p-0">Añadir más
                    ingredientes</button>
            </div>

            <div class="d-grid">
                <input type="submit" value="Crear Receta" class="btn btn-primary" />
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { useRouter } from "vue-router";

const title = ref('');
const img = ref('');
const video = ref('');
const description = ref('');
const recipebook = reactive({
    ingredients: [],
    quantities: []
});
const router = useRouter();
const comentarios = ref([]);
const userToken = ref(localStorage.getItem("userToken"));

//Si no existe el token en el localstorage lo vuelve a la pagina de login
if (userToken.value == null) {
    router.push({ name: "login" });
}

//Mete la imagen dentro de lo obtenido de la seleccion de la img
function handleImageChange(event) {
    const file = event.target.files[0];
    img.value = file;
}

//Mete el video dentro de lo obtenido de la seleccion de el video
function handleVideoChange(event) {
    const file = event.target.files[0];
    video.value = file;
}

//Mete los ingredientes y las cantidades de los arrays
function moreIngredients() {
    recipebook.ingredients.push('');
    recipebook.quantities.push('');
}

//Cuando pulsa en enviar crea un objeto formData en el cual se mete todos los valores obtenidos en el formulario
//Llamamos al back por referencia /create, con el argumento de formData si la respuesta es correcta nos devolvera un mensaje y nevegamos el home
function submitRecipe() {
    const formData = new FormData();
    formData.append('titulo', title.value);
    formData.append('imagen', img.value);
    formData.append('video', video.value);
    formData.append('descripcion', description.value);
    formData.append('ingredientes', JSON.stringify(recipebook.ingredients));
    formData.append('cantidades', JSON.stringify(recipebook.quantities));
    formData.append('idUser', localStorage.getItem("iduser"));
    formData.append('opcion', JSON.stringify(comentarios.value));
    formData.append('userToken', localStorage.getItem("userToken"));

    
    axios.post('http://localhost:5000/create', formData)
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

h1 {
    color: #007bff;
}

input[type="text"],
input[type="file"],
textarea,
select {
    border-radius: 5px;
}

input[type="submit"],
button {
    border-radius: 5px;
}

button {
    color: #007bff;
    text-decoration: underline;
}

button:hover {
    cursor: pointer;
    color: #0056b3;
}

.form-check-label {
    font-weight: 600;
}

.d-grid {
    margin-top: 20px;
}
</style>
