<template>
    <div class="min-h-screen bg-amber-50 py-8 px-4 sm:px-6 lg:px-8">
      <!-- Encabezado -->
      <div class="max-w-7xl mx-auto text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-2">
          Detalle de Receta
        </h1>
      </div>
  
      <!-- Botón de regreso -->
      <div class="max-w-7xl mx-auto mb-6">
        <router-link to="/" class="inline-flex items-center px-5 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg transition duration-300 shadow-md">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          Volver al inicio
        </router-link>
      </div>
  
      <!-- Contenido principal -->
      <div v-if="receta" class="max-w-7xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden border border-amber-200">
        <!-- Sección superior -->
        <div class="p-6 sm:p-8 border-b border-amber-100 bg-gradient-to-r from-amber-50 to-white">
          <div class="flex justify-between items-start">
            <div>
              <h2 class="text-2xl md:text-3xl font-bold text-amber-800 font-serif">{{ receta.title }}</h2>
              <button @click="toggleFavorite" 
                      class="mt-3 flex items-center text-red-500 hover:text-red-600 transition duration-300">
                <i class="fa text-2xl mr-2" :class="isFavorite ? 'fa-heart' : 'fa-heart-o'"></i>
                <span class="font-medium">{{ isFavorite ? 'En favoritos' : 'Añadir a favoritos' }}</span>
              </button>
            </div>
            <div v-if="iduser == receta.id_user || type == 'admin'" class="flex space-x-2">
              <button @click="editeRecipe" 
                      class="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg transition duration-300 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar
              </button>
              <button @click="deleteRecipe" 
                      class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition duration-300 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Eliminar
              </button>
            </div>
          </div>
  
          <p class="mt-4 text-amber-700 text-lg">{{ receta.description }}</p>
        </div>
  
        <!-- Imagen de la receta -->
        <div v-if="receta.image" class="p-6 sm:p-8">
          <div class="rounded-xl overflow-hidden shadow-md border border-amber-200">
            <img :src="`http://localhost:5000/${receta.image}`" alt="Imagen de la receta" class="w-full h-auto object-cover">
          </div>
        </div>
  
        <!-- Video de la receta -->
        <div v-if="receta.video" class="p-6 sm:p-8 pt-0">
          <div class="rounded-xl overflow-hidden shadow-md border border-amber-200">
            <video controls :src="'http://localhost:5000/' + receta.video" class="w-full"></video>
          </div>
        </div>
  
        <!-- Ingredientes -->
        <div class="p-6 sm:p-8 border-t border-amber-100">
          <h3 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Ingredientes
          </h3>
          <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <li v-for="(ingrediente, idx) in ingredients" :key="idx" class="bg-amber-50 p-3 rounded-lg border border-amber-200">
              <span class="font-medium text-amber-800">{{ ingrediente }}</span>
              <span class="block text-amber-600 text-sm">{{ quantity[idx] || 'Cantidad no disponible' }}</span>
            </li>
          </ul>
        </div>
  
        <!-- Pasos de la receta -->
        <div v-if="steps.length > 0" class="p-6 sm:p-8 border-t border-amber-100">
          <h3 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Pasos de Preparación
          </h3>
          <div class="space-y-6">
            <div v-for="(step, idx) in steps" :key="idx" class="bg-white p-5 rounded-xl border border-amber-200 shadow-sm">
              <div class="flex items-start">
                <span class="bg-amber-600 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center mr-4 flex-shrink-0">
                  {{ idx + 1 }}
                </span>
                <div>
                  <h4 class="font-semibold text-amber-800 text-lg">{{ step.title }}</h4>
                  <p class="text-amber-700 mt-1">{{ step.description }}</p>
                  <div v-if="step.image" class="mt-3 rounded-lg overflow-hidden border border-amber-200">
                    <img :src="`http://localhost:5000/${step.image}`" :alt="`Imagen del paso ${idx + 1}`" class="w-full max-w-md">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Valoración -->
        <div v-if="receta.assessment" class="p-6 sm:p-8 border-t border-amber-100 bg-amber-50">
          <h3 class="text-xl font-bold text-amber-800 mb-2">Valoración</h3>
          <div class="flex items-center">
            <div class="flex text-amber-500 mr-2">
              <svg v-for="star in 5" :key="star" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="{'text-amber-300': star > receta.valoraciones}" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <span class="text-amber-700 font-medium">{{ receta.valoraciones }} estrellas</span>
          </div>
        </div>
  
        <!-- Comentarios -->
        <div class="p-6 sm:p-8 border-t border-amber-100">
          <h3 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Comentarios
          </h3>
  
          <!-- Lista de comentarios -->
          <div v-if="comments.length > 0" class="space-y-4 mb-6">
            <div v-for="comment in comments" :key="comment.id" class="bg-white p-4 rounded-lg border border-amber-200 shadow-sm">
              <div v-if="editingCommentId === comment.id" class="mb-3">
                <textarea v-model="editedComment" rows="3" class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"></textarea>
                <div class="flex space-x-2 mt-2">
                  <button @click="updateComment(comment.id)" class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition duration-300">
                    Guardar
                  </button>
                  <button @click="cancelEdit" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition duration-300">
                    Cancelar
                  </button>
                </div>
              </div>
              <div v-else>
                <p class="text-amber-800">{{ comment.comment }}</p>
                <p class="text-sm text-amber-600 mt-1">Por: {{ comment.username }}</p>
                <div v-if="iduser == comment.iduser || type == 'admin'" class="flex space-x-2 mt-2">
                  <button @click="startEditComment(comment)" class="px-3 py-1 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-sm transition duration-300">
                    Editar
                  </button>
                  <button @click="deleteComment(comment.id)" class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm transition duration-300">
                    Eliminar
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="bg-amber-50 p-4 rounded-lg border border-amber-200 text-center text-amber-700 mb-6">
            No hay comentarios aún. ¡Sé el primero en comentar!
          </div>
  
          <!-- Formulario de comentario -->
          <div v-if="userToken" class="mt-4">
            <textarea v-model="comment" rows="3" placeholder="Escribe tu comentario..." 
                      class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"></textarea>
            <button @click.prevent="createComment" 
                    class="mt-2 w-full py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition duration-300">
              Enviar Comentario
            </button>
          </div>
          <div v-else class="text-center py-4">
            <router-link to="/login" class="text-amber-600 hover:text-amber-800 font-medium">
              Inicia sesión para dejar un comentario
            </router-link>
          </div>
        </div>
      </div>
  
      <!-- Cargando -->
      <div v-else class="max-w-7xl mx-auto text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600"></div>
        <p class="mt-4 text-amber-700">Cargando receta...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { useRoute } from 'vue-router';
  import 'font-awesome/css/font-awesome.min.css';
  
  const route = useRoute();
  const router = useRouter();
  const recipeId = route.query.id;
  const receta = ref(null);
  const comment = ref("");
  const userToken = localStorage.getItem('userToken');
  const iduser = localStorage.getItem('iduser');
  const type = localStorage.getItem('type')
  const ingredients = ref([]);
  const quantity = ref([]);
  const steps = ref([]);
  const comments = ref([]);
  const isFavorite = ref(false);
  const editingCommentId = ref(null);
  const editedComment = ref("");
  const payload = {
      idrecipe: parseInt(recipeId),
      userToken: userToken,
      comment: "",
      iduser: iduser,
      idcomment: 0
  };
  const toggleFavorite = () => {
      if (iduser) {
          isFavorite.value = !isFavorite.value;
          if (isFavorite.value) {
              axios
                  .post('http://localhost:5000/updateFavs', payload)
                  .then(response => {
                      console.log(response.data.message)
                  })
                  .catch(error => {
                      console.error("Error en la solicitud:", error);
                  });
          } else {
              axios
                  .post('http://localhost:5000/deleteFavs', payload)
                  .then(response => {
                      console.log(response.data.message)
                  })
                  .catch(error => {
                      console.error("Error en la solicitud:", error);
                  });
          }
      } else {
          router.push({ name: "login" });
      }
  };
  
  function fetchRecipe() {
      axios
          .post('http://localhost:5000/viewComment', payload)
          .then(response => {
              comments.value = response.data.comment_list;
          })
          .catch(error => console.error("Error en la solicitud:", error));
  }
  
  onMounted(() => {
      axios
          .post('http://localhost:5000/viewRecipe', payload)
          .then(response => {
              receta.value = response.data.recipe_list[0]
              response.data.ingredient_list.forEach(element => {
                  ingredients.value.push(element.ingredients);
                  quantity.value.push(element.quantity)
              });
              steps.value = response.data.step_list;
              fetchRecipe();
              if (iduser) {
                  response.data.favorites_list.forEach(id => {
                      if (id.id_recipe === parseInt(recipeId)) {
                          isFavorite.value = true;
                      }
                  });
              }
          })
          .catch(error => {
              console.error("Error en la solicitud:", error);
          });
  });
  
  function deleteRecipe() {
      if (confirm('¿Estás seguro de que quieres eliminar esta receta?')) {
          axios
              .post('http://localhost:5000/deleteRecipe', payload)
              .then(response => {
                  console.log(response.data.message);
                  router.push({ name: "home" });
              })
              .catch(error => {
                  console.error("Error en la solicitud:", error);
              });
      }
  }
  
  function editeRecipe() {
      router.push({ name: "edite", query: { id: recipeId } });
  }
  
  function createComment() {
      payload.comment = comment.value;
      if (userToken) {
          axios.post('http://localhost:5000/createComment', payload)
              .then(() => {
                  fetchRecipe();
                  comment.value = "";
              })
              .catch(error => console.error("Error en la solicitud:", error));
      } else {
          router.push({ name: "login" });
      }
  }
  
  function deleteComment(idcomment) {
      if (confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
          payload.idcomment = idcomment;
          axios.post('http://localhost:5000/deleteComment', payload)
              .then(() => {
                  fetchRecipe();
              })
              .catch(error => console.error("Error en la solicitud:", error));
      }
  }
  
  function updateComment(idcomment) {
      payload.idcomment = idcomment;
      payload.comment = editedComment.value;
      axios.post('http://localhost:5000/editeComment', payload)
          .then(() => {
              fetchRecipe();
              cancelEdit();
          })
          .catch(error => console.error("Error en la solicitud:", error));
  }
  
  function startEditComment(comment) {
      editingCommentId.value = comment.id;
      editedComment.value = comment.comment;
  }
  
  function cancelEdit() {
      editingCommentId.value = null;
      editedComment.value = "";
  }
  </script>
  
  <style scoped>
  /* Animación para el corazón de favoritos */
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }
  
  .fa-heart {
    animation: pulse 1.5s infinite;
  }
  
  /* Transición para los comentarios */
  .comment-enter-active,
  .comment-leave-active {
    transition: all 0.3s ease;
  }
  
  .comment-enter-from,
  .comment-leave-to {
    opacity: 0;
    transform: translateY(10px);
  }
  
  /* Efecto para las imágenes al hacer hover */
  img:hover {
    transform: scale(1.02);
    transition: transform 0.3s ease;
  }
  </style>