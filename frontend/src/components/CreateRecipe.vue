<template>
  <div class="min-h-screen bg-amber-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8 ">
    <!-- Encabezado con efecto de receta -->
    <div class="max-w-4xl mx-auto text-center mb-12">
      <h1 class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-red-600 font-serif mb-4">
        Crear Nueva Receta
      </h1>
      <p class="text-lg text-amber-700 dark:text-amber-300">Comparte tu creación culinaria con la comunidad</p>
    </div>

    <!-- Formulario -->
    <form @submit.prevent="submitRecipe"
      class="max-w-4xl mx-auto bg-white/80 dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden border border-amber-200 dark:border-gray-700">
      <!-- Sección de información básica -->
      <div class="p-8 border-b border-amber-100 dark:border-gray-700 bg-gradient-to-r from-amber-50 dark:from-gray-700 to-white dark:to-gray-800">
        <h2 class="text-2xl font-bold text-amber-800 dark:text-amber-200 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Información Básica
        </h2>

        <!--Ocultar o Mostrar-->
        <label for="descriptionRecipe" class="block text-base font-medium text-amber-700 dark:text-amber-300 mb-1">Mostrar / Ocultar Receta</label>
        <button @click.prevent="showBasicInfo = !showBasicInfo" class="text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="showBasicInfo" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </button>

        <!-- Título de la receta -->
        <div class="mb-6">
          <label for="titleRecipe" class="block text-lg font-medium text-amber-700 dark:text-amber-300 mb-2">Nombre de la receta*</label>
          <input type="text" id="titleRecipe" v-model="title" required
            class="w-full px-4 py-3 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-700 dark:text-white"
            placeholder="Ej: Paella Valenciana">
        </div>

        <!-- Imagen y video -->
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Imagen de la receta -->
          <div>
            <label for="imageRecipe" class="block text-lg font-medium text-amber-700 dark:text-amber-300 mb-2">Imagen principal*</label>
            <div
              class="relative border-2 border-dashed border-amber-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-amber-400 dark:hover:border-amber-500 bg-amber-50 dark:bg-gray-700">
              <input type="file" id="imageRecipe" @change="handleImageChange" required
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-amber-500 dark:text-amber-400" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="mt-2 text-sm text-amber-600 dark:text-amber-400">
                <span class="font-medium">Haz clic para subir</span> o arrastra una imagen
              </p>
              <p v-if="image" class="mt-1 text-xs text-amber-500 dark:text-amber-400">{{ image.name }}</p>
            </div>
          </div>

          <!-- Video de la receta (opcional) -->
          <div>
            <label for="videoRecipe" class="block text-lg font-medium text-amber-700 dark:text-amber-300 mb-2">Video (Opcional)</label>
            <div
            class="relative border-2 border-dashed border-amber-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-amber-400 dark:hover:border-amber-500  bg-amber-50 dark:bg-gray-700">
            <input type="file" id="videoRecipe" @change="handleVideoChange"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-amber-500 dark:text-amber-400" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                  d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p class="mt-2 text-sm text-amber-600 dark:text-amber-400">
                <span class="font-medium">Haz clic para subir</span> un video tutorial
              </p>
              <p v-if="video" class="mt-1 text-xs text-amber-500 dark:text-amber-400">{{ video.name }}</p>
            </div>
          </div>
        </div>

        <!-- Descripción de la receta -->
        <div class="mt-6">
          <label for="descriptionRecipe" class="block text-lg font-medium text-amber-700 dark:text-amber-300 mb-2">Descripción*</label>
          <textarea id="descriptionRecipe" rows="4" v-model="description" required
            class="w-full px-4 py-3 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-700 dark:text-white"
            placeholder="Describe tu receta, su origen, características especiales..."></textarea>
        </div>
              <!-- Sección de ingredientes -->
      <div class="p-8 border-b border-amber-100 dark:border-gray-700">
        <h2 class="text-2xl font-bold text-amber-800 dark:text-amber-200 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes Receta
        </h2>

        <div v-for="(ingredient, index) in recipebook.ingredients" :key="index" class="grid md:grid-cols-12 gap-4 mb-4">
          <div class="md:col-span-5">
            <label :for="'ingredient' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Ingrediente {{ index + 1 }}</label>
            <div class="flex">
              <input :id="'ingredient' + index" v-model="recipebook.ingredients[index]" required
                class="w-full px-4 py-2 rounded-l-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-700 dark:text-white"
                placeholder="Ej: Arroz bomba">
              <button @click.prevent="removeIngredient(index)"
                class="px-3 bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300 rounded-r-lg border border-l-0 border-amber-300 dark:border-gray-600 hover:bg-red-200 dark:hover:bg-red-800  ">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <div class="md:col-span-5">
            <label :for="'quantity' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Cantidad</label>
            <input :id="'quantity' + index" v-model="recipebook.quantities[index]" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-700 dark:text-white"
              placeholder="Ej: 300 gramos">
          </div>
          <div class="md:col-span-2 flex items-end">
            <!-- Espacio para alinear correctamente -->
          </div>
        </div>

        <button type="button" @click.prevent="moreIngredients"
          class="mt-4 flex items-center text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 ">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir otro ingrediente
        </button>
      </div>

      <!-- Sección de pasos -->
      <div class="p-8 border-b border-amber-100 dark:border-gray-700">
        <h2 class="text-2xl font-bold text-amber-800 dark:text-amber-200 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Pasos de Preparación Receta
        </h2>

        <div v-for="(step, index) in recipebook.steps" :key="index"
          class="mb-8 p-6 bg-amber-50 dark:bg-gray-700 rounded-lg border border-amber-200 dark:border-gray-600 relative">
          <button @click.prevent="removeStep(index)"
            class="absolute top-2 right-2 p-1 text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <h3 class="text-lg font-semibold text-amber-700 dark:text-amber-300 mb-3">Paso {{ index + 1 }}</h3>

          <div class="mb-4">
            <label :for="'stepTitle' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Título del paso</label>
            <input :id="'stepTitle' + index" v-model="step.title" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-800 dark:text-white"
              placeholder="Ej: Preparar el sofrito">
          </div>

          <div class="mb-4">
            <label :for="'stepDesc' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Descripción detallada</label>
            <textarea :id="'stepDesc' + index" v-model="step.text" rows="3" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-800 dark:text-white"
              placeholder="Describe este paso con detalle..."></textarea>
          </div>

          <div>
            <label :for="'stepImage' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Imagen (Opcional)</label>
            <div class="relative">
              <input type="file" :id="'stepImage' + index" @change="handleStepImageChange($event, index)"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <div
                class="flex items-center justify-between px-4 py-2 bg-white/80 dark:bg-gray-800 rounded-lg border border-amber-300 dark:border-gray-600 shadow-sm">
                <span class="text-sm text-amber-600 dark:text-amber-400 truncate">
                  {{ step.image ? step.image.name : 'Seleccionar imagen...' }}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500 dark:text-amber-400" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <button type="button" @click.prevent="moreSteps"
          class="flex items-center text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 ">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir otro paso
        </button>
      </div>

      <!-- Sección de Subingredientes -->
      <div class="p-8 border-b border-amber-100 dark:border-gray-700">
        <h2 class="text-2xl font-bold text-amber-800 dark:text-amber-200 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Ingredientes SubReceta
        </h2>

        <div v-for="(ingredient, index) in recipebook.subingredients" :key="index" class="grid md:grid-cols-12 gap-4 mb-4">
          <div class="md:col-span-5">
            <label :for="'subingredient' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">SubIngrediente {{ index + 1 }}</label>
            <div class="flex">
              <input :id="'subingredient' + index" v-model="recipebook.subingredients[index]" required
                class="w-full px-4 py-2 rounded-l-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-700 dark:text-white"
                placeholder="Ej: Arroz bomba">
              <button @click.prevent="removeSubIngredient(index)"
                class="px-3 bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300 rounded-r-lg border border-l-0 border-amber-300 dark:border-gray-600 hover:bg-red-200 dark:hover:bg-red-800 ">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <div class="md:col-span-5">
            <label :for="'subquantity' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">SubCantidad</label>
            <input :id="'subquantity' + index" v-model="recipebook.subquantities[index]" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-700 dark:text-white"
              placeholder="Ej: 300 gramos">
          </div>
          <div class="md:col-span-2 flex items-end">
            <!-- Espacio para alinear correctamente -->
          </div>
        </div>

        <button type="button" @click.prevent="moreSubIngredients"
          class="mt-4 flex items-center text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 ">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir otro ingrediente
        </button>
      </div>

      <!-- Sección de subpasos -->
      <div class="p-8 border-b border-amber-100 dark:border-gray-700">
        <h2 class="text-2xl font-bold text-amber-800 dark:text-amber-200 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Pasos de Preparación SubReceta
        </h2>

        <div v-for="(step, index) in recipebook.substeps" :key="index"
          class="mb-8 p-6 bg-amber-50 dark:bg-gray-700 rounded-lg border border-amber-200 dark:border-gray-600 relative">
          <button @click.prevent="removesubStep(index)"
            class="absolute top-2 right-2 p-1 text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <h3 class="text-lg font-semibold text-amber-700 dark:text-amber-300 mb-3">SubPaso {{ index + 1 }}</h3>

          <div class="mb-4">
            <label :for="'substepTitle' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Título del subpaso</label>
            <input :id="'substepTitle' + index" v-model="step.title" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-800 dark:text-white"
              placeholder="Ej: Preparar el sofrito">
          </div>

          <div class="mb-4">
            <label :for="'substepDesc' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Descripción detallada</label>
            <textarea :id="'substepDesc' + index" v-model="step.text" rows="3" required
              class="w-full px-4 py-2 rounded-lg border border-amber-300 dark:border-gray-600 focus:ring-2 focus:ring-amber-500 focus:border-amber-500 placeholder-amber-400 dark:placeholder-gray-500 shadow-sm dark:bg-gray-800 dark:text-white"
              placeholder="Describe este paso con detalle..."></textarea>
          </div>

          <div>
            <label :for="'substepImage' + index" class="block text-sm font-medium text-amber-700 dark:text-amber-300 mb-1">Imagen (Opcional)</label>
            <div class="relative">
              <input type="file" :id="'substepImage' + index" @change="handleSubStepImageChange($event, index)"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
              <div
                class="flex items-center justify-between px-4 py-2 bg-white/80 dark:bg-gray-800 rounded-lg border border-amber-300 dark:border-gray-600 shadow-sm">
                <span class="text-sm text-amber-600 dark:text-amber-400 truncate">
                  {{ step.image ? step.image.name : 'Seleccionar imagen...' }}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500 dark:text-amber-400" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <button type="button" @click.prevent="moreSubSteps"
          class="flex items-center text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 ">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Añadir otro paso
        </button>
      </div>

      <!-- Sección de Filtros - Diseño Alternativo -->
      <div class="p-8 border-b border-amber-100 dark:border-gray-700 bg-gradient-to-br from-amber-50 dark:from-gray-700 to-amber-100 dark:to-gray-800">
        <h2 class="text-2xl font-bold text-amber-800 dark:text-amber-200 mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filtros de Receta
        </h2>

        <!-- Filtros en acordeón -->
        <div class="space-y-4 " >
          <!-- Tipo de comida -->
          <div class="bg-white/80 dark:bg-gray-700 rounded-xl shadow-sm border border-amber-200 dark:border-gray-600 overflow-hidden">
            <button type="button" @click="toggleAccordion('foodType')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700 dark:text-amber-300">Tipo de comida</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 dark:text-amber-400 transform "
                :class="{ 'rotate-180': activeAccordion === 'foodType' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'foodType' }">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label v-for="(type, index) in foodTypes" :key="index"
                  class="flex items-center p-2 rounded-lg hover:bg-amber-50 dark:hover:bg-gray-600 cursor-pointer">
                  <input type="radio" name="tipoComida" :value="type.value" v-model="tipoComida"
                    class="h-4 w-4 text-amber-600 dark:text-amber-400 focus:ring-amber-500 border-amber-300 dark:border-gray-500">
                  <span class="ml-3 text-sm text-amber-800 dark:text-amber-300">{{ type.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Comunidad Autónoma -->
          <div class="bg-white/80 dark:bg-gray-700 rounded-xl shadow-sm border border-amber-200 dark:border-gray-600 overflow-hidden">
            <button type="button" @click="toggleAccordion('region')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700 dark:text-amber-300">Comunidad Autónoma</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 dark:text-amber-400 transform "
                :class="{ 'rotate-180': activeAccordion === 'region' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'region' }">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label v-for="(region, index) in regions" :key="index"
                  class="flex items-center p-2 rounded-lg hover:bg-amber-50 dark:hover:bg-gray-600 cursor-pointer">
                  <input type="radio" name="ccaa" :value="region.value" v-model="ccaa"
                    class="h-4 w-4 text-amber-600 dark:text-amber-400 focus:ring-amber-500 border-amber-300 dark:border-gray-500">
                  <span class="ml-3 text-sm text-amber-800 dark:text-amber-300">{{ region.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Tipo de proteína -->
          <div class="bg-white/80 dark:bg-gray-700 rounded-xl shadow-sm border border-amber-200 dark:border-gray-600 overflow-hidden">
            <button type="button" @click="toggleAccordion('protein')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700 dark:text-amber-300">Tipo de proteína</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 dark:text-amber-400 transform "
                :class="{ 'rotate-180': activeAccordion === 'protein' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'protein' }">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label v-for="(protein, index) in proteins" :key="index"
                  class="flex items-center p-2 rounded-lg hover:bg-amber-50 dark:hover:bg-gray-600 cursor-pointer">
                  <input type="checkbox" :value="protein.value" v-model="proteinas"
                    class="h-4 w-4 text-amber-600 dark:text-amber-400 focus:ring-amber-500 border-amber-300 dark:border-gray-500 rounded">
                  <span class="ml-3 text-sm text-amber-800 dark:text-amber-300">{{ protein.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Tiempo de preparación -->
          <div class="bg-white/80 dark:bg-gray-700 rounded-xl shadow-sm border border-amber-200 dark:border-gray-600 overflow-hidden">
            <button type="button" @click="toggleAccordion('time')"
              class="w-full px-6 py-4 flex justify-between items-center text-left">
              <span class="font-medium text-amber-700 dark:text-amber-300">Tiempo de preparación</span>
              <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-amber-500 dark:text-amber-400 transform "
                :class="{ 'rotate-180': activeAccordion === 'time' }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <div class="px-6 pb-4" :class="{ 'hidden': activeAccordion !== 'time' }">
              <div class="grid grid-cols-2 gap-4">
                <label v-for="(time, index) in prepTimes" :key="index"
                  class="flex items-center p-3 bg-amber-50 dark:bg-gray-600 rounded-lg border border-amber-200 dark:border-gray-500 cursor-pointer">
                  <input type="radio" name="tiempo" :value="time.value" v-model="tiempo"
                    class="h-4 w-4 text-amber-600 dark:text-amber-400 focus:ring-amber-500 border-amber-300 dark:border-gray-500">
                  <div class="ml-3">
                    <span class="block text-sm font-medium text-amber-800 dark:text-amber-300">{{ time.label }}</span>
                    <span class="block text-xs text-amber-600 dark:text-amber-400">{{ time.description }}</span>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>




      <!-- Botón de enviar -->
      <div class="px-8 pb-8">
        <button type="submit"
          class="w-full py-4 bg-gradient-to-r from-amber-600 to-red-600 hover:from-amber-700 hover:to-red-700 text-white font-bold rounded-lg shadow-lg  transform hover:scale-[1.02] flex items-center justify-center">
          Publicar Receta
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from "vue-router";

const title = ref('');
const image = ref('');
const video = ref('');
const description = ref('');
const recipebook = reactive({
  ingredients: [],
  quantities: [],
  steps: [],
  subingredients: [],
  subquantities:[],
  substeps:[]
});
const router = useRouter();
const userToken = ref(localStorage.getItem("userToken"));
const tipoComida = ref('')
const ccaa = ref('')
const tiempo = ref('')
const proteinas = ref([]);
const showBasicInfo = ref(true);
const activeAccordion = ref(null);
const darkMode = ref(false);


if (userToken.value == null) {
  router.push({ name: "login" });
}

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
}

function handleVideoChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      video.value = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }
}

function moreIngredients() {
  recipebook.ingredients.push('');
  recipebook.quantities.push('');
}

function moreSubIngredients() {
  recipebook.subingredients.push('');
  recipebook.subquantities.push('');
}

function moreSteps() {
  recipebook.steps.push({ title: '', text: '', image: null });
}

function moreSubSteps() {
  recipebook.substeps.push({ title: '', text: '', image: null });
}

function handleStepImageChange(event, index) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      recipebook.steps[index].image = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }
}

function handleSubStepImageChange(event, index) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      recipebook.substeps[index].image = {
        name: file.name,
        base64: reader.result
      };
    };
    reader.readAsDataURL(file);
  }
}


