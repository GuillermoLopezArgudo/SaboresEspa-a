<template>
    <div>
      <h1 class="text-center mt-4">Bienvenido a tu Recetario</h1>
  
      <!-- Barra de navegación -->
      <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm mb-4">
        <div class="container">
          <router-link to="/" class="navbar-brand fs-4 text-primary">Recetario</router-link>
          
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <router-link to="/create" class="nav-link">Crear receta</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/recipes" class="nav-link">Mis recetas</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/" class="nav-link">Todas las recetas</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link">Ajustes</router-link>
              </li>
              <li class="nav-item">
                <router-link @click="closeSession" to="/login" class="nav-link">Cerrar sesión</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- Contenido de las recetas -->
      <div class="container">
        <FavoriteRecipe></FavoriteRecipe>
      </div>
    </div>
  </template>
  
  <script setup>
  import FavoriteRecipe from './FavoriteRecipe.vue';
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const userToken = ref(localStorage.getItem("userToken"));
  const router = useRouter();
  if(userToken.value == null){
      router.push({ name: "login"});
  }
  
  function closeSession(){
      localStorage.clear()
  }
  </script>
  
  <style scoped>
  /* Estilos generales */
  body {
    background-color: #f8f9fa;
    font-family: 'Arial', sans-serif;
  }
  
  /* Títulos */
  h1 {
    font-size: 2.5rem;
    color: #007bff;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 30px;
  }
  
  /* Navbar */
  .navbar {
    background-color: #ffffff;
  }
  
  .navbar-brand {
    font-size: 1.5rem;
    color: #007bff;
  }
  
  .navbar-nav .nav-link {
    color: #6c757d;
    font-size: 1.1rem;
    margin-right: 15px;
  }
  
  .navbar-nav .nav-link:hover {
    color: #007bff;
  }
  
  .navbar-toggler {
    border-color: #007bff;
  }
  
  .navbar-toggler-icon {
    background-color: #007bff;
  }
  
  /* Favoritos */
  .favorite-recipes {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 40px;
  }
  
  .favorite-recipes .recipe-card {
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
  }
  
  .favorite-recipes .recipe-card img {
    width: 100%;
    border-radius: 8px;
  }
  
  .favorite-recipes .recipe-card h5 {
    font-size: 1.25rem;
    color: #333;
  }
  
  .favorite-recipes .recipe-card .btn {
    background-color: #007bff;
    color: white;
    border: none;
    margin-top: 10px;
    width: 100%;
    border-radius: 5px;
  }
  
  .favorite-recipes .recipe-card .btn:hover {
    background-color: #0056b3;
  }
  
  /* Estilo para los botones de acción */
  button {
    background-color: #007bff;
    border: none;
    color: white;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 5px;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  /* Estilos responsivos */
  @media (max-width: 768px) {
    .favorite-recipes {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (max-width: 480px) {
    .favorite-recipes {
      grid-template-columns: 1fr;
    }
  
    h1 {
      font-size: 2rem;
    }
  }
  </style>
  