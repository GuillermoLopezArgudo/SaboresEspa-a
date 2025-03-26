<template>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Receta</h1>
        <div v-if="receta">
            <h2 class="text-primary">{{ receta.titulo }}</h2>
            <p class="lead">{{ receta.descripcion }}</p>
            
            <div v-if="receta.img" class="mb-4">
                <img :src="'data:image/jpeg;base64,' + receta.img" alt="Imagen de la receta" class="img-fluid rounded shadow" />
            </div>
            
            <h3 class="text-secondary">Ingredientes:</h3>
            <ul class="list-group list-group-flush">
                <li v-for="(ingrediente, idx) in receta.ingredientes" :key="idx" class="list-group-item">
                    {{ ingrediente }} - {{ receta.cantidades[idx] || 'Cantidad no disponible' }}
                </li>
            </ul>
            
            <div v-if="receta.video" class="my-4">
                <video controls :src="'data:video/mp4;base64,' + receta.video" class="w-100 rounded shadow"></video>
            </div>
            
            <div v-if="receta.valoraciones" class="my-3">
                <p><strong>Valoración:</strong> {{ receta.valoraciones }} estrellas</p>
            </div>
            <button @click="deleteRecipe">Eliminar</button>
        </div>

        <p v-else class="text-center text-muted">Cargando receta...</p>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute();
const recipeId = route.query.id;

const receta = ref(null);

const userToken = localStorage.getItem('userToken');

const payload = {
    idrecipe: recipeId,
    userToken: userToken
};

onMounted(() => {
    axios
        .post('http://localhost:5000/viewRecipe', payload)
        .then(response => {
            if (response.data.message) {
                receta.value = {
                    ...response.data.message,
                    ingredientes:response.data.message.ingredientes.map(item => item.replace(/[\[\]"]/g, '')),
                    cantidades:response.data.message.cantidades.map(item => item.replace(/[\[\]"]/g, ''))
                };
            } else {
                console.error("Receta no encontrada o error en la respuesta");
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
});

function deleteRecipe(){
    axios
        .post('http://localhost:5000/deleteRecipe', payload)
        .then(response => {
            console.log(response.data.message)
            router.push({ name: "home"});
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}
</script>

<style scoped>
h1,
h2,
h3 {
    font-family: Arial, sans-serif;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin: 5px 0;
}

img {
    width: 100%;
    max-width: 500px;
}

video {
    width: 100%;
    max-width: 500px;
}
</style>

