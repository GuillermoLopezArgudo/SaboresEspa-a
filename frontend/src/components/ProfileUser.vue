<template>
  <div
    class="min-h-screen bg-gradient-to-b from-amber-50 to-amber-100 py-8 px-4 sm:px-6 lg:px-8 dark:bg-gradient-to-b dark:from-gray-800 dark:to-gray-900 dark:text-white">
    <div class="max-w-3xl mx-auto space-y-6 sm:space-y-8 hidden" ref="profile">
      <!-- Tarjeta principal de perfil -->
      <div
        class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl shadow-md sm:shadow-lg overflow-hidden hover:shadow-lg sm:hover:shadow-xl dark:shadow-lg dark:hover:shadow-xl">
        <!-- Encabezado con gradiente mejorado -->
        <div
          class="bg-gradient-to-r from-amber-500 to-amber-600 py-4 sm:py-5 px-4 sm:px-6 dark:from-gray-700 dark:to-gray-800">
          <h2 class="text-xl sm:text-2xl font-bold text-white text-center font-serif tracking-wide">MI PERFIL</h2>
        </div>

        <!-- Contenido -->
        <div class="p-4 sm:p-6 md:p-8">
          <!-- Foto de perfil con efecto hover mejorado -->
          <div class="text-center mb-6 sm:mb-8">
            <div class="relative inline-block group">
              <img :src="imageUrl" alt="Imagen de perfil"
                class="w-28 h-28 sm:w-32 sm:h-32 md:w-36 md:h-36 rounded-full mx-auto object-cover border-4 border-white shadow-md group-hover:border-amber-200 group-hover:shadow-lg">
              <label for="imageRecipe"
                class="absolute bottom-0 sm:bottom-2 right-0 sm:right-2 bg-amber-500 text-white p-1.5 sm:p-2 rounded-full cursor-pointer hover:bg-amber-600 shadow-md">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
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
          <div
            class="mb-4 sm:mb-6 p-4 sm:p-5 bg-amber-50 rounded-lg sm:rounded-xl border border-amber-100 dark:bg-gray-700 dark:border-gray-600">
            <div v-if="!boolChangeName" class="space-y-3 sm:space-y-4">
              <h3 class="text-base sm:text-lg font-semibold text-amber-800 mb-2 sm:mb-3 dark:text-amber-100">Nombre</h3>
              <input type="text" v-model="name"
                class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 dark:bg-gray-800 dark:border-gray-600 dark:text-white">

              <div class="flex space-x-2 sm:space-x-3 pt-1 sm:pt-2">
                <button @click="changeName"
                  class="flex-1 py-2 sm:py-2.5 bg-amber-500 text-white rounded-lg hover:bg-amber-600 flex items-center justify-center font-medium text-sm sm:text-base shadow hover:shadow-md dark:bg-gray-600 dark:hover:bg-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" viewBox="0 0 20 20"
                    fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Guardar
                </button>
                <button @click="handleNameChange"
                  class="flex-1 py-2 sm:py-2.5 bg-white text-amber-500 border border-amber-300 rounded-lg hover:bg-amber-50 font-medium text-sm sm:text-base dark:bg-gray-800 dark:text-white dark:border-gray-600">
                  Cancelar
                </button>
              </div>
            </div>
            <div v-else>
              <h3 class="text-base sm:text-lg font-semibold text-amber-800 mb-1 dark:text-amber-100">Nombre</h3>
              <p class="text-gray-700 mb-2 sm:mb-3 text-sm sm:text-base dark:text-gray-400">{{ name }}</p>
              <button @click="handleNameChange"
                class="text-amber-600 hover:text-amber-700 font-medium flex items-center text-sm sm:text-base dark:text-amber-400 dark:hover:text-amber-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none"
                  viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar nombre
              </button>
            </div>
          </div>

          <!-- Sección de email -->
          <div
            class="mb-4 sm:mb-6 p-4 sm:p-5 bg-amber-50 rounded-lg sm:rounded-xl border border-amber-100 dark:bg-gray-700 dark:border-gray-600">
            <div v-if="!boolChangeEmail" class="space-y-3 sm:space-y-4">
              <h3 class="text-base sm:text-lg font-semibold text-amber-800 mb-2 sm:mb-3 dark:text-amber-100">Email</h3>
              <input type="email" v-model="email"
                class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 dark:bg-gray-800 dark:border-gray-600 dark:text-white">

              <div class="flex space-x-2 sm:space-x-3 pt-1 sm:pt-2">
                <button @click="changeEmail"
                  class="flex-1 py-2 sm:py-2.5 bg-amber-500 text-white rounded-lg hover:bg-amber-600 flex items-center justify-center font-medium text-sm sm:text-base shadow hover:shadow-md dark:bg-gray-600 dark:hover:bg-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" viewBox="0 0 20 20"
                    fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Guardar
                </button>
                <button @click="handleChangeEmail"
                  class="flex-1 py-2 sm:py-2.5 bg-white text-amber-500 border border-amber-300 rounded-lg hover:bg-amber-50 font-medium text-sm sm:text-base dark:bg-gray-800 dark:text-white dark:border-gray-600">
                  Cancelar
                </button>
              </div>
            </div>
            <div v-else>
              <h3 class="text-base sm:text-lg font-semibold text-amber-800 mb-1 dark:text-amber-100">Email</h3>
              <p class="text-gray-700 mb-2 sm:mb-3 text-sm sm:text-base dark:text-gray-400">{{ email }}</p>
              <button @click="handleChangeEmail"
                class="text-amber-600 hover:text-amber-700 font-medium flex items-center text-sm sm:text-base dark:text-amber-400 dark:hover:text-amber-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none"
                  viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar email
              </button>
            </div>
          </div>

          <!-- Sección de contraseña -->
          <div
            class="mb-6 sm:mb-8 p-4 sm:p-5 bg-amber-50 rounded-lg sm:rounded-xl border border-amber-100 dark:bg-gray-700 dark:border-gray-600">
            <div v-if="!boolChangePassword" class="space-y-3 sm:space-y-4">
              <h3 class="text-base sm:text-lg font-semibold text-amber-800 mb-2 sm:mb-3 dark:text-amber-100">Cambiar
                Contraseña</h3>

              <div class="space-y-2 sm:space-y-3">
                <div>
                  <label class="block text-xs sm:text-sm font-medium text-amber-700 mb-1 dark:text-amber-400">Nueva
                    Contraseña</label>
                  <input type="password" v-model="newPassword"
                    class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 dark:bg-gray-800 dark:border-gray-600 dark:text-white">
                </div>

                <div>
                  <label class="block text-xs sm:text-sm font-medium text-amber-700 mb-1 dark:text-amber-400">Confirmar
                    Contraseña</label>
                  <input type="password" v-model="confirmPassword"
                    class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border border-amber-200 focus:ring-2 focus:ring-amber-400 focus:border-amber-400 dark:bg-gray-800 dark:border-gray-600 dark:text-white">
                </div>
              </div>

              <div v-if="error" class="text-red-500 text-xs sm:text-sm mt-1 sm:mt-2 animate-pulse">{{ error }}</div>

              <div class="flex space-x-2 sm:space-x-3 pt-1 sm:pt-2">
                <button @click="changePassword"
                  class="flex-1 py-2 sm:py-2.5 bg-amber-500 text-white rounded-lg hover:bg-amber-600 flex items-center justify-center font-medium text-sm sm:text-base shadow hover:shadow-md dark:bg-gray-600 dark:hover:bg-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" viewBox="0 0 20 20"
                    fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Guardar Contraseña
                </button>
                <button @click="handleChangePassword"
                  class="flex-1 py-2 sm:py-2.5 bg-white text-amber-500 border border-amber-300 rounded-lg hover:bg-amber-50 font-medium text-sm sm:text-base dark:bg-gray-800 dark:text-white dark:border-gray-600">
                  Cancelar
                </button>
              </div>
            </div>
            <div v-else>
              <h3 class="text-base sm:text-lg font-semibold text-amber-800 mb-1 dark:text-amber-100">Contraseña</h3>
              <p class="text-gray-700 mb-2 sm:mb-3 text-sm sm:text-base dark:text-gray-400">**********</p>
              <button @click="handleChangePassword"
                class="text-amber-600 hover:text-amber-700 font-medium flex items-center text-sm sm:text-base dark:text-amber-400 dark:hover:text-amber-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none"
                  viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Cambiar Contraseña
              </button>
            </div>
          </div>

          <!-- Botón para eliminar perfil -->
          <div class="mt-4 sm:mt-6 text-center">
            <button @click="deleteProfile"
              class="w-full max-w-xs mx-auto py-2.5 sm:py-3 bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold rounded-lg hover:from-red-600 hover:to-red-700 shadow-md hover:shadow-lg text-sm sm:text-base dark:bg-gradient-to-r dark:from-red-700 dark:to-red-800 dark:hover:from-red-800 dark:hover:to-red-900">
              Eliminar perfil
            </button>
          </div>
        </div>
      </div>

      <!-- Sección de administración (solo para admin) -->
      <div v-if="type === 'admin'"
        class="bg-white dark:bg-gray-800 rounded-xl sm:rounded-2xl shadow-md sm:shadow-lg overflow-hidden">
        <div
          class="bg-gradient-to-r from-amber-500 to-amber-600 py-4 sm:py-5 px-4 sm:px-6 dark:from-gray-700 dark:to-gray-800">
          <h2 class="text-xl sm:text-2xl font-bold text-white text-center font-serif tracking-wide ">ADMINISTRACIÓN DE
            USUARIOS</h2>
        </div>

        <div class="p-4 sm:p-6">
          <div v-for="(item, index) in users" :key="index"
            class="mb-3 sm:mb-4 p-3 sm:p-4 bg-amber-50 rounded-lg border border-amber-100 flex flex-col sm:flex-row justify-between items-start sm:items-center hover:bg-amber-100 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:bg-gray-600">
            <div class="mb-2 sm:mb-0">
              <p class="text-base sm:text-lg font-semibold text-amber-800 dark:text-amber-200">{{ item.name }}</p>
              <p class="text-xs sm:text-sm text-amber-600 dark:text-amber-400">{{ item.email }}</p>
            </div>
            <button @click="deleteUser(index)"
              class="ml-0 sm:ml-4 py-1.5 px-3 sm:py-2 sm:px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 flex items-center shadow hover:shadow-md text-xs sm:text-sm dark:bg-red-700 dark:hover:bg-red-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
    <div ref="loading" class="flex flex-col items-center min-h-screen px-4">
      <div
        class="inline-block animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 md:h-16 md:w-16 border-t-2 border-b-2 border-amber-600 dark:border-amber-400">
      </div>
      <p class="mt-3 sm:mt-4 text-amber-700 dark:text-amber-300 text-sm sm:text-base md:text-lg text-center">Cargando
        perfil...</p>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const image = ref("");
