<template>
    <div class="container mx-auto mt-5 px-4">
        <h1 class="text-center mb-4 text-3xl font-bold">Receta</h1>
        <div v-if="userToken">
            <router-link to="/home"
                class="btn btn-secondary mb-3 px-4 py-2 border border-gray-300 rounded-md">Atrás</router-link>
        </div>
        <div v-else>
            <router-link to="/"
                class="btn btn-secondary mb-3 px-4 py-2 border border-gray-300 rounded-md">Atrás</router-link>
        </div>
        <div v-if="receta">
            <h2 class="text-primary text-2xl font-semibold">{{ receta.title }}</h2>
            <button @click="toggleFavorite" :class="['heart-button', { 'active': isFavorite }]"
                class="btn btn-outline-danger mb-3 px-4 py-2 border border-red-500 rounded-md">
                <i class="fa" :class="isFavorite ? 'fa-heart' : 'fa-heart-o'"></i> Favoritos
            </button>
            <p class="lead text-lg">{{ receta.descripcion }}</p>
            <div v-if="receta.image" class="mb-4">
                <img :src="`http://localhost:5000/${receta.image}`" alt="Imagen de la receta"
                    class="w-full rounded-lg shadow-lg" />
            </div>
            <h3 class="text-secondary text-xl font-semibold">Ingredientes:</h3>
            <ul class="list-none mb-4">
                <li v-for="(ingrediente, idx) in ingredients" :key="idx" class="mb-2">
                    {{ ingrediente }} - {{ quantity[idx] || 'Cantidad no disponible' }}
                </li>
            </ul>
            <div v-if="receta.video" class="my-4">
                <video controls :src="'http://localhost:5000/' + receta.video"
                    class="w-full rounded-lg shadow-lg"></video>
            </div>
            <div v-if="receta.assessment" class="my-3">
                <p><strong>Valoración:</strong> {{ receta.valoraciones }} estrellas</p>
            </div>
            <div v-if="comment != null" class="my-4">
                <h4 class="text-xl font-semibold">Comentarios:</h4>
                <ul class="list-none">
                    <li v-for="comment in comments" :key="comment.id" class="mb-4">
                        <strong>Comentario:</strong>
                        <div v-if="editingCommentId === comment.id" class="mb-2">
                            <input type="text" v-model="editedComment"
                                class="form-control mb-2 p-2 border border-gray-300 rounded-md" />
                            <button @click="updateComment(comment.id)"
                                class="btn btn-sm bg-green-500 text-white px-4 py-2 rounded-md mr-2">Actualizar</button>
                            <button @click="cancelEdit"
                                class="btn btn-sm bg-gray-500 text-white px-4 py-2 rounded-md">Cancelar</button>
                        </div>
                        <div v-else>
                            {{ comment.comment }} <br>
                            <small>Usuario: {{ comment.username }}</small>
                            <div v-if="iduser == comment.iduser">
                                <button @click="startEditComment(comment)"
                                    class="btn btn-sm bg-yellow-500 text-white px-4 py-2 rounded-md mr-2">Editar</button>
                                <button @click="deleteComment(comment.id)"
                                    class="btn btn-sm bg-red-500 text-white px-4 py-2 rounded-md">Eliminar</button>
                            </div>
                        </div>
                    </li>
                </ul>
                <div class="mt-3">
                    <input type="text" placeholder="Escribe tu comentario..." v-model="comment"
                        class="form-control mb-2 p-2 border border-gray-300 rounded-md" :value="comment" />
                    <button @click.prevent="createComment" class="btn btn-primary w-full py-2 rounded-md">Enviar
                        Comentario</button>
                </div>
            </div>
            <div v-if="iduser == receta.id_user" class="mt-4">
                <button @click="deleteRecipe" class="btn bg-red-600 text-white w-full py-2 rounded-md mb-2">Eliminar
                    Receta</button>
                <button @click="editeRecipe" class="btn bg-yellow-500 text-white w-full py-2 rounded-md">Editar
                    Receta</button>
            </div>
        </div>
        <p v-else class="text-center text-muted">Cargando receta...</p>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
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
const ingredients = reactive([]);
const quantity = reactive([]);
const comments = reactive([]);
const isFavorite = ref(false);
const editingCommentId = ref(null);
const editedComment = ref("");
const payload = {
    idrecipe: parseInt(recipeId),
    userToken: userToken,
    comment: "",
    iduser: iduser,
    idcomment: 0
};

const toggleFavorite = () => {
    if (iduser) {
        isFavorite.value = !isFavorite.value;
        if (isFavorite.value) {
            axios
                .post('http://localhost:5000/updateFavs', payload)
                .then(response => {
                    console.log(response.data.message)
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        } else {
            axios
                .post('http://localhost:5000/deleteFavs', payload)
                .then(response => {
                    console.log(response.data.message)
                })
                .catch(error => {
                    console.error("Error en la solicitud:", error);
                });
        }
    } else {
        router.push({ name: "login" });
    }
};

onMounted(() => {
    
    axios
        .post('http://localhost:5000/viewRecipe', payload)
        .then(response => {
            receta.value = response.data.recipe_list[0]
            response.data.ingredient_list.forEach(element => {
                ingredients.push(element.ingredients);
                quantity.push(element.quantity)
            });
            if (iduser) {
                response.data.favorites_list.forEach(id => {
                    if (id.id_recipe === parseInt(recipeId)) {
                        isFavorite.value = true;
                    }
                });
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });

    axios
        .post('http://localhost:5000/viewComment', payload)
        .then(response => {
            comments.splice(0, comments.length, ...response.data.comment_list);
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
    router.push({ name: "edite", query: { id: recipeId } });
}

function createComment() {
    payload.comment = comment.value;
    if (userToken) {
        axios
            .post('http://localhost:5000/createComment', payload)
            .then(response => {
                const newComment = {
                    idcomment: response.data.idcomment,
                    comment: comment.value,
                    username: response.data.username,
                    iduser: iduser
                };
                comments.splice(0, comments.length, ...comments, newComment);
                comment.value = "";
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
            console.log(comments)
            comments.splice(0, comments.length, ...comments.filter(comment => comment.idcomment !== idcomment));
            console.log(comments)
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function updateComment(idcomment) {
    payload.idcomment = idcomment;
    payload.comment = editedComment.value;

    axios
        .post('http://localhost:5000/editeComment', payload)
        .then(response => {
            const updatedComment = comments.find(comment => comment.idcomment === idcomment);
            console.log(response.data.message);
            updatedComment.comment = editedComment.value;
            comments.splice(0, comments.length, ...comments);  // Force update the reactive array
            cancelEdit();
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
        });
}

function startEditComment(comment) {
    editingCommentId.value = comment.id;
    editedComment.value = comment.comment;
}

function cancelEdit() {
    editingCommentId.value = null;
    editedComment.value = "";
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
