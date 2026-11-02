<template>
  <div class="recipe-image relative overflow-hidden bg-amber-100" :class="wrapClass">
    <img
      v-if="src"
      :src="src"
      :srcset="srcset || undefined"
      :sizes="sizes || undefined"
      :alt="alt"
      :loading="loading"
      decoding="async"
      class="w-full h-full object-cover"
      :class="imgClass"
      @error="onError"
    />
    <div
      v-else
      class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-amber-100 to-amber-200 text-amber-700/70"
    >
      <span class="font-serif text-lg">{{ placeholder }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { mediaUrl } from '../api'
import { responsiveSrc } from '../utils/imageCompress'

const props = defineProps({
  path: { type: String, default: '' },
  alt: { type: String, default: '' },
  placeholder: { type: String, default: 'Sin imagen' },
  wrapClass: { type: String, default: '' },
  imgClass: { type: String, default: '' },
  loading: { type: String, default: 'lazy' },
})

const broken = ref(false)

const resolved = computed(() => {
  if (broken.value || !props.path) return { src: '', srcset: '', sizes: '' }
  return responsiveSrc(mediaUrl(props.path))
})

const src = computed(() => resolved.value.src)
const srcset = computed(() => resolved.value.srcset)
const sizes = computed(() => resolved.value.sizes)

watch(
  () => props.path,
  () => {
    broken.value = false
  }
)

function onError() {
  broken.value = true
}
</script>
