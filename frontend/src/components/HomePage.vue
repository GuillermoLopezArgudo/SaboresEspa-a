<template>
    <h1>WELCOME HOME</h1>
    <nav class="navbar bg-body-tertiary">
        <div class="container">
            <router-link to="/create" class="navbar-brand">Crear</router-link>
            <router-link to="/recipes" class="navbar-brand">Recetas</router-link>
            <router-link to="/register" class="navbar-brand">Ajustes</router-link>
        </div>
    </nav>
    <div>
        <FavoriteRecipe></FavoriteRecipe>
    </div>
</template>

<script setup>
import FavoriteRecipe from './FavoriteRecipe.vue';
</script>

<style></style>