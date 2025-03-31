<template>
  <div class="star-rating">
    <i
      v-for="star in 5"
      :key="star"
      class="fa"
      :class="{
        'fa-star': star <= rating,
        'fa-star-o': star > rating
      }"
      @click="setRating(star)"
    ></i>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  rating: {
    type: Number,
    required: true
  },
  onRatingChanged: {
    type: Function,
    required: true
  }
});



// Función para cambiar la calificación
const setRating = (star) => {
  // Actualiza la calificación solo si el usuario está autenticado
  const userToken = localStorage.getItem('userToken');
  if (userToken) {
    // Llamamos a la función que viene como prop para que se propague el cambio
    props.onRatingChanged(star);
  } else {
    // Redirige al login si no está autenticado
    const router = useRouter();
    router.push({ name: "login" });
  }
};
</script>

<style scoped>
.star-rating {
  font-size: 1.5rem;
  color: #ffd700; /* Color dorado para las estrellas */
}
.star-rating .fa {
  cursor: pointer;
  margin-right: 5px;
}
</style>
