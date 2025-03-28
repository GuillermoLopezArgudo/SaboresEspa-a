<template>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Recetas de Hoy</h1>
        <router-link to="/home" class="btn btn-secondary mb-4">Atras</router-link>
        <div v-if="elementos.recetas.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3">
            <div v-for="(item, index) in elementos.recetas" :key="index" class="col mb-4">
                <Recipe :item="item"></Recipe>
            </div>
        </div>
        <div v-else class="text-center">
            <p>No se encontraron recetas.</p>
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

//Comprueba si el token esta guardado en el localstorage si no lo esta llama al back por la referencia /viewRecipes y muestra todas las recetas propias
if (userToken.value == null) {
    router.push({ name: "login" });
} else {

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
                console.log("No se encontraron recetas o respuesta inválida");
            }
        })
        .catch(error => {
            console.log("Error al obtener las recetas:", error);
        });
}
</script>

<style scoped>
.container {
    max-width: 1200px;
}

h1 {
    font-family: 'Arial', sans-serif;
    font-weight: 700;
}

.btn-secondary {
    font-size: 1rem;
    padding: 0.5rem 1.5rem;
}

.text-center p {
    font-size: 1.2rem;
    color: #6c757d;
}

.card {
    transition: transform 0.2s ease-in-out;
}

.card:hover {
    transform: scale(1.05);
}
</style>
