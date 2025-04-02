<template>
    <div class="container mx-auto mt-5 px-4">
        <h1 class="text-center text-3xl font-bold mb-4">Tus Recetas</h1>
        <router-link to="/home" class="btn btn-secondary mb-4 text-white bg-gray-500 hover:bg-gray-600 px-6 py-2 rounded-md">
            Atrás
        </router-link>
        <div v-if="elementos.recetas.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="(item, index) in elementos.recetas[0]" :key="index" class="mb-4">
                <Recipe :item="item"></Recipe>
            </div>
        </div>
        <div v-else class="text-center">
            <p class="text-lg text-gray-600">No se encontraron recetas.</p>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import Recipe from './RecipesHome.vue';
import { useRouter } from 'vue-router';

const userToken = ref(localStorage.getItem("userToken"));
const router = useRouter();
const elementos = reactive({
    recetas: []
});

// Comprueba si el token esta guardado en el localstorage, si no lo esta llama al back por la referencia /viewRecipes y muestra todas las recetas propias
if (userToken.value == null) {
    router.push({ name: "login" });
} else {
    const playload = {
        id:localStorage.getItem("iduser"),
        userToken:userToken
    }

    axios.post('http://localhost:5000/viewRecipes', playload)
        .then(response => {
            elementos.recetas.push(response.data.message)
        })
        .catch(error => {
            console.log("Error al obtener las recetas:", error);
        });
}
</script>

<style scoped>
</style>
