<template>
    <div class="card" style="width: 18rem;">
        <img :src="`http://localhost:5000/${item.img}`" class="card-img-top" alt="recipe image" v-if="item.img" />
        <div class="card-body">
            <h5 class="card-title">{{ item.titulo }}</h5>
            <p class="card-text text-truncate" :title="item.descripcion">{{ item.descripcion }}</p>
            <button @click="OnClickRecipe" class="btn btn-primary w-100">Ver Receta</button>
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
.card {
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
}

.card-text {
    font-size: 0.9rem;
    color: #6c757d;
}

.card-body {
    padding: 1rem;
}

button {
    border-radius: 5px;
    font-size: 1rem;
}
</style>
