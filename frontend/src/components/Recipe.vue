<template>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Receta</h1>

        <div v-if="userToken">
            <router-link to="/home" class="btn btn-secondary mb-3">Atrás</router-link>
        </div>
        <div v-else>
            <router-link to="/" class="btn btn-secondary mb-3">Atrás</router-link>
        </div>

        <div v-if="receta">
            <h2 class="text-primary">{{ receta.titulo }}</h2>

            <button @click="toggleFavorite" :class="['heart-button', { 'active': isFavorite }]"
                class="btn btn-outline-danger mb-3">
                <i class="fa" :class="isFavorite ? 'fa-heart' : 'fa-heart-o'"></i> Favoritos
            </button>

            <p class="lead">{{ receta.descripcion }}</p>

            <div v-if="receta.img" class="mb-4">
                <img :src="'data:image/jpeg;base64,' + receta.img" alt="Imagen de la receta"
                    class="img-fluid rounded shadow" />
            </div>

            <h3 class="text-secondary">Ingredientes:</h3>
            <ul class="list-group list-group-flush mb-4">
                <li v-for="(ingrediente, idx) in receta.ingredientes" :key="idx" class="list-group-item">
                    {{ ingrediente }} - {{ receta.cantidades[idx] || 'Cantidad no disponible' }}
                </li>
            </ul>

            <div v-if="receta.video" class="my-4">
                <video controls :src="'data:video/mp4;base64,' + receta.video" class="w-100 rounded shadow"></video>
            </div>

            <div v-if="receta.valoraciones" class="my-3">
                <p><strong>Valoración:</strong> {{ receta.valoraciones }} estrellas</p>
            </div>

            <div v-if="receta.comentarios != null" class="my-4">
                <h4>Comentarios:</h4>
                <ul class="list-group">
                    <li v-for="comentario in comments" :key="comentario.idcomment" class="list-group-item">
                        <strong>Comentario:</strong> {{ comentario.comment }} <br>
                        <small>Usuario: {{ comentario.username }}</small>
                        <div v-if="iduser == comentario.iduser">
                            <button class="btn btn-sm btn-warning me-2">Editar</button>
                            <button @click="deleteComment(comentario.idcomment)"
                                class="btn btn-sm btn-danger">Eliminar</button>
                        </div>
                    </li>
                </ul>
                <div class="mt-3">
                    <input type="text" placeholder="Escribe tu comentario..." v-model="comment"
                        class="form-control mb-2" />
                    <button @click.prevent="createComment" class="btn btn-primary w-100">Enviar Comentario</button>
                </div>
            </div>

            <div v-if="iduser == receta.idUser" class="mt-4">
                <button @click="deleteRecipe" class="btn btn-danger w-100 mb-2">Eliminar Receta</button>
                <button @click="editeRecipe" class="btn btn-warning w-100">Editar Receta</button>
            </div>
        </div>

        <p v-else class="text-center text-muted">Cargando receta...</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import 'font-awesome/css/font-awesome.min.css';

const route = useRoute();
const router = useRouter();
const recipeId = route.query.id;
const receta = ref(null);
const comment = ref("");
const userToken = localStorage.getItem('userToken');
const iduser = localStorage.getItem('iduser');
const comments = ref([]);
const isFavorite = ref(false);

const toggleFavorite = () => {
    isFavorite.value = !isFavorite.value;
    if (isFavorite.value) {
        axios
            .post('http://localhost:5000/updateFavs', payload)
            .then(response => {
                console.log(response.data.message)
                localStorage.setItem('idFavs',response.data.idFavs)
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
            });
    }else{
        axios
            .post('http://localhost:5000/deleteFavs', payload)
            .then(response => {
                console.log(response.data.message)
                localStorage.setItem('idFavs',response.data.idFavs)
                
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
            });
    }
    

};

const payload = {
    idrecipe: recipeId,
    userToken: userToken,
    comment: "",
    iduser: iduser,
    idcomment: 0
};

onMounted(() => {
    axios
        .post('http://localhost:5000/viewRecipe', payload)
        .then(response => {
            if (response.data.message) {
                receta.value = {
                    ...response.data.message,
                    ingredientes: response.data.message.ingredientes.map(item => item.replace(/[\[\]"]/g, '')),
                    cantidades: response.data.message.cantidades.map(item => item.replace(/[\[\]"]/g, ''))
                };
            } else {
                console.error("Receta no encontrada o error en la respuesta");
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });

    axios
        .post('http://localhost:5000/viewComment', payload)
        .then(response => {
            const commentsArray = response.data.message.map(item => ({
                idcomment: item.idcomment,
                comment: item.comment,
                idrecipe: item.idrecipe,
                iduser: item.iduser,
                username: item.username
            }));

            comments.value = commentsArray;
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
});

function deleteRecipe() {
    axios
        .post('http://localhost:5000/deleteRecipe', payload)
        .then(response => {
            console.log(response.data.message);
            router.push({ name: "home" });
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function editeRecipe() {
    axios
        .post('http://localhost:5000/editeRecipe', payload)
        .then(response => {
            console.log(response.data.message);
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function createComment() {
    payload.comment = comment.value;
    if (userToken) {
        axios
            .post('http://localhost:5000/createComment', payload)
            .then(response => {
                comment.value = "";
                comments.value.push({
                    idcomment: response.data.idcomment,
                    comment: payload.comment,
                    idrecipe: recipeId,
                    iduser: iduser,
                    username: response.data.username
                });
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
            });
    } else {
        router.push({ name: "login" });
    }
}

function deleteComment(idcomment) {
    payload.idcomment = idcomment;
    axios
        .post('http://localhost:5000/deleteComment', payload)
        .then(response => {
            console.log(response.data.message);
            comments.value = comments.value.filter(comment => comment.idcomment !== idcomment);
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}
</script>

<style scoped>
h1,
h2,
h3 {
    font-family: Arial, sans-serif;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin: 5px 0;
}

img {
    width: 100%;
    max-width: 500px;
}

video {
    width: 100%;
    max-width: 500px;
}

.heart-button {
    background: transparent;
    border: none;
    font-size: 36px;
    cursor: pointer;
    transition: color 0.3s ease;
}

.heart-button i {
    color: gray;
}

.heart-button.active i {
    color: pink;
}

button {
    border-radius: 5px;
}

h4 {
    font-size: 1.2rem;
}

.list-group-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.mt-4,
.mb-4 {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

.w-100 {
    width: 100%;
}
</style>
