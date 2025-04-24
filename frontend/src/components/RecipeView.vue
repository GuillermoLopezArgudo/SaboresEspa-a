<template>
  <div class="min-h-screen bg-amber-50 py-4 px-2 sm:px-4 lg:px-8">
    <!-- Encabezado -->
    <div class="max-w-7xl mx-auto text-center mb-4 sm:mb-6">
      <h1
        class="text-2xl sm:text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-2">
        Detalle de Receta
      </h1>
    </div>

    <!-- Botón de regreso -->
    <div class="max-w-7xl mx-auto mb-4 sm:mb-6">
      <router-link to="/"
        class="inline-flex items-center px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base bg-amber-700 hover:bg-amber-800 text-white rounded-lg transition duration-300 shadow-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2" viewBox="0 0 20 20"
          fill="currentColor">
          <path fill-rule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd" />
        </svg>
        Volver al inicio
      </router-link>
    </div>

    <!-- Contenido principal -->
    <div v-if="receta" class="max-w-7xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden border border-amber-200">
      <!-- Sección superior -->

      <div class="p-4 sm:p-6 md:p-8 border-b border-amber-100 bg-gradient-to-r from-amber-50 to-white">
        <div class="flex flex-col sm:flex-row justify-between items-start gap-4">
          <div class="w-full">
            <div class="flex justify-between items-center">
              <!-- Título -->
              <h2 class="text-xl sm:text-2xl md:text-3xl font-bold text-amber-800 font-serif">{{ receta.title }}</h2>

              <!-- Contenedor del botón -->
              <div class="relative" ref="menuRecipeRef">
                <!-- Botón tres puntitos -->
                <button @click="toggleMenuRecipe"
                  class="px-3 py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-sm transition duration-300 flex items-center">
                  <i class="fa fa-ellipsis-h text-sm mr-1"></i>
                </button>

                <!-- Menú desplegable -->
                <div v-if="istoggleMenuRecipe"
                  class="absolute right-0 mt-2 w-44 bg-white shadow-lg rounded-lg z-50 flex flex-col gap-2 p-2">

                  <!-- Botón de reporte -->
                  <template v-if="userToken != 'notoken'">
                    <button v-if="userToken" @click="showReportDialog"
                      class="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium bg-red-100 hover:bg-red-200 text-red-600 rounded-lg transition duration-200">
                      <i class="fa fa-flag text-sm"></i>
                      Reportar
                    </button>
                  </template>

                  <!-- Editar / Eliminar -->
                  <template v-if="userToken == receta.userToken || type == 'admin'">
                    <button @click="editeRecipe"
                      class="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-amber-500 hover:bg-amber-600 rounded-lg transition duration-200">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      Editar
                    </button>

                    <button @click="deleteRecipe"
                      class="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-red-500 hover:bg-red-600 rounded-lg transition duration-200">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Eliminar
                    </button>
                  </template>
                </div>
              </div>
            </div>

            <div class="mt-1 sm:mt-2 inline-block bg-amber-100 px-2 py-0.5 sm:px-3 sm:py-1 rounded-full">
              <span class="text-xs sm:text-sm text-amber-700 font-medium">Por </span>
              <span class="text-xs sm:text-sm text-amber-800 font-semibold">{{ receta.user_name }}</span>
            </div>
            <button @click="toggleFavorite"
              class="mt-2 sm:mt-3 flex items-center text-red-500 hover:text-red-600 transition duration-300 text-sm sm:text-base">
              <i class="fa text-xl sm:text-2xl mr-1 sm:mr-2" :class="isFavorite ? 'fa-heart' : 'fa-heart-o'"></i>
              <span class="font-medium">{{ isFavorite ? 'En favoritos' : 'Añadir a favoritos' }}</span>
            </button>
          </div>


        </div>
        <p class="mt-2 sm:mt-4 text-amber-700 text-sm sm:text-base md:text-lg">{{ receta.description }}</p>
      </div>

      <!-- Imagen de la receta -->
      <div v-if="receta.image" class="p-4 sm:p-6 md:p-8">
        <div class="rounded-xl overflow-hidden shadow-md border border-amber-200">
          <img :src="`http://48.217.185.80/api/${receta.image}`" alt="Imagen de la receta"
            class="w-full h-auto object-cover">
        </div>
      </div>

      <!-- Ingredientes -->
      <div v-if="ingredients.length > 0" class="p-4 sm:p-6 md:p-8 border-t border-amber-100">
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 mb-2 sm:mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes Receta
        </h3>
        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
          <li v-for="(ingrediente, idx) in ingredients" :key="idx"
            class="bg-amber-50 p-2 sm:p-3 rounded-lg border border-amber-200 hover:bg-amber-100 transition duration-200">
            <span class="font-medium text-amber-800 text-sm sm:text-base">{{ ingrediente }}</span>
            <span class="block text-amber-600 text-xs sm:text-sm">{{ quantity[idx] || 'Cantidad no disponible' }}</span>
          </li>
        </ul>
      </div>

      <!-- Pasos de la receta -->
      <div v-if="steps.length > 0" class="p-4 sm:p-6 md:p-8 border-t border-amber-100">
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 mb-2 sm:mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Pasos de Preparación Receta
        </h3>
        <div class="space-y-3 sm:space-y-4 md:space-y-6">
          <div v-for="(step, idx) in steps" :key="idx"
            class="bg-white p-3 sm:p-4 md:p-5 rounded-xl border border-amber-200 shadow-sm hover:shadow-md transition duration-300">
            <div class="flex items-start">
              <span
                class="bg-amber-600 text-white font-bold rounded-full w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 flex items-center justify-center mr-2 sm:mr-3 md:mr-4 flex-shrink-0 text-xs sm:text-sm md:text-base">
                {{ idx + 1 }}
              </span>
              <div>
                <h4 class="font-semibold text-amber-800 text-base sm:text-lg">{{ step.title }}</h4>
                <p class="text-amber-700 mt-0.5 sm:mt-1 text-sm sm:text-base">{{ step.description }}</p>
                <div v-if="step.image" class="mt-2 sm:mt-3 rounded-lg overflow-hidden border border-amber-200">
                  <img :src="`http://48.217.185.80/api/${step.image}`" :alt="`Imagen del paso ${idx + 1}`"
                    class="w-full max-w-md">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ingredientes SubReceta -->
      <div v-if="subingredients.length > 0" class="p-4 sm:p-6 md:p-8 border-t border-amber-100">
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 mb-2 sm:mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes SubReceta
        </h3>
        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
          <li v-for="(ingrediente, idx) in subingredients" :key="idx"
            class="bg-amber-50 p-2 sm:p-3 rounded-lg border border-amber-200 hover:bg-amber-100 transition duration-200">
            <span class="font-medium text-amber-800 text-sm sm:text-base">{{ ingrediente }}</span>
            <span class="block text-amber-600 text-xs sm:text-sm">{{ quantity[idx] || 'Cantidad no disponible' }}</span>
          </li>
        </ul>
      </div>

      <!-- Pasos de la Subreceta -->
      <div v-if="substeps.length > 0" class="p-4 sm:p-6 md:p-8 border-t border-amber-100">
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 mb-2 sm:mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Pasos de Preparación SubReceta
        </h3>
        <div class="space-y-3 sm:space-y-4 md:space-y-6">
          <div v-for="(step, idx) in substeps" :key="idx"
            class="bg-white p-3 sm:p-4 md:p-5 rounded-xl border border-amber-200 shadow-sm hover:shadow-md transition duration-300">
            <div class="flex items-start">
              <span
                class="bg-amber-600 text-white font-bold rounded-full w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 flex items-center justify-center mr-2 sm:mr-3 md:mr-4 flex-shrink-0 text-xs sm:text-sm md:text-base">
                {{ idx + 1 }}
              </span>
              <div>
                <h4 class="font-semibold text-amber-800 text-base sm:text-lg">{{ step.title }}</h4>
                <p class="text-amber-700 mt-0.5 sm:mt-1 text-sm sm:text-base">{{ step.description }}</p>
                <div v-if="step.image" class="mt-2 sm:mt-3 rounded-lg overflow-hidden border border-amber-200">
                  <img :src="`http://48.217.185.80/api/${step.image}`" :alt="`Imagen del paso ${idx + 1}`"
                    class="w-full max-w-md">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Video de la receta -->
      <div v-if="receta.video" class="p-4 sm:p-6 md:p-8 pt-0">
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 mb-2 sm:mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          Video
        </h3>
        <div class="rounded-xl overflow-hidden shadow-md border border-amber-200">
          <video controls :src="'http://48.217.185.80/api/' + receta.video" class="w-full"></video>
        </div>
      </div>

      <!-- Comentarios -->
      <div class="p-4 sm:p-6 md:p-8 border-t border-amber-100">
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 mb-2 sm:mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          Comentarios
        </h3>

        <!-- Lista de comentarios -->
        <div v-if="comments.length > 0" class="space-y-3 sm:space-y-4 md:space-y-6 mb-4 sm:mb-6">
          <div v-for="comment in commentsWithSubcomments" :key="comment.id"
            class="bg-white p-3 sm:p-4 rounded-lg border border-amber-200 shadow-sm hover:shadow-md transition duration-300">
            <!-- Comentario principal -->
            <div class="mb-3 sm:mb-4">
              <div v-if="editingCommentId === comment.id" class="mb-2 sm:mb-3">
                <textarea v-model="editedComment" rows="3"
                  class="resize-none w-full px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border-2 border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300"></textarea>
                <div class="flex flex-wrap gap-1 sm:gap-2 mt-1 sm:mt-2">
                  <button @click="updateComment(comment.id)"
                    class="px-2 py-1 sm:px-4 sm:py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition duration-300 flex items-center text-xs sm:text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1"
                      viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd" />
                    </svg>
                    Guardar
                  </button>
                  <button @click="cancelEdit"
                    class="px-2 py-1 sm:px-4 sm:py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition duration-300 flex items-center text-xs sm:text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1"
                      viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                    Cancelar
                  </button>
                </div>
              </div>
              <div v-else>
                <!-- Contenedor del botón -->
                <div class="flex justify-end" >
                  <div class="relative" :ref="el => menuRefs[comment.id] = el">
                    <!-- Botón tres puntitos -->
                    <button @click="toggleMenu(comment.id)"
                      class="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-xs sm:text-sm transition duration-300 flex items-center">
                      <i class="fa fa-ellipsis-h text-xs sm:text-sm mr-1"></i>
                    </button>

                    <!-- Menú desplegable -->
                    <div v-if="isMenuVisible[comment.id]"
                      class="absolute right-0 mt-2 w-40 sm:w-44 bg-white shadow-lg rounded-lg z-50 flex flex-col gap-1 p-1 sm:p-2">

                      <!-- BOTÓN: Reportar -->
                      <button v-if="userToken" @click="showCommentReportDialog(comment.id)"
                        class="w-full flex items-center px-2 py-1 text-red-600 bg-red-100 hover:bg-red-200 rounded text-xs sm:text-sm transition">
                        <i class="fa fa-flag mr-1"></i> Reportar
                      </button>

                      <!-- BOTÓN: Editar -->
                      <button v-if="userToken == comment.userToken || type == 'admin'"
                        @click="startEditComment(comment)"
                        class="w-full flex items-center px-2 py-1 text-white bg-amber-500 hover:bg-amber-600 rounded text-xs sm:text-sm transition">
                        <i class="fa fa-pencil mr-1"></i> Editar
                      </button>

                      <!-- BOTÓN: Eliminar -->
                      <button v-if="userToken == comment.userToken || type == 'admin'"
                        @click="deleteComment(comment.id)"
                        class="w-full flex items-center px-2 py-1 text-white bg-red-500 hover:bg-red-600 rounded text-xs sm:text-sm transition">
                        <i class="fa fa-trash mr-1"></i> Eliminar
                      </button>
                    </div>
                  </div>
                </div>
                <p
                  class="text-amber-800 text-sm sm:text-base break-words w-full max-w-[90%] sm:max-w-[90%] md:max-w-[95%] lg:max-w-[90%]">
                  {{ comment.comment }}</p>
                <p class="text-xs text-amber-600 mt-0.5 sm:mt-1">Por: {{ comment.username }}</p>
                <div class="flex flex-wrap items-center gap-1 sm:gap-2 mt-1 sm:mt-2">
                  <!-- Botones de interacción -->
                  <div class="flex gap-1 sm:gap-2 items-center">
                    <!-- LIKE -->
                    <button @click="toggleLike(comment.id)"
                      class="focus:outline-none flex items-center gap-0.5 sm:gap-1">
                      <svg class="w-4 h-4 sm:w-5 sm:h-5 transition text-green-800 hover:text-green-900"
                        :fill="likedComments[comment.id] ? 'currentColor' : 'none'" xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M7 11c.889-.086 1.416-.543 2.156-1.057a22.323 22.323 0 0 0 3.958-5.084 1.6 1.6 0 0 1 .582-.628 1.549 1.549 0 0 1 1.466-.087c.205.095.388.233.537.406a1.64 1.64 0 0 1 .384 1.279l-1.388 4.114M7 11H4v6.5A1.5 1.5 0 0 0 5.5 19v0A1.5 1.5 0 0 0 7 17.5V11Zm6.5-1h4.915c.286 0 .372.014.626.15.254.135.472.332.637.572a1.874 1.874 0 0 1 .215 1.673l-2.098 6.4C17.538 19.52 17.368 20 16.12 20c-2.303 0-4.79-.943-6.67-1.475" />
                      </svg>
                      <span class="text-green-800 text-xs sm:text-sm">{{ conteoLikes[comment.id] || 0 }}</span>
                    </button>
                    <!-- DISLIKE -->
                    <button @click="toggleDislike(comment.id)"
                      class="focus:outline-none flex items-center gap-0.5 sm:gap-1">
                      <svg class="w-4 h-4 sm:w-5 sm:h-5 transition text-red-600 hover:text-red-700"
                        :fill="dislikedComments[comment.id] ? 'currentColor' : 'none'"
                        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 13c-.889.086-1.416.543-2.156 1.057a22.322 22.322 0 0 0-3.958 5.084 1.6 1.6 0 0 1-.582.628 1.549 1.549 0 0 1-1.466.087 1.587 1.587 0 0 1-.537-.406 1.666 1.666 0 0 1-.384-1.279l1.389-4.114M17 13h3V6.5A1.5 1.5 0 0 0 18.5 5v0A1.5 1.5 0 0 0 17 6.5V13Zm-6.5 1H5.585c-.286 0-.372-.014-.626-.15a1.797 1.797 0 0 1-.637-.572 1.873 1.873 0 0 1-.215-1.673l2.098-6.4C6.462 4.48 6.632 4 7.88 4c2.302 0 4.79.943 6.67 1.475" />
                      </svg>
                      <span class="text-red-600 text-xs sm:text-sm">{{ conteoDisLikes[comment.id] || 0 }}</span>
                    </button>
                  </div>
                  <!-- BOTON DE RESPUESTA -->
                  <div class="ml-auto">
                    <button @click="toggleReply(comment.id)"
                      class="px-2 py-0.5 sm:px-3 sm:py-1 bg-blue-100 hover:bg-blue-200 text-blue-600 rounded-lg text-xs sm:text-sm transition duration-300 flex items-center">
                      <i class="fa fa-reply text-xs sm:text-sm mr-0.5 sm:mr-1"></i> Responder
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Subcomentarios -->
            <div v-if="comment.subcomments && comment.subcomments.length > 0"
              class="ml-4 sm:ml-6 md:ml-8 pl-2 sm:pl-3 md:pl-4 border-l-2 border-amber-200 space-y-2 sm:space-y-3">
              <div v-for="subcomment in comment.subcomments" :key="subcomment.id"
                class="bg-amber-50 p-2 sm:p-3 rounded-lg">
                <div v-if="editingSubcommentId === subcomment.id">
                  <textarea v-model="editedSubcomment" rows="2"
                    class="resize-none w-full px-2 py-1 sm:px-3 sm:py-1 text-sm sm:text-base rounded-lg border-2 border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300"></textarea>
                  <div class="flex flex-wrap gap-1 sm:gap-2 mt-1 sm:mt-2">
                    <button @click="updateSubcomment(subcomment.id)"
                      class="px-2 py-0.5 sm:px-3 sm:py-1 bg-green-500 hover:bg-green-600 text-white rounded text-xs sm:text-sm">
                      Guardar
                    </button>
                    <button @click="cancelEditSubcomment"
                      class="px-2 py-0.5 sm:px-3 sm:py-1 bg-gray-400 hover:bg-gray-500 text-white rounded text-xs sm:text-sm">
                      Cancelar
                    </button>
                  </div>
                </div>
                <div v-else>
                  <!-- Botón que activa el submenú -->
                  <div class="flex justify-end">
                    <div class="relative" :ref="el => subMenuRefs[subcomment.id] = el">
                      <button @click="toggleSubMenu(subcomment.id)"
                        class="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-xs sm:text-sm transition duration-300 flex items-center">
                        <i class="fa fa-ellipsis-h text-xs sm:text-sm mr-1"></i>
                      </button>

                      <!-- Menú desplegable -->
                      <div v-if="isSubMenuVisible[subcomment.id]"
                        class="absolute right-0 mt-2 w-40 sm:w-44 bg-white shadow-lg rounded-lg z-50 flex flex-col gap-1 p-1 sm:p-2">

                        <!-- BOTÓN: Reportar -->
                        <button v-if="userToken" @click="showCommentReportDialog(subcomment.id)"
                          class="w-full flex items-center px-2 py-1 text-red-600 bg-red-100 hover:bg-red-200 rounded text-xs sm:text-sm transition">
                          <i class="fa fa-flag mr-1"></i> Reportar
                        </button>

                        <!-- BOTÓN: Editar -->
                        <button v-if="userToken == subcomment.userToken || type == 'admin'"
                          @click="startEditSubcomment(subcomment)"
                          class="w-full flex items-center px-2 py-1 text-white bg-amber-400 hover:bg-amber-500 rounded text-xs sm:text-sm transition">
                          <i class="fa fa-pencil mr-1"></i> Editar
                        </button>

                        <!-- BOTÓN: Eliminar -->
                        <button v-if="userToken == subcomment.userToken || type == 'admin'"
                          @click="deleteSubcomment(subcomment.id)"
                          class="w-full flex items-center px-2 py-1 text-white bg-red-400 hover:bg-red-500 rounded text-xs sm:text-sm transition">
                          <i class="fa fa-trash mr-1"></i> Eliminar
                        </button>
                      </div>
                    </div>
                  </div>

                  <p
                    class="text-amber-700 text-sm sm:text-base break-words w-full max-w-[90%] sm:max-w-[90%] md:max-w-[90%] lg:max-w-[90%]">
                    {{ subcomment.comment }}</p>
                  <p class="text-xs text-amber-500 mt-0.5 sm:mt-1">Por: {{ subcomment.username }}</p>

                </div>
              </div>
            </div>

            <!-- Formulario de respuesta (subcomentario) -->
            <div v-if="replyingTo === comment.id" class="mt-2 sm:mt-3 ml-4 sm:ml-6 md:ml-8">
              <textarea v-model="replyComment" rows="2" placeholder="Escribe tu respuesta..."
                class="resize-none w-full px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border-2 border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300"></textarea>
              <div class="flex flex-wrap gap-1 sm:gap-2 mt-1 sm:mt-2">
                <button @click="createSubcomment(comment.id)"
                  class="px-2 py-1 sm:px-4 sm:py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg transition duration-300 text-xs sm:text-sm">
                  Enviar respuesta
                </button>
                <button @click="cancelReply"
                  class="px-2 py-1 sm:px-4 sm:py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition duration-300 text-xs sm:text-sm">
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else
          class="bg-amber-50 p-3 sm:p-4 rounded-lg border border-amber-200 text-center text-amber-700 mb-4 sm:mb-6 text-sm sm:text-base">
          No hay comentarios aún. ¡Sé el primero en comentar!
        </div>

        <!-- Formulario de comentario principal -->
        <div v-if="userToken !== 'notoken'" class="mt-3 sm:mt-4">
          <textarea v-model="newComment" rows="3" placeholder="Escribe tu comentario..."
            class="resize-none resize-none w-full px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border-2 border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300"></textarea>
          <button @click="createComment"
            class="mt-1 sm:mt-2 w-full py-1.5 sm:py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition duration-300 flex items-center justify-center text-sm sm:text-base">
            <i class="fa fa-paper-plane text-xs sm:text-sm mr-1 sm:mr-2"></i> Enviar Comentario
          </button>
        </div>
        <div v-else class="text-center py-2 sm:py-4 text-sm sm:text-base">
          <router-link to="/login" class="text-amber-600 hover:text-amber-800 font-medium">
            Inicia sesión para dejar un comentario
          </router-link>
        </div>
      </div>
    </div>

    <!-- Cargando -->
    <div v-else class="max-w-7xl mx-auto text-center py-8 sm:py-12">
      <div
        class="inline-block animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 border-t-2 border-b-2 border-amber-600">
      </div>
      <p class="mt-3 sm:mt-4 text-amber-700 text-sm sm:text-base">Cargando receta...</p>
    </div>

    <!-- Diálogo de reporte de receta -->
    <div v-if="showReportModal" @click.self="showReportModal = false"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2 sm:p-4" >
      <div class="bg-white rounded-xl shadow-2xl overflow-hidden w-full max-w-xs sm:max-w-md" >
        <!-- Encabezado con degradado -->
        <div class="bg-gradient-to-r from-amber-600 to-amber-800 p-3 sm:p-4">
          <h3 class="text-lg sm:text-xl font-bold text-white font-serif">Reportar Receta</h3>
        </div>

        <!-- Contenido -->
        <div class="p-4 sm:p-6">
          <div class="mb-3 sm:mb-5">
            <label class="block text-amber-800 font-medium mb-1 sm:mb-2 text-sm sm:text-base">Motivo del reporte</label>
            <select v-model="reportReason"
              class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base border-2 border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300">
              <option value="" disabled selected>Selecciona un motivo</option>
              <option value="Contenido inapropiado">Contenido inapropiado</option>
              <option value="Información incorrecta">Información incorrecta</option>
              <option value="Derechos de autor">Derechos de autor</option>
              <option value="Spam o publicidad">Spam o publicidad</option>
              <option value="Otro">Otro</option>
            </select>
          </div>

          <div v-if="reportReason === 'Otro'" class="mb-3 sm:mb-5">
            <label class="block text-amber-800 font-medium mb-1 sm:mb-2 text-sm sm:text-base">Explica el
              problema</label>
            <textarea v-model="customReason" rows="3" placeholder="Por favor, describe el problema en detalle..."
              class="resize-none resize-none w-full px-3 py-2 text-sm sm:text-base border-2 border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300"></textarea>
          </div>

          <div class="flex justify-end space-x-2 sm:space-x-3 pt-1 sm:pt-2">
            <button @click="cancelReport"
              class="px-3 py-1.5 sm:px-4 sm:py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition duration-300 flex items-center text-xs sm:text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
              Cancelar
            </button>
            <button @click="submitReportRecipe"
              class="px-3 py-1.5 sm:px-4 sm:py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition duration-300 flex items-center shadow-md text-xs sm:text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd" />
              </svg>
              Enviar Reporte
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Diálogo de reporte de comentario -->
    <div v-if="showCommentReportModal" @click.self="showCommentReportModal = false"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2 sm:p-4">
      <div class="bg-white rounded-xl shadow-2xl overflow-hidden w-full max-w-xs sm:max-w-md">
        <!-- Encabezado con degradado -->
        <div class="bg-gradient-to-r from-amber-600 to-amber-800 p-3 sm:p-4">
          <h3 class="text-lg sm:text-xl font-bold text-white font-serif">Reportar Comentario</h3>
        </div>

        <!-- Contenido -->
        <div class="p-4 sm:p-6">
          <div class="mb-3 sm:mb-5">
            <label class="block text-amber-800 font-medium mb-1 sm:mb-2 text-sm sm:text-base">Motivo del reporte</label>
            <select v-model="commentReportReason"
              class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base border-2 border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300">
              <option value="" disabled selected>Selecciona un motivo</option>
              <option value="Contenido inapropiado">Contenido inapropiado</option>
              <option value="Lenguaje ofensivo">Lenguaje ofensivo</option>
              <option value="Spam o publicidad">Spam o publicidad</option>
              <option value="Información falsa">Información falsa</option>
              <option value="Otro">Otro</option>
            </select>
          </div>

          <div v-if="commentReportReason === 'Otro'" class="mb-3 sm:mb-5">
            <label class="block text-amber-800 font-medium mb-1 sm:mb-2 text-sm sm:text-base">Explica el
              problema</label>
            <textarea v-model="commentCustomReason" rows="3" placeholder="Por favor, describe el problema en detalle..."
              class="resize-none w-full px-3 py-2 text-sm sm:text-base border-2 border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition duration-300"></textarea>
          </div>

          <div class="flex justify-end space-x-2 sm:space-x-3 pt-1 sm:pt-2">
            <button @click="cancelCommentReport"
              class="px-3 py-1.5 sm:px-4 sm:py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition duration-300 flex items-center text-xs sm:text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
              Cancelar
            </button>
            <button @click="submitCommentReport"
              class="px-3 py-1.5 sm:px-4 sm:py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition duration-300 flex items-center shadow-md text-xs sm:text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd" />
              </svg>
              Enviar Reporte
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed,onBeforeUnmount  } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import 'font-awesome/css/font-awesome.min.css';
import { useToast } from 'vue-toastification'

