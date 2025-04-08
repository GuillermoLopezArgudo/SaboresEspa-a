<template>
  <NavbarHome></NavbarHome>
  <div class="min-h-screen bg-amber-50 py-12 px-4 sm:px-6 lg:px-8">

    <div class="max-w-md mx-auto bg-white rounded-xl shadow-xl overflow-hidden">
      <!-- Encabezado -->
      <div class="bg-gradient-to-r from-amber-600 to-amber-700 py-4 px-6">
        <h2 class="text-2xl font-bold text-white text-center">Mi Perfil</h2>
      </div>

      <!-- Contenido -->
      <div class="p-6">
        <!-- Foto de perfil -->
        <div class="text-center mb-6">
          <div class="relative inline-block">
            <img :src="imageUrl" alt="Imagen de perfil"
              class="w-32 h-32 rounded-full mx-auto object-cover border-4 border-amber-100 shadow-md">
            <label for="imageRecipe"
              class="absolute bottom-0 right-0 bg-amber-600 text-white p-2 rounded-full cursor-pointer hover:bg-amber-700 transition duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <input type="file" id="imageRecipe" @change="handleImageChange" class="hidden" />
            </label>
          </div>
        </div>

        <!-- Nombre -->
        <div class="mb-6 p-4 bg-amber-50 rounded-lg">
          <div v-if="!boolChangeName" class="space-y-3">
            <label for="nameInput" class="block text-sm font-medium text-amber-800">Nuevo nombre</label>
            <input type="text" id="nameInput" v-model="name"
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
            <div class="flex space-x-3">
              <button @click="changeName"
                class="flex-1 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition duration-300 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd" />
                </svg>
                Guardar
              </button>
              <button @click="handleNameChange"
                class="flex-1 py-2 bg-white text-amber-600 border border-amber-600 rounded-lg hover:bg-amber-50 transition duration-300">
                Cancelar
              </button>
            </div>
          </div>
          <div v-else>
            <h5 class="text-sm font-medium text-amber-600">Nombre</h5>
            <p class="text-lg font-semibold text-amber-800 mt-1">{{ name }}</p>
            <button @click="handleNameChange"
              class="mt-2 text-amber-600 hover:text-amber-800 font-medium flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Cambiar nombre
            </button>
          </div>
        </div>

        <!-- Email -->
        <div class="mb-6 p-4 bg-amber-50 rounded-lg">
          <div v-if="!boolChangeEmail" class="space-y-3">
            <label for="emailInput" class="block text-sm font-medium text-amber-800">Nuevo email</label>
            <input type="email" id="emailInput" v-model="email"
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
            <div class="flex space-x-3">
              <button @click="changeEmail"
                class="flex-1 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition duration-300 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd" />
                </svg>
                Guardar
              </button>
              <button @click="handleChangeEmail"
                class="flex-1 py-2 bg-white text-amber-600 border border-amber-600 rounded-lg hover:bg-amber-50 transition duration-300">
                Cancelar
              </button>
            </div>
          </div>
          <div v-else>
            <h5 class="text-sm font-medium text-amber-600">Email</h5>
            <p class="text-lg font-semibold text-amber-800 mt-1">{{ email }}</p>
            <button @click="handleChangeEmail"
              class="mt-2 text-amber-600 hover:text-amber-800 font-medium flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Cambiar email
            </button>
          </div>
        </div>

        <!-- Cambiar contraseña -->
        <div class="p-4 bg-amber-50 rounded-lg">
          <div v-if="!boolChangePassword" class="space-y-3">
            <label for="emailInput" class="block text-sm font-medium text-amber-800">Nueva Contraseña</label>
            <input type="password" id="emailInput"
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              v-model="newPassword">
            <label>Confirma contraseña</label>
            <input type="password" id="emailInput"
              class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              v-model="confirmPassword">
            <div class="flex space-x-3">
              <button @click="changePassword"
                class="flex-1 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition duration-300 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd" />
                </svg>
                Guardar
              </button>
              <button @click="handleChangePassword"
                class="flex-1 py-2 bg-white text-amber-600 border border-amber-600 rounded-lg hover:bg-amber-50 transition duration-300">
                Cancelar
              </button>
            </div>
          </div>
          <div v-else>
            <button @click="handleChangePassword"
              class="w-full py-2 text-amber-600 hover:text-amber-800 font-medium flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Cambiar contraseña
            </button>
          </div>
          {{ error }}
        </div>
        <!-- Botón para eliminar perfil -->
        <div class="mt-6 text-center">
          <button @click="deleteProfile"
            class="w-full py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition duration-300">
            Eliminar perfil
          </button>
        </div>
      </div>
    </div>

  </div>
  <div v-for="(item) in users" :key="item.id">
    <p>{{ item.name }}</p>
  </div>
  <FooterPage></FooterPage>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NavbarHome from './NavbarHome.vue';
import { useRouter } from 'vue-router';
import FooterPage from './FooterPage.vue';

const image = ref("");
const imageUrl = ref("");
const name = ref("");
const email = ref("");
const error = ref('');
const payload = ref({
  userToken: localStorage.getItem("userToken"),
  iduser: localStorage.getItem("iduser"),
  name: "",
  email: "",
  newPassword: "",
  confirmPassword: "",
  type: localStorage.getItem("type")
});
const newPassword = ref('');
const confirmPassword = ref('');
const boolChangeName = ref(true);
const boolChangeEmail = ref(true);
const boolChangePassword = ref(true)
const router = useRouter();
const type = localStorage.getItem("type")
const users = []

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

function handleNameChange() {
  boolChangeName.value = !boolChangeName.value;
}

function handleChangeEmail() {
  boolChangeEmail.value = !boolChangeEmail.value;
}

function handleChangePassword() {
  boolChangePassword.value = !boolChangePassword.value;
}

function changePassword() {

  if (newPassword.value !== confirmPassword.value) {
    error.value = "Las contraseñas no coinciden";
    setTimeout(() => { error.value = ''; }, 3000);
    return;
  } else {
    payload.value.newPassword = newPassword.value;
    axios
      .post('http://localhost:5000/changePassword', payload.value)
      .then(response => {
        console.log(response.data.message)
      })
      .catch(error => {
        console.log(error);
      })
    handleChangePassword();
  }

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
  payload.value.name = name.value;
  axios
    .post('http://localhost:5000/changeName', payload.value)
    .then(response => {
      console.log(response.data.message);
      handleNameChange();
    })
    .catch(error => {
      console.log(error);
    });
}

function changeEmail() {
  payload.value.email = email.value;
  axios
    .post('http://localhost:5000/changeEmail', payload.value)
    .then(response => {
      console.log(response.data.message);
      localStorage.setItem('userToken', response.data.userToken);
      handleChangeEmail();
    })
    .catch(error => {
      console.log(error);
    });
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
  if (type == "admin") {
    axios
      .post('http://localhost:5000/allUsers', payload.value)
      .then(response => {
        users.push(response.data.users_list)
        console.log(response.data.users_list)
      })
      .catch(error => {
        console.log(error);
      });
  }
});

function deleteProfile() {
  axios
    .post('http://localhost:5000/deleteProfile', payload.value)
    .then(response => {
      console.log(response.data.message);
      localStorage.removeItem("iduser");
      localStorage.removeItem("token");
      localStorage.removeItem("type");
      router.push({ name: "register" });
    })
    .catch(error => {
      console.log(error);
    });
}



</script>

<style scoped>
/* Animaciones para los cambios de estado */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Efecto para el hover de la imagen */
img:hover {
  filter: brightness(1.05);
  transition: filter 0.3s ease;
}
</style>