function submitRecipe() {
  const payload = {
    title: title.value,
    image: image.value,
    video: video.value,
    description: description.value,
    ingredients: recipebook.ingredients.length > 0 ? recipebook.ingredients : [],
    quantities: recipebook.quantities.length > 0 ? recipebook.quantities : [],
    steps: recipebook.steps.length > 0 ? recipebook.steps.map(step => ({
      title: step.title,
      text: step.text,
      image: step.image
    })) : [],
    subingredients: recipebook.subingredients.length > 0 ? recipebook.subingredients : [],
    subquantities: recipebook.subquantities.length > 0 ? recipebook.subquantities : [],
    substeps: recipebook.substeps.length > 0 ? recipebook.substeps.map(step => ({
      title: step.title,
      text: step.text,
      image: step.image
    })) : [],
    token: localStorage.getItem("userToken"),
    typeeat: tipoComida.value,
    ccaa: ccaa.value,
    time: tiempo.value,
    proteins: proteinas.value,
    visibility: showBasicInfo.value
  };
  axios.post(`${process.env.VUE_APP_API_URL}/create`, payload)
    .then(() => {
      router.push({ name: "home" });
    })
    .catch(error => {
      console.log(error);
    });
}

const toggleAccordion = (section) => {
  activeAccordion.value = activeAccordion.value === section ? null : section;
};

