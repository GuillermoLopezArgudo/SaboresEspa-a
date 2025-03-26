<template>
    <h1>WELCOME A CREATE</h1>
    <div>
        <form @submit.prevent="submitRecipe">
            <div>
                <label for="titleRecipe" class="form-label">Nombre de la receta</label>
                <input type="text" id="titleRecipe" v-model="title" class="form-control">
            </div>
            <div>
                <label for="imageRecipe" class="form-label">Imagen de la receta</label>
                <input type="file" id="imageRecipe" @change="handleImageChange" class="form-control">
            </div>
            <div>
                <label for="videoRecipe" class="form-label">Video de la receta (Opcional)</label>
                <input type="file" id="videoRecipe" @change="handleVideoChange" class="form-control">
            </div>
            <div>
                <label for="descriptionRecipe" class="form-label">Descripción de la receta</label>
                <textarea id="descriptionRecipe" rows="20" cols="20" v-model="description"
                    class="form-control"></textarea>
            </div>
            <label for="ingredientsRecipe" class="form-label">Ingredientes + Cantidades</label>
            <div v-for="(ingredient, index) in recipebook.ingredients" :key="index">
                <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente" class="form-control">
                <input v-model="recipebook.quantities[index]" placeholder="Cantidad" class="form-control">
            </div>
            <div class="form-check">
                <input type="radio" id="option" name="option" value="yes" checked v-model="option"
                    class="form-check-input">
                <label for="option" class="form-check-label">Yes</label>
            </div>
            <div class="form-check">
                <input type="radio" id="option" name="option" value="no" v-model="option" class="form-check-input">
                <label for="optio" class="form-check-label">No</label>
            </div>
            <div>
                <label for="more" class="form-label">Añadir más</label>
                <input type="button" id="more" value="+" @click.prevent="moreIngredients" class="form-control">
            </div>
            <input type="submit" value="Crear Receta" class="btn btn-primary">
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
const option = ref('')

function handleImageChange(event) {
    const file = event.target.files[0];
    img.value = file;
}

function handleVideoChange(event) {
    const file = event.target.files[0];
    console.log(file)
    video.value = file;
}

function moreIngredients() {
    recipebook.ingredients.push('');
    recipebook.quantities.push('');
}

function submitRecipe() {
    const formData = new FormData();

    formData.append('titulo', title.value);
    formData.append('imagen', img.value);
    formData.append('video', video.value);
    formData.append('descripcion', description.value);
    formData.append('ingredientes', JSON.stringify(recipebook.ingredients));
    formData.append('cantidades', JSON.stringify(recipebook.quantities));
    formData.append('idUser', localStorage.getItem("iduser"));
    formData.append('opcion', option.value);
    formData.append('userToken', localStorage.getItem("userToken"));

    axios.post('http://localhost:5000/create', formData)
        .then(response => {
            if (response.data.isLoggin) {
                console.log(response.data.message)
                router.push({ name: "home" });
            } else {
                router.push({ name: "register" });
            }
        })
        .catch(error => {
            console.log(error)
        })
}
</script>

<style scoped></style>
