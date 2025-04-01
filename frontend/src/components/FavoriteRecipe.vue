<template>
  <div class="container mt-5">
    <h1 class="text-center mb-5">Recetario: Recetas Favoritas</h1>
    <div v-if="recetas.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div v-for="(item, index) in recetas" :key="item.id" class="col">
        <div class="card shadow-sm border-light">
          <img :src="`http://localhost:5000/${item.imagen}`" class="card-img-top" alt="Imagen de receta">
          <div class="card-body">
            <h5 class="card-title text-center text-primary">{{ item.titulo }}</h5>
            <p class="card-text text-muted">{{ item.descripcion }}</p>
            <div class="d-flex justify-content-between align-items-center">
              <router-link :to="'/recipe?id=' + item.id" class="btn btn-primary">Ver receta</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center mt-5">
      <div class="alert alert-warning" role="alert">
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
const idFavs = JSON.parse(localStorage.getItem('idFavs')) || [];

const recetas = ref([]);

//Cuando se crea el componente compruebe si en el localstorage hay favoritos si hay muestra los favoritos llamando al back por referencia /viewFavs
onMounted(() => {
  if (idFavs.length > 0) {
    const payload = {
      userToken: userToken,
      iduser: iduser,
      idFavs: idFavs,
    };

    axios
      .post('http://localhost:5000/viewFavs', payload)
      .then(response => {
        
        recetas.value = response.data.message;
      })
      .catch(error => {
        console.error("Error en la solicitud:", error);
      });
  }
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin-top: 50px;
}

.card {
  border-radius: 15px;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.card-title {
  font-weight: bold;
}

.card-text {
  font-size: 1rem;
  line-height: 1.5;
}

.btn {
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}

.alert {
  font-size: 1.2rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .container {
    margin-top: 30px;
  }
}
</style>
