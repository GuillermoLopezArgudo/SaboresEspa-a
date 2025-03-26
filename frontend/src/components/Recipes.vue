<template>
    <div class="card" style="width: 18rem;">
        <img :src="'data:image/jpeg;base64,' + item.img" class="card-img-top" alt="recipe image" v-if="item.img" />
        <div class="card-body">
            <h5 class="card-title">{{ item.titulo }}</h5>
            <p class="card-text">{{ item.descripcion }}</p>
            <button @click="OnClickRecipe">Ver Receta</button>
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
})
const router = useRouter();

function OnClickRecipe(){
    router.push({ name: "recipe",query: { id: props.item.id} });
}
</script>

<style scoped>
.card {
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
