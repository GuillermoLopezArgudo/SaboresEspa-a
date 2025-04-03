<template>
  <div class="container mx-auto mt-5 px-4">
    <h1 class="text-center text-3xl font-semibold mb-5">Recetario: Recetas Favoritas</h1>
    <div v-if="recetas.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="(item) in recetas" :key="item.id" class="card border border-light rounded-lg shadow-sm overflow-hidden">
        <img :src="`http://localhost:5000/${item.image}`" class="w-full h-48 object-cover" alt="Imagen de receta">
        <div class="card-body p-4">
          <h5 class="card-title text-center text-primary text-xl font-bold">{{ item.title }}</h5>
          <p class="card-text text-gray-600 text-sm">{{ item.description }}</p>
          <div class="flex justify-between items-center mt-4">
            <router-link :to="'/recipe?id=' + item.id" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition">Ver receta</router-link>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center mt-5">
      <div class="alert alert-warning bg-yellow-100 text-yellow-800 p-4 rounded-lg font-medium">
        No tienes recetas favoritas. ¡Agrega algunas y vuelve!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userToken = localStorage.getItem('userToken');
const iduser = localStorage.getItem('iduser');

const recetas = ref([]);

//Cuando se crea el componente, si hay favoritos en localstorage, llama al backend para obtenerlos
onMounted(() => {
    const payload = {
      userToken: userToken,
      iduser: iduser
    };  

    axios
      .post('http://localhost:5000/viewFavs', payload)
      .then(response => {
        recetas.value = response.data.message;
      })
      .catch(error => {
        console.error("Error en la solicitud:", error);
      });
});
</script>

<style scoped>
</style>
