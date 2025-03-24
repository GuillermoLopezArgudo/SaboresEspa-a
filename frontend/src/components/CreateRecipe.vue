<template>
    <h1>WELCOME A CREATE</h1>
    <div>
        <form @submit.prevent="submitRecipe">
            <div>
                <label for="titleRecipe" class="form-label">Nombre de la receta</label>
                <input type="text" id="titleRecipe" v-model="title" class="form-control" required>
            </div>
            <div>
                <label for="imageRecipe" class="form-label">Imagen de la receta</label>
                <input type="file" id="imageRecipe" @change="handleImageChange" class="form-control" required> 
            </div>
            <div>
                <label for="descriptionRecipe" class="form-label">Descripción de la receta</label>
                <textarea id="descriptionRecipe" rows="20" cols="20" v-model="description" class="form-control" required></textarea>
            </div>
            <label for="ingredientsRecipe" class="form-label">Ingredientes + Cantidades</label>
            <div v-for="(ingredient, index) in recipebook.ingredients" :key="index">
                <input v-model="recipebook.ingredients[index]" placeholder="Ingrediente" class="form-control" required>
                <input v-model="recipebook.quantities[index]" placeholder="Cantidad" class="form-control" required>
            </div>
            <div>
                <label for="more" class="form-label">Añadir más</label>
                <input type="button" id="more" value="+" @click.prevent="moreIngredients" class="form-control" required>
            </div>
            <input type="submit" value="Crear Receta" class="btn btn-primary">
        </form>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const title = ref('');
const img = ref('');
const description = ref('');
const recipebook = reactive({
    ingredients: [],
    quantities: []
});

var datos  = [];
var objeto = {};

function handleImageChange(event) {
    const file = event.target.files[0];
    img.value = file;
}

function moreIngredients() {
    recipebook.ingredients.push('');
    recipebook.quantities.push(''); 
}

function submitRecipe() {
    //console.log('Title:', title.value);
    //console.log('Image:', img.value);
    //console.log('Description:', description.value);
    //console.log('Ingredients:', recipebook.ingredients);
    //console.log('Quantities:', recipebook.quantities);

    datos.push({
        "titulo":title.value,
        "imagen":img.value.name,
        "descipcion":description.value,
        "ingredientes":recipebook.ingredients,
        "cantidades":recipebook.quantities
    })
    objeto.datos = datos;
    console.log(JSON.stringify(objeto));
}
</script>

<style scoped>

</style>
