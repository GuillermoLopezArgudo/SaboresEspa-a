<template>
    <div>
        <h1>PAGE RECIPE</h1>
        <div v-if="elementos.recetas.length > 0">
            <div v-for="(item, index) in elementos.recetas" :key="index">
                <Recipe :item="item"></Recipe>
            </div>
        </div>
        <div v-else>
            <p>No recipes found.</p>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import Recipe from './Recipes.vue';

const userToken = ref(localStorage.getItem("userToken"));
const elementos = reactive({
    recetas: []
});

axios.post('http://localhost:5000/viewRecipes', { userToken: userToken.value })
    .then(response => {
        if (response.data.message && response.data.message.length > 0) {
            elementos.recetas = response.data.message.map(item => {
                return {
                    ...item,
                    ingredientes: JSON.parse(item.ingredientes), 
                    cantidades: JSON.parse(item.cantidades)   
                };
            });
        } else {
            console.log("No recipes found or invalid response");
        }
    })
    .catch(error => {
        console.log(error);
    });
</script>

<style scoped></style>
