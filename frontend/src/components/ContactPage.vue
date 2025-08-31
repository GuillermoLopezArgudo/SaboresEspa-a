<template>
  <div class="min-h-screen bg-amber-100 dark:bg-neutral-900 text-gray-900 dark:text-neutral-200 flex items-center justify-center px-4 ">
    <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-lg dark:shadow-md p-8 max-w-2xl w-full ">
      <h1 class="text-4xl font-bold text-amber-600 dark:text-amber-400 mb-6 text-center">Contáctanos</h1>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="name" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Nombre</label>
          <input v-model="form.name" type="text" id="name"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/80 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-amber-400 focus:outline-none" required />
        </div>
        <div>
          <label for="email" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Correo Electrónico</label>
          <input v-model="form.email" type="email" id="email"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/80 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-amber-400 focus:outline-none" required />
        </div>
        <div>
          <label for="message" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Mensaje</label>
          <textarea v-model="form.message" id="message" rows="4"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/80 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-amber-400 focus:outline-none"
            required></textarea>
        </div>
        <button type="submit"
          class="w-full py-2 px-4 bg-amber-500 hover:bg-amber-600 text-white font-semibold rounded-lg ">
          Enviar mensaje
        </button>
      </form>
      <p v-if="submitted" class="mt-4 text-green-600 dark:text-green-400 text-center font-medium">
        ¡Gracias por contactarnos! Te responderemos pronto.
      </p>
    </div>
  </div>
</template>


<script setup>
import { reactive, ref, onMounted } from 'vue'
import axios from 'axios';

const darkMode = ref(false);
const form = reactive({
  name: '',
  email: '',
  message: ''
})

const submitted = ref(false)

const handleSubmit = async () => {
  try {
    await axios.post(`${process.env.VUE_APP_API_URL}/send-email`, form)
    submitted.value = true
    form.name = ''
    form.email = ''
    form.message = ''
  } catch (error) {
    console.error("Error al enviar el correo:", error)
  }
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