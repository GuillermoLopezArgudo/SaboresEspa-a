<template>
  <div class="star-rating flex items-center">
    <div class="flex">
      <button
        v-for="star in 5"
        :key="star"
        class="focus:outline-none transition-all duration-200 transform hover:scale-125"
        @click="setRating(star)"
        @mouseover="hoverRating = star"
        @mouseleave="hoverRating = 0"
        :aria-label="`Calificar con ${star} ${star === 1 ? 'estrella' : 'estrellas'}`"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-8 w-8"
          :class="{
            'text-yellow-500 fill-current': star <= effectiveRating,
            'text-gray-300 fill-current': star > effectiveRating
          }"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
          />
        </svg>
      </button>
    </div>
    
    <!-- Mostrar calificación o el mensaje para calificar -->
    <span v-if="effectiveRating > 0" class="ml-2 text-sm text-gray-600">
      {{ effectiveRating }} de 5
    </span>
    <span v-else class="ml-2 text-sm text-gray-600">
      ¡Sé el primero en calificar!
    </span>
  </div>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  rating: {
    type: Number,
    required: true,
    validator: value => value >= 0 && value <= 5
  },
  onRatingChanged: {
    type: Function,
    required: true
  },
  showRatingText: {
    type: Boolean,
    default: true
  },
  interactive: {
    type: Boolean,
    default: true
  }
});

const hoverRating = ref(0);
const router = useRouter();

const effectiveRating = computed(() => {
  return hoverRating.value || props.rating;
});

const setRating = (star) => {
  if (!props.interactive) return;
  
  const userToken = localStorage.getItem('userToken');
  if (userToken) {
    props.onRatingChanged(star);
  } else {
    router.push({ name: "login" });
  }
};
</script>

<style scoped>
.star-rating {
  min-height: 2rem;
}

button {
  transition: all 0.2s ease-in-out;
}

.star-rating.non-interactive {
  pointer-events: none;
}
</style>
