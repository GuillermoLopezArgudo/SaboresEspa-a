<template>
  <div class="flex justify-center mt-12">
    <div class="w-full sm:w-96">
      <div class="bg-white shadow-lg rounded-xl p-6">
        <div class="text-center mb-4">
          <img :src="imageUrl" alt="Imagen de perfil" class="w-36 h-36 rounded-full mx-auto object-cover" />
          <label for="imageRecipe" class="block text-lg mt-4 text-gray-700">Imagen del perfil</label>
          <input type="file" id="imageRecipe" @change="handleImageChange"
            class="mt-2 p-2 border border-gray-300 rounded-md w-full" />
        </div>
        <div class="mt-4">
          <div v-if="!bollChangeName">
            <input type="text" id="changeName"  v-model="name">
            <button class="mt-2 text-blue-500 hover:text-blue-700 font-medium" @click="changeName">
              Enviar
            </button>
          </div>
          <div v-else>
            <h5 class="text-lg font-semibold text-gray-800">Nombre:</h5>
            <p class="text-gray-600">{{ name }}</p>
            <button class="mt-2 text-blue-500 hover:text-blue-700 font-medium" @click="handleNameChange">
              Cambiar Nombre
            </button>
          </div>
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

const image = ref("");
const imageUrl = ref("");
const name = ref("");
const email = ref("");
const payload = ref({
  userToken: localStorage.getItem("userToken"),
  iduser: localStorage.getItem("iduser"),
});
const bollChangeName = ref(true)

function handleImageChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      image.value = reader.result;
      imageUrl.value = reader.result;

      const imageData = {
        base64: image.value.split(',')[1],
        name: file.name 
      };
      changeImage(imageData);
    };
    reader.readAsDataURL(file);
  }
}


function  handleNameChange() {
  bollChangeName.value = false
}

function changeEmail() {
  alert('Función para cambiar el correo');
}

function changePassword() {
  alert('Función para cambiar el password');
}
function changeImage(imageData) {
  axios
    .post('http://localhost:5000/changeImage', {
      image: imageData,
      iduser: payload.value.iduser,
      userToken: payload.value.userToken
    })
    .then(response => {
      console.log(response.data);
      imageUrl.value = `http://localhost:5000/${response.data.newImage}`;
    })
    .catch(error => {
      console.log(error);
    });
}


function changeName() {

}

onMounted(() => {
  axios
    .post('http://localhost:5000/viewProfile', payload.value)
    .then(response => {
      name.value = response.data.message[0].name;
      email.value = response.data.message[0].email;
      imageUrl.value = `http://localhost:5000/${response.data.message[0].image}`; 
    })
    .catch(error => {
      console.log(error);
    });
});
</script>

<style scoped></style>