// Datos para los filtros
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
  { value: "<15'⏱️", label: 'Rápida', description: '<15 minutos' },
  { value: '15-30 ⏱️', label: 'Media', description: '15-30 minutos' },
  { value: "30'-60' ⏱️", label: 'Lenta', description: '30-60 minutos' },
  { value: ">60' ⏱️", label: 'Muy lenta', description: '>1 hora' }
];

// Función para eliminar ingrediente
function removeIngredient(index) {

    recipebook.ingredients.splice(index, 1);
    recipebook.quantities.splice(index, 1);

}

// Función para eliminar subingrediente
function removeSubIngredient(index) {

recipebook.subingredients.splice(index, 1);
recipebook.subquantities.splice(index, 1);

}

// Función para eliminar paso
function removeStep(index) {

    recipebook.steps.splice(index, 1);

}

// Función para eliminar subpaso
function removesubStep(index) {

recipebook.substeps.splice(index, 1);

}

onMounted(() => {
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode !== null) {
        darkMode.value = JSON.parse(savedMode);
        applyDarkMode();
    }

});

function applyDarkMode() {
    if (darkMode.value) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

</script>

<style scoped>
/* Efectos adicionales */
form:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Animación para los pasos */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-enter-active {
  animation: fadeIn 0.5s ease-out;
}
</style>
