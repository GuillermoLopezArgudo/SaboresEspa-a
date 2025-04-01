<template>
    <div class="flex justify-center mt-12">
      <!-- Contenedor principal -->
      <div class="w-full sm:w-96">
        <!-- Card del perfil -->
        <div class="bg-white shadow-lg rounded-xl p-6">
          <!-- Imagen de perfil -->
          <div class="text-center mb-4">
            <img :src="`http://localhost:5000/${img}`" alt="Imagen de perfil"
              class="w-36 h-36 rounded-full mx-auto object-cover" />
            <label for="imageRecipe" class="block text-lg mt-4 text-gray-700">Imagen del perfil</label>
            <input type="file" id="imageRecipe" @change="handleImageChange" 
              class="mt-2 p-2 border border-gray-300 rounded-md w-full" />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const img = ref("static/images/NonPerfil.webp");
  
  function handleImageChange(event) {
    const file = event.target.files[0];
    img.value = file;
  }
  
  onMounted(() => {
    axios
      .post('http://localhost:5000/viewProfile')
      .then(response => {
        console.log(response.data.message)
      })
      .catch(error => {
        console.log(error)
      })
  })
  </script>
  
  <style scoped>
  /* Tailwind se usa por defecto, no es necesario agregar más estilos */
  </style>
  