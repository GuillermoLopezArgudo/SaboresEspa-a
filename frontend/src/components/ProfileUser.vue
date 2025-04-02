<template>
  <div class="flex justify-center mt-12">
    <div class="w-full sm:w-96">
      <div class="bg-white shadow-lg rounded-xl p-6">
        <div class="text-center mb-4">
          <img :src="`http://localhost:5000/${image}`" alt="Imagen de perfil"
            class="w-36 h-36 rounded-full mx-auto object-cover" />
          <label for="imageRecipe" class="block text-lg mt-4 text-gray-700">Imagen del perfil</label>
          <input type="file" id="imageRecipe" @change="handleImageChange"
            class="mt-2 p-2 border border-gray-300 rounded-md w-full" />
        </div>
        <div class="mt-4">
          <h5 class="text-lg font-semibold text-gray-800">Nombre:</h5>
          <p class="text-gray-600">{{ name }}</p>
          <button class="mt-2 text-blue-500 hover:text-blue-700 font-medium" @click="changeName">
            Cambiar Nombre
          </button>
        </div>
        <div class="mt-4">
          <h5 class="text-lg font-semibold text-gray-800">Email:</h5>
          <p class="text-gray-600">{{ email }}</p>
          <button class="mt-2 text-blue-500 hover:text-blue-700 font-medium" @click="changeEmail">
            Cambiar Email
          </button>
        </div>
        <button class="mt-2 text-blue-500 hover:text-blue-700 font-medium" @click="changePassword">
          Cambiar Password
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const image = ref("static/images/NonPerfil.webp");
const name = ref("")
const email = ref("")
const payload = {
  userToken: localStorage.getItem("userToken"),
  iduser: localStorage.getItem("iduser")
};

function handleImageChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      image.value = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }

  /*axios
    .post('http://localhost:5000/changeImage', { image: image.value })
    .then(response => {
      console.log(response.data.message)
    })
    .catch(error => {
      console.log(error);
    });*/
}

function changeName() {
  alert('Función para cambiar el nombre');
}

function changeEmail() {
  alert('Función para cambiar el correo');
}

function changePassword() {
  alert('Función para cambiar el password');
}


onMounted(() => {
  axios
    .post('http://localhost:5000/viewProfile', payload)
    .then(response => {

      name.value = response.data.message[0]
      email.value = response.data.message[1]
    })
    .catch(error => {
      console.log(error);
    });
});
</script>

<style scoped></style>
