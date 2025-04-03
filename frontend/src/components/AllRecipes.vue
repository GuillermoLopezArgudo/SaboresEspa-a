<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-center text-4xl font-bold text-gray-800 mb-6">Todas las Recetas</h1>
      
      <!-- Navbar -->
      <nav class="navbar bg-white shadow-lg rounded-lg mb-6 p-4">
        <div class="container flex justify-between items-center">
          <div v-if="!userToken" class="flex space-x-4">
            <router-link to="/login" class="btn btn-outline-primary text-white bg-blue-600 hover:bg-blue-500 hover:text-white py-2 px-6 rounded-md">Iniciar Sesión</router-link>
            <router-link to="/register" class="btn btn-outline-success text-white bg-green-600 hover:bg-green-500 hover:text-white py-2 px-6 rounded-md">Registrar</router-link>
          </div>
          <div v-else>
            <router-link to="/home" class="btn btn-outline-primary text-white bg-blue-600 hover:bg-blue-500 hover:text-white py-2 px-6 rounded-md">Home</router-link>
          </div>
        </div>
      </nav>
  
      <!-- Recetas Listado -->
      <div v-if="elementos.recetas.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(item) in elementos.recetas" :key="item.id" class="bg-white shadow-xl rounded-lg p-6 transition-transform transform hover:scale-105">
          
          <!-- Favoritos Button -->
          <button @click="toggleFavorite(item.id)" :class="['heart-button', { 'active': isFavorite(item.id) }]" class="btn btn-outline-danger mb-4 flex items-center space-x-2 text-red-600 hover:text-red-500">
            <i class="fa" :class="isFavorite(item.id) ? 'fa-heart' : 'fa-heart-o'"></i> <span class="font-semibold">Favoritos</span>
          </button>
  
          <!-- Componente Receta -->
          <Recipe :item="item" class="mb-4" />
  
          <!-- Estrellas Rating -->
          <StarRating :rating="ratings[item.id] || 0" :onRatingChanged="ratingChanged(item.id)" class="mt-3" />
        </div>
      </div>
  
      <!-- Mensaje si no hay recetas -->
      <div v-else class="text-center text-gray-600">
        <p class="text-lg">No se encontraron recetas.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { reactive } from 'vue';
  import Recipe from './RecipesHome.vue';
  import StarRating from './StarRating.vue';
  import 'font-awesome/css/font-awesome.min.css';
  import { useRouter } from 'vue-router';
  
  const elementos = reactive({
    recetas: []
  });
  const favoritos = reactive({});
  const ratings = reactive({});
  const userToken = localStorage.getItem('userToken');
  const iduser = localStorage.getItem('iduser');
  const router = useRouter();
  
  // Solicitar todas las recetas y datos relacionados
  axios.post('http://localhost:5000/viewAll', { iduser })
    .then(response => {
      elementos.recetas = response.data.recipes_list;
      if (iduser) {
        response.data.favorites_list.forEach(id => {
          favoritos[id.id_recipe] = true;
        });
        response.data.reviews_list.forEach(id => {
          ratings[id.id_recipe] = id.review;
        });
      }
    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
    });
  
  // Cambiar el estado de favoritos
  const toggleFavorite = (id) => {
    if (userToken) {
      const payload = {
        idrecipe: id,
        userToken,
        comment: "",
        iduser,
        idcomment: 0
      };
  
      if (favoritos[id]) {
        favoritos[id] = false;
        axios.post('http://localhost:5000/deleteFavs', payload)
          .then(response => {
            console.log(response.data.message);
          })
          .catch(error => {
            console.error("Error en la solicitud:", error);
          });
      } else {
        favoritos[id] = true;
        axios.post('http://localhost:5000/updateFavs', payload)
          .then(response => {
            console.log(response.data.message);
          })
          .catch(error => {
            console.error("Error en la solicitud:", error);
          });
      }
    } else {
      router.push({ name: "login" });
    }
  };
  
  // Comprobar si una receta es favorita
  const isFavorite = (id) => {
    return favoritos[id] || false;
  };
  
  // Función para cambiar la calificación de una receta
  const ratingChanged = (recipeId) => {
    if (userToken) {
      return (newRating) => {
        ratings[recipeId] = newRating;
        const payload = {
          idrecipe: recipeId,
          rating: newRating,
          userToken,
          iduser
        };
  
        localStorage.setItem('ratings', JSON.stringify(ratings));
        axios.post('http://localhost:5000/updateRating', payload)
          .then(response => {
            console.log(response.data.message);
          })
          .catch(error => {
            console.error("Error en la solicitud:", error);
          });
      };
    }
  };
  </script>
  
  <style scoped>
  /* Tailwind already takes care of most of the styling */
  .container {
    max-width: 1200px;
  }
  
  .heart-button {
    transition: transform 0.3s ease;
  }
  
  .heart-button.active {
    color: #e74c3c;
  }
  
  .heart-button:hover {
    transform: scale(1.1);
  }
  </style>
  