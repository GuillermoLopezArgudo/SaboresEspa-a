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
  //Modifica el estado de las estrellas cuando se pulsa en ellas
  const setRating = (star) => {
    props.onRatingChanged(star);
  };
  </script>
  
  <style scoped>
  .star-rating {
    font-size: 1.5rem;
    color: #ffc107;
  }
  
  .star-rating .fa {
    cursor: pointer;
  }
  </style>
  