const route = useRoute();
const router = useRouter();
const recipeId = route.query.id;
const receta = ref(null);
const newComment = ref("");
const replyComment = ref("");
const userToken = ref(localStorage.getItem('userToken') || "notoken");
const ingredients = ref([]);
const quantity = ref([]);
const steps = ref([]);
const subingredients = ref([]);
const subquantity = ref([]);
const substeps = ref([]);
const comments = ref([]);
const subcomments = ref([]);
const isFavorite = ref(false);
const editingCommentId = ref(null);
const editingSubcommentId = ref(null);
const editedComment = ref("");
const editedSubcomment = ref("");
const showReportModal = ref(false);
const reportReason = ref('');
const customReason = ref('');
const showCommentReportModal = ref(false);
const commentReportReason = ref('');
const commentCustomReason = ref('');
const currentCommentId = ref(null);
const type = ref("");
const likedComments = ref({});
const dislikedComments = ref({});
const conteoLikes = ref({});
const conteoDisLikes = ref({});
const replyingTo = ref(null);
const toast = useToast()
const isMenuVisible = ref({});
const isSubMenuVisible = ref({});
const istoggleMenuRecipe = ref(false)
const menuRecipeRef = ref(null);
const menuRefs = ref({});
const subMenuRefs = ref({});
const reportModalRef = ref(null);
const commentReportModalRef = ref(null);

