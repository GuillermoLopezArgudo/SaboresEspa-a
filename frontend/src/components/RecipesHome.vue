<template>
    <div class="max-w-xs mx-auto my-4 p-4 bg-white rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:translate-y-2">
        <img :src="`http://localhost:5000/${item.image}`" class="w-full h-48 object-cover rounded-t-lg" alt="recipe image" v-if="item.image" />
        <div class="p-4">
            <h5 class="text-lg font-semibold">{{ item.title }}</h5>
            <p class="text-sm text-gray-600 truncate" :title="item.description">{{ item.description }}</p>
            <button @click="OnClickRecipe" class="mt-4 w-full py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                Ver Receta
            </button>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
    item: {
        type: Object,   
        required: true
    }
});

const router = useRouter();

//Funcion que navega a la receta pulsada segun id
function OnClickRecipe(){
    router.push({ name: "recipe", query: { id: props.item.id } });
}
</script>

<style scoped>
</style>