const imageUrl = ref("");
const name = ref(null);
const email = ref("");
const error = ref('');
const payload = ref({
  userToken: localStorage.getItem("userToken"),
  name: "",
  email: "",
  newPassword: "",
  confirmPassword: ""
});
const newPassword = ref('');
const confirmPassword = ref('');
const boolChangeName = ref(true);
const boolChangeEmail = ref(true);
const boolChangePassword = ref(true)
const darkMode = ref(false);
const router = useRouter();
const type = ref("")
const users = ref([])
const loading = ref("")
const profile = ref("")
const timeStart = ref(0)
const timeEnd = ref(0)
const timeTotal = ref(0)

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
      .post(`${process.env.VUE_APP_API_URL}/changePassword`, payload.value)
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
    .post(`${process.env.VUE_APP_API_URL}/changeImage`, {
      image: imageData,
      userToken: payload.value.userToken
    })
    .then(response => {
      console.log(response.data);
      imageUrl.value = `${process.env.VUE_APP_API_URL}/${response.data.newImage}`;
    })
    .catch(error => {
      console.log(error);
    });
}

function changeName() {
  payload.value.name = name.value;
  console.log("a")
  axios
    .post(`${process.env.VUE_APP_API_URL}/changeName`, payload.value)
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
    .post(`${process.env.VUE_APP_API_URL}/changeEmail`, payload.value)
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
  timeStart.value = performance.now();

  const savedMode = localStorage.getItem('darkMode');
  if (savedMode !== null) {
    darkMode.value = JSON.parse(savedMode);
    applyDarkMode();
  }

  axios
    .post(`${process.env.VUE_APP_API_URL}/viewProfile`, payload.value)
    .then(response => {
      name.value = response.data.message[0].name;
      email.value = response.data.message[0].email;
      imageUrl.value = `${process.env.VUE_APP_API_URL}/${response.data.message[0].image}`;
      type.value = response.data.type
      allusers(response.data.type)
      timeCharge()

    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
      if (error.status == 500) {
        router.push({ name: 'login' });
        localStorage.removeItem('userToken')
      }
    });

});

function deleteProfile() {
  axios
    .post(`${process.env.VUE_APP_API_URL}/deleteProfile`, payload.value)
    .then(response => {
      console.log(response.data.message);
      localStorage.removeItem("userToken");
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
      .post(`${process.env.VUE_APP_API_URL}/deleteUser`, {
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

function allusers(type) {
  if (type == "admin") {
    axios
      .post(`${process.env.VUE_APP_API_URL}/allUsers`, payload.value)
      .then(response => {
        users.value.push(...response.data.users_list)
      })
      .catch(error => {
        console.log(error);
      });
  }
}

function applyDarkMode() {
  if (darkMode.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

const timeCharge = () => {
  if (image.value.length > 0) {
    timeEnd.value = performance.now();
    timeTotal.value = timeEnd.value - timeStart.value;
    setTimeout(() => {
      loading.value.classList.add("hidden");
      profile.value.classList.remove("hidden");
    }, timeTotal.value)
  } else {
    loading.value.classList.add("hidden");
    profile.value.classList.remove("hidden");
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

/* Mejoras para móviles */
@media (max-width: 640px) {
  .flex-col-on-mobile {
    flex-direction: column;
  }

  .space-y-2-on-mobile>*+* {
    margin-top: 0.5rem;
  }
}
</style>