const payload = {
  idrecipe: parseInt(recipeId),
  userToken: userToken.value,
  comment: "",
  idcomment: 0
};

const commentsWithSubcomments = computed(() => {
  return comments.value.map(comment => {
    return {
      ...comment,
      subcomments: subcomments.value.filter(sub => sub.id_comment === comment.id)
    };
  });
});

const toggleFavorite = () => {
  if (userToken.value) {
    isFavorite.value = !isFavorite.value;
    if (isFavorite.value) {
      axios
        .post(`${process.env.VUE_APP_API_URL}/updateFavs`, payload)
        .then(response => {
          console.log(response.data.message)
        })
        .catch(error => {
          console.error("Error en la solicitud:", error);
        });
    } else {
      axios
        .post(`${process.env.VUE_APP_API_URL}/deleteFavs`, payload)
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
    .post(`${process.env.VUE_APP_API_URL}/viewComment`, payload)
    .then(response => {
      comments.value = response.data.comment_list;
      subcomments.value = response.data.subcomments_list || [];
    })
    .catch(error => console.error("Error en la solicitud:", error));
}

onMounted(() => {
  axios
    .post(`${process.env.VUE_APP_API_URL}/viewRecipe`, payload)
    .then(response => {
      if (response.data.recipe_list[0].id_user == response.data.user_id) {
        response.data.recipe_list[0].userToken = response.data.user_token;
      }
      response.data.recipe_list[0].user_name = response.data.user_name;
      receta.value = response.data.recipe_list[0];

      response.data.ingredient_list.forEach(element => {
        ingredients.value.push(element.ingredients);
        quantity.value.push(element.quantity);
      });

      steps.value = response.data.step_list;

      response.data.subingredient_list.forEach(element => {
        subingredients.value.push(element.ingredients);
        subquantity.value.push(element.quantity);
      });

      substeps.value = response.data.substep_list;
      type.value = response.data.user_type;

      fetchRecipe();

      conteoLikes.value = response.data.countLikes_list?.reduce((acc, item) => {
        const id = item.id_comment;
        acc[id] = (acc[id] || 0) + 1;
        return acc;
      }, {}) || {};

      conteoDisLikes.value = response.data.countDisLikes_list?.reduce((acc, item) => {
        const id = item.id_comment;
        acc[id] = (acc[id] || 0) + 1;
        return acc;
      }, {}) || {};

      if (response.data.user_token) {
        response.data.favorites_list?.forEach(id => {
          if (id.id_recipe === parseInt(recipeId)) {
            isFavorite.value = true;
          }
        });

        response.data.likes_list?.forEach(element => {
          likedComments.value[element.id_recipe] = true;
        });

        response.data.dislikes_list?.forEach(element => {
          dislikedComments.value[element.id_recipe] = true;
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
      .post(`${process.env.VUE_APP_API_URL}/deleteRecipe`, payload)
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
  if (!newComment.value.trim()) return;

  payload.comment = newComment.value;
  payload.idcomment = 0; // Reset para comentario principal

  axios.post(`${process.env.VUE_APP_API_URL}/createComment`, payload)
    .then(() => {
      fetchRecipe();
      newComment.value = "";
    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
      if (error.response?.status === 401) {
        router.push({ name: "login" });
      }
    });
}

function createSubcomment(commentId) {
  if (!replyComment.value.trim()) return;

  payload.comment = replyComment.value;
  payload.idcomment = commentId;

  axios.post(`${process.env.VUE_APP_API_URL}/createSubComment`, payload)
    .then(() => {
      fetchRecipe();
      replyComment.value = "";
      replyingTo.value = null;
    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
      if (error.response?.status === 401) {
        router.push({ name: "login" });
      }
    });

}

function deleteComment(idcomment) {
  if (confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
    payload.idcomment = idcomment;
    axios.post(`${process.env.VUE_APP_API_URL}/deleteComment`, payload)
      .then(() => {
        fetchRecipe();
      })
      .catch(error => console.error("Error en la solicitud:", error));
  }
}

function deleteSubcomment(idcomment) {
  if (confirm('¿Estás seguro de que quieres eliminar esta respuesta?')) {
    payload.idcomment = idcomment;
    axios.post(`${process.env.VUE_APP_API_URL}/deleteSubComment`, payload)
      .then(() => {
        fetchRecipe();
      })
      .catch(error => console.error("Error en la solicitud:", error));
  }
}

function updateComment(idcomment) {
  payload.idcomment = idcomment;
  payload.comment = editedComment.value;
  axios.post(`${process.env.VUE_APP_API_URL}/editeComment`, payload)
    .then(() => {
      fetchRecipe();
      cancelEdit();
    })
    .catch(error => console.error("Error en la solicitud:", error));
}

function updateSubcomment(idcomment) {
  payload.idcomment = idcomment;
  payload.comment = editedSubcomment.value;
  axios.post(`${process.env.VUE_APP_API_URL}/editeSubComment`, payload)
    .then(response => {
      console.log(response.data.message)
      fetchRecipe();
      cancelEditSubcomment();
    })
    .catch(error => console.error("Error en la solicitud:", error));
}

function startEditComment(comment) {
  editingCommentId.value = comment.id;
  editedComment.value = comment.comment;
}

function startEditSubcomment(subcomment) {
  editingSubcommentId.value = subcomment.id;
  editedSubcomment.value = subcomment.comment;
}

function cancelEdit() {
  editingCommentId.value = null;
  editedComment.value = "";
}

function cancelEditSubcomment() {
  editingSubcommentId.value = null;
  editedSubcomment.value = "";
}

function toggleReply(commentId) {
  replyingTo.value = replyingTo.value === commentId ? null : commentId;
  if (replyingTo.value === commentId) {
    replyComment.value = "";
  }
}

function cancelReply() {
  replyingTo.value = null;
  replyComment.value = "";
}

function cancelReport() {
  showReportModal.value = false;
}

function showReportDialog() {
  showReportModal.value = true;
  reportReason.value = '';
  customReason.value = '';
}

function submitReportRecipe() {
  if (!reportReason.value) {
    toast.warning('Por favor selecciona un motivo para el reporte');
    return;
  }

  const reason = reportReason.value === 'Otro' ? customReason.value : reportReason.value;

  axios.post(`${process.env.VUE_APP_API_URL}/report-recipe`, {
    idrecipe: recipeId,
    reason: reason,
    usertoken: userToken.value
  })
    .then(() => {
      toast.success('Gracias por tu reporte. Hemos notificado al equipo administrativo.');
      showReportModal.value = false;
    })
    .catch(error => {
      console.error("Error al reportar:", error);
      toast.error('Ocurrió un error al enviar el reporte. Por favor intenta nuevamente.');
    });
}

const showCommentReportDialog = (commentId) => {
  currentCommentId.value = commentId;
  commentReportReason.value = '';
  commentCustomReason.value = '';
  showCommentReportModal.value = true;
};

const cancelCommentReport = () => {
  showCommentReportModal.value = false;
};

const submitCommentReport = async () => {

  if (!commentReportReason.value) {
    toast.error('Por favor selecciona un motivo para el reporte');
    return;
  }

  const reason = commentReportReason.value === 'Otro'
    ? commentCustomReason.value
    : commentReportReason.value;

  try {


    const response = await axios.post(`${process.env.VUE_APP_API_URL}/report-comment`, {
      commentId: currentCommentId.value,
      reason: reason,
      userToken: userToken.value
    });

    if (response.data.message) {
      toast.success('Reporte enviado correctamente. Gracias por ayudar a mejorar la comunidad.');
    }
  } catch (error) {
    console.error("Error al reportar:", error);
    toast.error('Ocurrió un error al enviar el reporte. Por favor intenta nuevamente.');
  } finally {
    showCommentReportModal.value = false;
  }
};

const toggleLike = (commentId) => {
  if (!likedComments.value[commentId]) {
    likedComments.value[commentId] = !likedComments.value[commentId];

    if (likedComments.value[commentId]) {
      dislikedComments.value[commentId] = false;
    }

    payload.idcomment = commentId;
    axios.post(`${process.env.VUE_APP_API_URL}/likeComment`, payload)
      .then(() => {
        conteoLikes.value[commentId] = (conteoLikes.value[commentId] || 0) + 1;
        if (conteoDisLikes.value[commentId] > 0) {
          conteoDisLikes.value[commentId] = (conteoDisLikes.value[commentId] || 0) - 1;
        }
        fetchRecipe();
      })
      .catch(error => console.error("Error en la solicitud:", error));
  } else {
    likedComments.value[commentId] = !likedComments.value[commentId];
    payload.idcomment = commentId;
    axios.post(`${process.env.VUE_APP_API_URL}/deleteLike`, payload)
      .then(() => {
        conteoLikes.value[commentId] = (conteoLikes.value[commentId] || 0) - 1;
        fetchRecipe();
      })
      .catch(error => console.error("Error en la solicitud:", error));
  }
};

const toggleDislike = (commentId) => {
  if (!dislikedComments.value[commentId]) {
    dislikedComments.value[commentId] = !dislikedComments.value[commentId];

    if (dislikedComments.value[commentId]) {
      likedComments.value[commentId] = false;
    }

    payload.idcomment = commentId;
    axios.post(`${process.env.VUE_APP_API_URL}/disLikeComment`, payload)
      .then(() => {
        conteoDisLikes.value[commentId] = (conteoDisLikes.value[commentId] || 0) + 1;
        if (conteoLikes.value[commentId] > 0) {
          conteoLikes.value[commentId] = (conteoLikes.value[commentId] || 0) - 1;
        }
        fetchRecipe();
      })
      .catch(error => console.error("Error en la solicitud:", error));
  } else {
    dislikedComments.value[commentId] = !dislikedComments.value[commentId];
    payload.idcomment = commentId;
    axios.post(`${process.env.VUE_APP_API_URL}/deleteDisLike`, payload)
      .then(() => {
        conteoDisLikes.value[commentId] = (conteoDisLikes.value[commentId] || 0) - 1;
        fetchRecipe();
      })
      .catch(error => console.error("Error en la solicitud:", error));
  }
};

const toggleMenu = (commentId) => {
  isMenuVisible.value[commentId] = !isMenuVisible.value[commentId];
};

const toggleSubMenu = (subCommentId) => {
  isSubMenuVisible.value[subCommentId] = !isSubMenuVisible.value[subCommentId];
};

const toggleMenuRecipe = () => {
  istoggleMenuRecipe.value = !istoggleMenuRecipe.value;
};

const handleClickOutsideRecipeMenu = (event) => {
  if (menuRecipeRef.value && !menuRecipeRef.value.contains(event.target)) {
    istoggleMenuRecipe.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutsideRecipeMenu);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutsideRecipeMenu);
});

const handleClickOutsideCommentMenu = (event) => {
  Object.keys(menuRefs.value).forEach(commentId => {
    if (menuRefs.value[commentId] && !menuRefs.value[commentId].contains(event.target)) {
      isMenuVisible.value[commentId] = false;
    }
  });
};

onMounted(() => {
  document.addEventListener('click', handleClickOutsideCommentMenu);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutsideCommentMenu);
});

const handleClickOutsideSubCommentMenu = (event) => {
  Object.keys(subMenuRefs.value).forEach(subCommentId => {
    if (subMenuRefs.value[subCommentId] && !subMenuRefs.value[subCommentId].contains(event.target)) {
      isSubMenuVisible.value[subCommentId] = false;
    }
  });
};

onMounted(() => {
  document.addEventListener('click', handleClickOutsideSubCommentMenu);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutsideSubCommentMenu);
});

const handleClickOutsideModals = (event) => {
  if (reportModalRef.value && !reportModalRef.value.contains(event.target)) {
    showReportModal.value = false;
  }
  
  if (commentReportModalRef.value && !commentReportModalRef.value.contains(event.target)) {
    showCommentReportModal.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutsideModals);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutsideModals);
})
</script>

<style scoped>
/* Animación para el corazón de favoritos */
@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
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

/* Estilo para subcomentarios */
.subcomment {
  position: relative;
}

.subcomment::before {
  content: "";
  position: absolute;
  left: -20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #f59e0b;
  opacity: 0.3;
}

/* Estilo para el botón de responder */
.reply-btn {
  transition: all 0.2s ease;
}

.reply-btn:hover {
  transform: translateY(-1px);
}

/* Estilo para el área de texto de comentarios */
.comment-textarea {
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.comment-textarea:focus {
  border-color: #f59e0b;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2);
}
</style>