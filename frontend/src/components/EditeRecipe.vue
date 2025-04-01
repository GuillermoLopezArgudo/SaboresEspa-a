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
            }else{
                let parsedArrayIngredientes= JSON.parse(response.data.message.ingredients)
                let parsedArrayQuantities= JSON.parse(response.data.message.quatities)
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