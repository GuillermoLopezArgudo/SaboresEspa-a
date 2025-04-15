<template>
  <div class="min-h-screen bg-amber-50 py-8 px-4 sm:px-6 lg:px-8">
    <!-- Encabezado -->
    <div class="max-w-4xl mx-auto text-center mb-8">
      <h1
        class="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-2">
        Editar Receta
      </h1>
      <p class="text-lg text-amber-700">Actualiza los detalles de tu creación culinaria</p>
    </div>

    <!-- Botón de regreso -->
    <div class="max-w-4xl mx-auto mb-6">
      <router-link to="/home"
        class="inline-flex items-center px-5 py-2.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg transition duration-300 shadow-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd" />
        </svg>
        Volver al inicio
      </router-link>
    </div>

    <!-- Formulario -->
    <form @submit.prevent="submitEditeRecipe"
      class="max-w-4xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden border border-amber-200">
      <!-- Información básica -->
      <div class="p-6 sm:p-8 border-b border-amber-100 bg-gradient-to-r from-amber-50 to-white">
        <h2 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Información Básica
        </h2>

        <!--Ocultar o Mostrar-->
        <label for="descriptionRecipe" class="block text-base font-medium text-amber-700 mb-1">Mostrar / Ocultar
          Receta</label>
        <button @click.prevent="showBasicInfo = !showBasicInfo" class="text-amber-600 hover:text-amber-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="showBasicInfo" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </button>

        <!-- Título -->
        <div class="mb-5">
          <label for="titleRecipe" class="block text-base font-medium text-amber-700 mb-1">Nombre de la receta*</label>
          <input type="text" id="titleRecipe" v-model="title" required
            class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
            placeholder="Ej: Lasagna tradicional">
        </div>

        <!-- Imagen y video -->
        <div class="grid md:grid-cols-2 gap-5">
          <!-- Imagen -->
          <div>
            <label for="imageRecipe" class="block text-base font-medium text-amber-700 mb-1">Imagen principal</label>
            <div
              class="relative border-2 border-dashed border-amber-300 rounded-lg p-4 text-center hover:border-amber-400 transition duration-300 bg-amber-50">
              <input type="file" id="imageRecipe" @change="handleImageChange"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-10 w-10 text-amber-500" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="mt-1 text-sm text-amber-600">
                {{ image && typeof image === 'object' ? image.name : 'Haz clic para cambiar la imagen' }}
              </p>
            </div>
          </div>

          <!-- Video -->
          <div>
            <label for="videoRecipe" class="block text-base font-medium text-amber-700 mb-1">Video (Opcional)</label>
            <div
              class="relative border-2 border-dashed border-amber-300 rounded-lg p-4 text-center hover:border-amber-400 transition duration-300 bg-amber-50">
              <input type="file" id="videoRecipe" @change="handleVideoChange"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-10 w-10 text-amber-500" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p class="mt-1 text-sm text-amber-600">
                {{ video && typeof video === 'object' ? video.name : 'Subir o cambiar video' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Descripción -->
        <div class="mt-5">
          <label for="descriptionRecipe" class="block text-base font-medium text-amber-700 mb-1">Descripción*</label>
          <textarea id="descriptionRecipe" rows="4" v-model="description" required
            class="w-full px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
            placeholder="Describe tu receta..."></textarea>
        </div>
      </div>

      <!-- Ingredientes -->
      <div class="p-6 sm:p-8 border-b border-amber-100">
        <h2 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes Receta
        </h2>

        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="grid md:grid-cols-3 gap-3 mb-3">
          <div>
            <label :for="'ingredient' + index" class="block text-sm font-medium text-amber-700 mb-1">Ingrediente {{
              index + 1 }}</label>
            <input :id="'ingredient' + index" v-model="recipebook.ingredients[index]" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Nombre del ingrediente">
          </div>
          <div>
            <label :for="'quantity' + index" class="block text-sm font-medium text-amber-700 mb-1">Cantidad</label>
            <input :id="'quantity' + index" v-model="recipebook.quantities[index]" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Cantidad necesaria">
          </div>
          <div class="flex items-end">
            <button @click="removeIngredient(index)" type="button" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>


        <button type="button" @click="addIngredient"
          class="mt-3 flex items-center text-sm text-amber-600 hover:text-amber-800 transition duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir ingrediente
        </button>
      </div>

      <!-- Pasos de preparación -->
      <div class="p-6 sm:p-8">
        <h2 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Pasos de Preparación Receta
        </h2>

        <div v-for="(step, index) in recipebook.steps" :key="index"
          class="mb-5 p-4 bg-amber-50 rounded-lg border border-amber-200 relative">
          <button @click="removeStep(index)" type="button"
            class="absolute top-2 right-2 text-red-500 hover:text-red-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
          <h3 class="text-base font-semibold text-amber-700 mb-2">Paso {{ index + 1 }}</h3>

          <div class="mb-3">
            <label :for="'stepTitle' + index" class="block text-sm font-medium text-amber-700 mb-1">Título del
              paso</label>
            <input :id="'stepTitle' + index" v-model="step.title" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Título breve">
          </div>

          <div class="mb-3">
            <label :for="'stepDesc' + index" class="block text-sm font-medium text-amber-700 mb-1">Descripción</label>
            <textarea :id="'stepDesc' + index" v-model="step.description" rows="2" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Describe este paso..."></textarea>
          </div>

          <div>
            <label :for="'stepImage' + index" class="block text-sm font-medium text-amber-700 mb-1">Imagen
              (Opcional)</label>
            <div class="relative">
              <input type="file" :id="'stepImage' + index" @change="handleStepImageChange($event, index)"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <div
                class="flex items-center justify-between px-3 py-1.5 bg-white rounded-lg border border-amber-300 shadow-sm">
                <span class="text-xs text-amber-600 truncate">
                  {{ step.image ? (typeof step.image === 'object' ? step.image.name : 'Imagen existente') : 'Seleccionar imagen...' }}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-500" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>



        <button type="button" @click="addStep"
          class="flex items-center text-sm text-amber-600 hover:text-amber-800 transition duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir paso
        </button>
      </div>

      <!-- SubIngredientes -->
      <div class="p-6 sm:p-8 border-b border-amber-100">
        <h2 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes SubReceta
        </h2>

        <div v-for="(ingredient, index) in recipebook.subingredients" :key="index"
          class="grid md:grid-cols-3 gap-3 mb-3">
          <div>
            <label :for="'subingredient' + index" class="block text-sm font-medium text-amber-700 mb-1">SubIngrediente
              {{ index + 1 }}</label>
            <input :id="'subingredient' + index" v-model="recipebook.subingredients[index]" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Nombre del ingrediente">
          </div>
          <div>
            <label :for="'subquantity' + index"
              class="block text-sm font-medium text-amber-700 mb-1">SubCantidad</label>
            <input :id="'subquantity' + index" v-model="recipebook.subquantities[index]" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Cantidad necesaria">
          </div>
          <div class="flex items-end">
            <button @click="removeSubIngredient(index)" type="button" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <button type="button" @click="addSubIngredient"
          class="mt-3 flex items-center text-sm text-amber-600 hover:text-amber-800 transition duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir ingrediente
        </button>
      </div>

      <!-- SubPasos de preparación -->
      <div class="p-6 sm:p-8">
        <h2 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Pasos de Preparación SubReceta
        </h2>

        <div v-for="(step, index) in recipebook.substeps" :key="index"
          class="mb-5 p-4 bg-amber-50 rounded-lg border border-amber-200 relative">
          <button @click="removeSubStep(index)" type="button"
            class="absolute top-2 right-2 text-red-500 hover:text-red-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
          <h3 class="text-base font-semibold text-amber-700 mb-2">Paso {{ index + 1 }}</h3>

          <div class="mb-3">
            <label :for="'stepTitle' + index" class="block text-sm font-medium text-amber-700 mb-1">Título del
              subpaso</label>
            <input :id="'stepTitle' + index" v-model="step.title" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Título breve">
          </div>

          <div class="mb-3">
            <label :for="'stepDesc' + index" class="block text-sm font-medium text-amber-700 mb-1">Descripción</label>
            <textarea :id="'stepDesc' + index" v-model="step.description" rows="2" required
              class="w-full px-3 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 shadow-sm"
              placeholder="Describe este paso..."></textarea>
          </div>

          <div>
            <label :for="'stepImage' + index" class="block text-sm font-medium text-amber-700 mb-1">Imagen
              (Opcional)</label>
            <div class="relative">
              <input type="file" :id="'stepImage' + index" @change="handleSubStepImageChange($event, index)"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <div
                class="flex items-center justify-between px-3 py-1.5 bg-white rounded-lg border border-amber-300 shadow-sm">
                <span class="text-xs text-amber-600 truncate">
                  {{ step.image ? (typeof step.image === 'object' ? step.image.name : 'Imagen existente') : 'Seleccionar imagen...' }}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-500" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>



        <button type="button" @click="addSubStep"
          class="flex items-center text-sm text-amber-600 hover:text-amber-800 transition duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir paso
        </button>
      </div>

      <!-- Filtros -->

      <!-- Sección de Filtros -->
      <div class="p-6 sm:p-8 border-b border-amber-100 bg-gradient-to-r from-amber-50 to-white">
        <h2 class="text-xl font-bold text-amber-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filtros de Receta
        </h2>

        <!-- Grid de filtros -->
        <div class="grid md:grid-cols-2 gap-5">
          <!-- Tipo de comida -->
          <div class="space-y-2">
            <label class="block text-base font-medium text-amber-700">Tipo de comida*</label>
            <div class="bg-white p-3 rounded-lg border border-amber-200 shadow-sm">
              <div class="space-y-2">
                <label v-for="(type, index) in foodTypes" :key="index" class="flex items-center">
                  <input type="radio" name="tipoComida" :value="type.value" v-model="tipoComida"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300">
                  <span class="ml-2 text-sm text-amber-800">{{ type.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Comunidad Autónoma -->
          <div class="space-y-2">
            <label class="block text-base font-medium text-amber-700">Comunidad Autónoma</label>
            <div class="bg-white p-3 rounded-lg border border-amber-200 shadow-sm max-h-48 overflow-y-auto">
              <div class="space-y-2">
                <label v-for="(region, index) in regions" :key="index" class="flex items-center">
                  <input type="radio" name="ccaa" :value="region.value" v-model="ccaa"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300">
                  <span class="ml-2 text-sm text-amber-800">{{ region.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Tipo de proteína -->
          <div class="space-y-2">
            <label class="block text-base font-medium text-amber-700">Tipo de proteína</label>
            <div class="bg-white p-3 rounded-lg border border-amber-200 shadow-sm">
              <div class="grid grid-cols-2 gap-2">
                <label v-for="(protein, index) in proteins" :key="index" class="flex items-center">
                  <input type="checkbox" :value="protein.value" v-model="proteinas"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300 rounded">
                  <span class="ml-2 text-sm text-amber-800">{{ protein.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Tiempo de preparación -->
          <div class="space-y-2">
            <label class="block text-base font-medium text-amber-700">Tiempo de preparación</label>
            <div class="bg-white p-3 rounded-lg border border-amber-200 shadow-sm">
              <div class="space-y-2">
                <label v-for="(time, index) in prepTimes" :key="index" class="flex items-center">
                  <input type="radio" name="tiempo" :value="time.value" v-model="tiempo"
                    class="h-4 w-4 text-amber-600 focus:ring-amber-500 border-amber-300">
                  <span class="ml-2 text-sm text-amber-800">{{ time.label }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Botón de enviar -->
      <div class="px-6 sm:px-8 pb-6 sm:pb-8">
        <button type="submit"
          class="w-full py-3 bg-gradient-to-r from-amber-600 to-red-600 hover:from-amber-700 hover:to-red-700 text-white font-semibold rounded-lg shadow-md transition duration-300 transform hover:scale-[1.01]">
          Guardar Cambios
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';

const route = useRoute();
const router = useRouter();
const recipeId = route.query.id;

const title = ref('');
const description = ref('');
const video = ref('');
const image = ref('');
const tipoComida = ref('')
const ccaa = ref('')
const tiempo = ref('')
const proteinas = ref([]);
const showBasicInfo = ref();
const userToken = localStorage.getItem('userToken');
const recipebook = reactive({
  ingredients: [],
  quantities: [],
  steps: [],
  subingredients: [],
  subquantities: [],
  substeps: []
});

// Función para añadir ingrediente
const addIngredient = () => {
  recipebook.ingredients.push('');
  recipebook.quantities.push('');
};

// Función para añadir paso
const addStep = () => {
  recipebook.steps.push({ title: '', description: '', image: null });
};

// Función para añadir ingrediente
const addSubIngredient = () => {
  recipebook.subingredients.push('');
  recipebook.subquantities.push('');
};

// Función para añadir paso
const addSubStep = () => {
  recipebook.substeps.push({ title: '', description: '', image: null });
};

onMounted(() => {
  axios.post('http://localhost:5000/viewRecipe', { idrecipe: recipeId, userToken: userToken})
    .then(response => {
      title.value = response.data.recipe_list[0].title;
      description.value = response.data.recipe_list[0].description;
      showBasicInfo.value = Boolean(response.data.recipe_list[0].visibility)
      image.value = response.data.recipe_list[0].image;
      video.value = response.data.recipe_list[0].video;

      response.data.ingredient_list.forEach(element => {
        recipebook.ingredients.push(element.ingredients);
        recipebook.quantities.push(element.quantity);
      });

      response.data.step_list.forEach(element => {
        recipebook.steps.push(element);
      });

      response.data.subingredient_list.forEach(element => {
        recipebook.subingredients.push(element.ingredients);
        recipebook.subquantities.push(element.quantity);
      });

      response.data.substep_list.forEach(element => {
        recipebook.substeps.push(element);
      });

      response.data.filters_list.forEach(element => {
        if (element.category === 'typeeat') {
          tipoComida.value = element.type;
        }
        if (element.category === 'ccaa') {
          ccaa.value = element.type;
        }
        if (element.category === 'time') {
          tiempo.value = element.type;
        }
        if (element.category === 'protein') {
          proteinas.value.push(element.type);
        }
      });
    })
    .catch(error => {
      console.error("Error en la solicitud:", error);
    });
});

function handleImageChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      image.value = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function handleVideoChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      video.value = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function handleStepImageChange(event, index) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      recipebook.steps[index].image = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function handleSubStepImageChange(event, index) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      recipebook.substeps[index].image = {
        base64: reader.result.split(",")[1],
        name: file.name
      };
    };
  }
}

function submitEditeRecipe() {
  const payload = {
    idrecipe: recipeId,
    title: title.value,
    image: typeof image.value === 'object' ? image.value : { base64: null, name: image.value },
    video: typeof video.value === 'object' ? video.value : { base64: null, name: video.value },
    description: description.value,
    ingredients: recipebook.ingredients.length > 0 ? recipebook.ingredients : [],
    quantities: recipebook.quantities.length > 0 ? recipebook.quantities : [],
    steps: recipebook.steps.length > 0 ? recipebook.steps.map(step => ({
      title: step.title,
      description: step.description,
      image: typeof step.image === 'object' ? step.image : { base64: null, name: step.image }
    })) : [],
    subingredients: recipebook.subingredients.length > 0 ? recipebook.subingredients : [],
    subquantities: recipebook.subquantities.length > 0 ? recipebook.subquantities : [],
    substeps: recipebook.substeps.length > 0 ? recipebook.substeps.map(step => ({
      title: step.title,
      description: step.description,
      image: typeof step.image === 'object' ? step.image : { base64: null, name: step.image }
    })) : [],
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: proteinas.value,
    visibility: showBasicInfo.value ? 1 : 0,
    token: localStorage.getItem("userToken")
  };

  axios.post('http://localhost:5000/editeRecipe', payload)
    .then(response => {
      console.log(response.data.message);
      router.push({ name: 'home' });
    })
    .catch(error => {
      console.error(error);
    });
}

const foodTypes = [
  { value: 'starters', label: 'Entrantes' },
  { value: 'maindishes', label: 'Platos principales' },
  { value: 'accompaniments', label: 'Acompañamientos' },
  { value: 'dessert', label: 'Postres' },
  { value: 'soups', label: 'Sopas' },
  { value: 'salads', label: 'Ensaladas' },
  { value: 'sauces', label: 'Salsas' },
  { value: 'breads', label: 'Panes y masas' }
];

const regions = [
  { value: 'andalucia', label: 'Andalucía' },
  { value: 'aragon', label: 'Aragón' },
  { value: 'asturias', label: 'Asturias' },
  { value: 'cantabria', label: 'Cantabria' },
  { value: 'castillalamancha', label: 'Castilla-La Mancha' },
  { value: 'castillaleon', label: 'Castilla y León' },
  { value: 'catalunya', label: 'Cataluña' },
  { value: 'valencia', label: 'Com. Valenciana' },
  { value: 'extremadura', label: 'Extremadura' },
  { value: 'galicia', label: 'Galicia' },
  { value: 'baleares', label: 'Baleares' },
  { value: 'canarias', label: 'Canarias' },
  { value: 'larioja', label: 'La Rioja' },
  { value: 'madrid', label: 'Madrid' },
  { value: 'murcia', label: 'Murcia' },
  { value: 'navarra', label: 'Navarra' },
  { value: 'paisvasco', label: 'País Vasco' }
];

const proteins = [
  { value: 'pollo', label: 'Pollo' },
  { value: 'res', label: 'Res / Ternera' },
  { value: 'cerdo', label: 'Cerdo / Ibérico' },
  { value: 'cordero', label: 'Cordero' },
  { value: 'conejo', label: 'Conejo' },
  { value: 'pato', label: 'Pato' },
  { value: 'pescado', label: 'Pescado blanco' },
  { value: 'atun', label: 'Atún' },
  { value: 'bacalao', label: 'Bacalao' },
  { value: 'salmon', label: 'Salmón' },
  { value: 'anguila', label: 'Anguila' },
  { value: 'mariscos', label: 'Mariscos' },
  { value: 'pulpo', label: 'Pulpo' },
  { value: 'calamar', label: 'Calamar / Sepia' },
  { value: 'huevo', label: 'Huevo' },
  { value: 'queso', label: 'Queso' },
  { value: 'legumbres', label: 'Legumbres (lentejas, garbanzos)' },
  { value: 'setas', label: 'Setas / Champiñones' },
  { value: 'vegetariana', label: 'Vegetariana' },
  { value: 'vegana', label: 'Vegana' },
];

const prepTimes = [
  { value: 'menos15', label: 'Rápida (<15 min)' },
  { value: '15a30', label: 'Media (15-30 min)' },
  { value: '30a60', label: 'Lenta (30-60 min)' },
  { value: 'mas60', label: 'Muy lenta (>1 hora)' }
];

// Función para eliminar ingrediente
const removeIngredient = (index) => {
  recipebook.ingredients.splice(index, 1);
  recipebook.quantities.splice(index, 1);
};

// Función para eliminar subingrediente
const removeSubIngredient = (index) => {
  recipebook.subingredients.splice(index, 1);
  recipebook.subquantities.splice(index, 1);
};

// Función para eliminar paso
const removeStep = (index) => {
  recipebook.steps.splice(index, 1);
};

// Función para eliminar subpaso
const removeSubStep = (index) => {
  recipebook.substeps.splice(index, 1);
};
</script>

<style scoped>
/* Animación para las secciones del formulario */
.form-section {
  transition: all 0.3s ease;
}

.form-section:hover {
  background-color: rgba(254, 243, 199, 0.3);
}

/* Efecto para los botones de añadir */
.add-button {
  transition: all 0.2s ease;
}

.add-button:hover {
  transform: translateY(-1px);
}
</style>