<template>
  <NavbarHome />
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-amber-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto space-y-8">
      <!-- Tarjeta principal de perfil -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
        <!-- Encabezado con gradiente mejorado -->
        <div class="bg-gradient-to-r from-amber-500 to-amber-600 py-5 px-6">
          <h2 class="text-2xl font-bold text-white text-center font-serif tracking-wide">MI PERFIL</h2>
        </div>

        <!-- Contenido -->
        <div class="p-6 md:p-8">
          <!-- Foto de perfil con efecto hover mejorado -->
          <div class="text-center mb-8">
            <div class="relative inline-block group">
              <img :src="imageUrl" alt="Imagen de perfil"
                class="w-36 h-36 rounded-full mx-auto object-cover border-4 border-white shadow-lg transition-all duration-300 group-hover:border-amber-200 group-hover:shadow-md">
              <label for="imageRecipe"
                class="absolute bottom-2 right-2 bg-amber-500 text-white p-2 rounded-full cursor-pointer hover:bg-amber-600 transition duration-300 shadow-md">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <input type="file" id="imageRecipe" @change="handleImageChange" class="hidden" accept="image/*" />
              </label>
            </div>
          </div>

          <!-- Sección de nombre -->
          <div class="mb-6 p-5 bg-amber-50 rounded-xl border border-amber-100">
            <div v-if="!boolChangeName" class="space-y-4">
              <h3 class="text-lg font-semibold text-amber-800 mb-3">Nombre</h3>
              <input type="text" v-model="name"
                class="w-full px-4 py-2 rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition duration-200">
              
              <div class="flex space-x-3 pt-2">
                <button @click="changeName"
                  class="flex-1 py-2.5 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition duration-300 flex items-center justify-center font-medium shadow hover:shadow-md">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Guardar
                </button>
                <button @click="handleNameChange"
                  class="flex-1 py-2.5 bg-white text-amber-500 border border-amber-300 rounded-lg hover:bg-amber-50 transition duration-300 font-medium">
                  Cancelar
                </button>
              </div>
            </div>
            <div v-else>
              <h3 class="text-lg font-semibold text-amber-800 mb-1">Nombre</h3>
              <p class="text-gray-700 mb-3">{{ name }}</p>
              <button @click="handleNameChange"
                class="text-amber-600 hover:text-amber-700 font-medium flex items-center transition duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar nombre
              </button>
            </div>
          </div>

          <!-- Sección de email -->
          <div class="mb-6 p-5 bg-amber-50 rounded-xl border border-amber-100">
            <div v-if="!boolChangeEmail" class="space-y-4">
              <h3 class="text-lg font-semibold text-amber-800 mb-3">Email</h3>
              <input type="email" v-model="email"
                class="w-full px-4 py-2 rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition duration-200">
              
              <div class="flex space-x-3 pt-2">
                <button @click="changeEmail"
                  class="flex-1 py-2.5 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition duration-300 flex items-center justify-center font-medium shadow hover:shadow-md">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Guardar
                </button>
                <button @click="handleChangeEmail"
                  class="flex-1 py-2.5 bg-white text-amber-500 border border-amber-300 rounded-lg hover:bg-amber-50 transition duration-300 font-medium">
                  Cancelar
                </button>
              </div>
            </div>
            <div v-else>
              <h3 class="text-lg font-semibold text-amber-800 mb-1">Email</h3>
              <p class="text-gray-700 mb-3">{{ email }}</p>
              <button @click="handleChangeEmail"
                class="text-amber-600 hover:text-amber-700 font-medium flex items-center transition duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar email
              </button>
            </div>
          </div>

          <!-- Sección de contraseña -->
          <div class="mb-8 p-5 bg-amber-50 rounded-xl border border-amber-100">
            <div v-if="!boolChangePassword" class="space-y-4">
              <h3 class="text-lg font-semibold text-amber-800 mb-3">Cambiar Contraseña</h3>
              
              <div class="space-y-3">
                <div>
                  <label class="block text-sm font-medium text-amber-700 mb-1">Nueva Contraseña</label>
                  <input type="password" v-model="newPassword"
                    class="w-full px-4 py-2 rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition duration-200">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-amber-700 mb-1">Confirmar Contraseña</label>
                  <input type="password" v-model="confirmPassword"
                    class="w-full px-4 py-2 rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition duration-200">
                </div>
              </div>

              <div v-if="error" class="text-red-500 text-sm mt-2 animate-pulse">{{ error }}</div>

              <div class="flex space-x-3 pt-2">
                <button @click="changePassword"
                  class="flex-1 py-2.5 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition duration-300 flex items-center justify-center font-medium shadow hover:shadow-md">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Guardar
                </button>
                <button @click="handleChangePassword"
                  class="flex-1 py-2.5 bg-white text-amber-500 border border-amber-300 rounded-lg hover:bg-amber-50 transition duration-300 font-medium">
                  Cancelar
                </button>
              </div>
            </div>
            <div v-else>
              <button @click="handleChangePassword"
                class="w-full py-2.5 text-amber-600 hover:text-amber-700 font-medium flex items-center justify-center transition duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                Cambiar contraseña
              </button>
            </div>
          </div>

          <!-- Botón para eliminar perfil -->
          <div class="mt-6 text-center">
            <button @click="deleteProfile"
              class="w-full max-w-xs mx-auto py-3 bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold rounded-lg hover:from-red-600 hover:to-red-700 transition duration-300 shadow-md hover:shadow-lg">
              Eliminar perfil
            </button>
          </div>
        </div>
      </div>

      <!-- Sección de administración (solo para admin) -->
      <div v-if="type === 'admin'" class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="bg-gradient-to-r from-amber-500 to-amber-600 py-5 px-6">
          <h2 class="text-2xl font-bold text-white text-center font-serif tracking-wide">ADMINISTRACIÓN DE USUARIOS</h2>
        </div>
        
        <div class="p-6">
          <div v-for="(item, index) in users" :key="index" 
               class="mb-4 p-4 bg-amber-50 rounded-lg border border-amber-100 flex justify-between items-center transition duration-200 hover:bg-amber-100">
            <div>
              <p class="text-lg font-semibold text-amber-800">{{ item.name }}</p>
              <p class="text-sm text-amber-600">{{ item.email }}</p>
            </div>
            <button @click="deleteUser(index)"
              class="ml-4 py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 transition duration-300 flex items-center shadow hover:shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <FooterPage />
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
const users = ref([])

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
        users.value.push(...response.data.users_list)
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

function deleteUser(index) {
  if (confirm("¿Estás seguro de que quieres eliminar este usuario?")) {
    const userId = users.value[index].iduser;
    axios
      .post('http://localhost:5000/deleteUser', {
        iduser: userId,
        userToken: payload.value.userToken
      })
      .then(response => {
        console.log(response.data.message);
        users.value.splice(index, 1);
      })
      .catch(error => {
        console.log(error);
      });
  }
}
</script>

<style scoped>
/* Animaciones mejoradas */
.fade-enter-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* Efecto para la imagen de perfil */
img {
  transition: all 0.3s ease;
}
img:hover {
  transform: scale(1.03);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Estilo para los inputs con enfoque */
input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.5);
}
</style>