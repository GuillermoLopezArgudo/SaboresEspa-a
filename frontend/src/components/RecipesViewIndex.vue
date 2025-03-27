<template>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Todas las Recetas</h1>
        <nav class="navbar navbar-light bg-light mb-4">
            <div class="container">
                <div v-if="!userToken">
                    <router-link to="/login" class="btn btn-outline-primary me-2">Iniciar Sesión</router-link>
                    <router-link to="/register" class="btn btn-outline-success">Registrar</router-link>
                </div>
                <div v-else>
                    <router-link to="/home" class="btn btn-outline-primary me-2">Home</router-link>
                </div>
            </div>
        </nav>

        <div v-if="elementos.recetas.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3">
            <div v-for="(item, index) in elementos.recetas" :key="index" class="col mb-4">
                <button @click="toggleFavorite(item.id)" :class="['heart-button', { 'active': isFavorite(item.id) }]"
                    class="btn btn-outline-danger mb-3">
                    <i class="fa" :class="isFavorite ? 'fa-heart' : 'fa-heart-o'"></i> Favoritos
                </button>
                <Recipe :item="item"></Recipe>
            </div>
        </div>

        <div v-else class="text-center">
            <p>No se encontraron recetas.</p>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref,reactive,onMounted } from 'vue';
import Recipe from './RecipesHome.vue';

const elementos = reactive({
    recetas: []
});
const userToken = localStorage.getItem('userToken');
const favoritos = reactive({});
const iduser = localStorage.getItem('iduser');

axios
    .post('http://localhost:5000/viewAll')
    .then(response => {
        if (response.data.message && response.data.message.length > 0) {
            elementos.recetas = response.data.message.map(item => {
                return {
                    ...item,
                    ingredientes: JSON.parse(item.ingredientes),
                    cantidades: JSON.parse(item.cantidades)
                };
            });
        }
    })
    .catch(error => {
        console.error("Error en la solicitud:", error);
    });

const toggleFavorite = (id) => {
    const payload = {
    idrecipe: id,
    userToken: userToken,
    comment: "",
    iduser: iduser,
    idcomment: 0
};
    if (favoritos[id]) {
        favoritos[id] = false;
        axios
            .post('http://localhost:5000/deleteFavs', payload)
            .then(response => {
                console.log(response.data.message)
                localStorage.setItem('idFavs',response.data.idFavs)
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
            });
    } else {
        favoritos[id] = true;
        axios
            .post('http://localhost:5000/updateFavs', payload)
            .then(response => {
                console.log(response.data.message)
                localStorage.setItem('idFavs',response.data.idFavs)
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
            });
    }


};

const isFavorite = (id) => {
    return favoritos[id] || false;
};
</script>

<style scoped>
.container {
    max-width: 1200px;
}

h1 {
    font-family: 'Arial', sans-serif;
    font-weight: 700;
}

.navbar {
    border-radius: 10px;
}

.navbar .btn {
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
