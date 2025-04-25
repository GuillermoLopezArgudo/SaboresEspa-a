<template>
    <!-- Comentarios -->
    <div class="p-4 sm:p-6 md:p-8 border-t border-amber-100 dark:border-gray-700">     
        <h3 class="text-lg sm:text-xl font-bold text-amber-800 dark:text-amber-200 mb-2 sm:mb-4 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 sm:h-6 sm:w-6 mr-1 sm:mr-2 text-amber-600 dark:text-amber-400" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Comentarios
        </h3>

        <!-- Lista de comentarios -->
        <div v-if="comments.length > 0 " class="space-y-3 sm:space-y-4 md:space-y-6 mb-4 sm:mb-6">
            <div v-for="comment in commentsWithSubcomments" :key="comment.id"
                class="bg-white/80 dark:bg-gray-700 p-3 sm:p-4 rounded-lg border border-amber-200 dark:border-gray-600 shadow-sm hover:shadow-md ">
                <!-- Comentario principal -->
                <div class="mb-3 sm:mb-4">
                    <div v-if="editingCommentId === comment.id" class="mb-2 sm:mb-3">
                        <textarea v-model="editedComment" rows="3"
                            class="resize-none w-full px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border-2 border-amber-300 dark:border-amber-500 focus:ring-2 focus:ring-amber-500 focus:border-amber-500  bg-white/80 dark:bg-gray-800 text-gray-900 dark:text-gray-100"></textarea>
                        <div class="flex flex-wrap gap-1 sm:gap-2 mt-1 sm:mt-2">
                            <button @click="updateComment(comment.id)"
                                class="px-2 py-1 sm:px-4 sm:py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg  flex items-center text-xs sm:text-sm">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1"
                                    viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd"
                                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                        clip-rule="evenodd" />
                                </svg>
                                Guardar
                            </button>
                            <button @click="cancelEdit"
                                class="px-2 py-1 sm:px-4 sm:py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg  flex items-center text-xs sm:text-sm">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1"
                                    viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd"
                                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                        clip-rule="evenodd" />
                                </svg>
                                Cancelar
                            </button>
                        </div>
                    </div>
                    <div v-else>
                        <!-- Contenedor del botón -->
                        <div class="flex justify-end">
                            <div class="relative" :ref="el => menuRefs[comment.id] = el">
                                <!-- Botón tres puntitos -->
                                <button @click="toggleMenu(comment.id)"
                                    class="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-200 rounded-lg text-xs sm:text-sm  flex items-center">
                                    <i class="fa fa-ellipsis-h text-xs sm:text-sm mr-1"></i>
                                </button>

                                <!-- Menú desplegable -->
                                <div v-if="isMenuVisible[comment.id]"
                                    class="absolute right-0 mt-2 w-40 sm:w-44 bg-white/80 dark:bg-gray-700 shadow-lg rounded-lg z-50 flex flex-col gap-1 p-1 sm:p-2 border border-gray-200 dark:border-gray-600">

                                    <!-- BOTÓN: Reportar -->
                                    <button v-if="userToken" @click="callChildFunction((comment.id))"
                                        class="w-full flex items-center px-2 py-1 text-red-600 dark:text-red-300 bg-red-100 hover:bg-red-200 dark:bg-red-900 dark:hover:bg-red-800 rounded text-xs sm:text-sm ">
                                        <i class="fa fa-flag mr-1"></i> Reportar
                                    </button>

                                    <!-- BOTÓN: Editar -->
                                    <button v-if="userToken == comment.userToken || type == 'admin'"
                                        @click="startEditComment(comment)"
                                        class="w-full flex items-center px-2 py-1 text-white bg-amber-500 hover:bg-amber-600 dark:bg-amber-600 dark:hover:bg-amber-700 rounded text-xs sm:text-sm">
                                        <i class="fa fa-pencil mr-1"></i> Editar
                                    </button>

                                    <!-- BOTÓN: Eliminar -->
                                    <button v-if="userToken == comment.userToken || type == 'admin'"
                                        @click="deleteComment(comment.id)"
                                        class="w-full flex items-center px-2 py-1 text-white bg-red-500 hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700 rounded text-xs sm:text-sm ">
                                        <i class="fa fa-trash mr-1"></i> Eliminar
                                    </button>
                                </div>
                            </div>
                        </div>
                        <p
                            class="text-amber-800 dark:text-amber-200 text-sm sm:text-base break-words w-full max-w-[90%] sm:max-w-[90%] md:max-w-[95%] lg:max-w-[90%]">
                            {{ comment.comment }}</p>
                        <p class="text-xs text-amber-600 dark:text-amber-400 mt-0.5 sm:mt-1">Por: {{ comment.username }}
                        </p>
                        <div class="flex flex-wrap items-center gap-1 sm:gap-2 mt-1 sm:mt-2">
                            <!-- Botones de interacción -->
                            <div class="flex gap-1 sm:gap-2 items-center">
                                <!-- LIKE -->
                                <button @click="toggleLike(comment.id)"
                                    class="focus:outline-none flex items-center gap-0.5 sm:gap-1">
                                    <svg class="w-4 h-4 sm:w-5 sm:h-5 text-green-800 hover:text-green-900 dark:text-green-500 dark:hover:text-green-400"
                                        :fill="likedComments[comment.id] ? 'currentColor' : 'none'"
                                        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M7 11c.889-.086 1.416-.543 2.156-1.057a22.323 22.323 0 0 0 3.958-5.084 1.6 1.6 0 0 1 .582-.628 1.549 1.549 0 0 1 1.466-.087c.205.095.388.233.537.406a1.64 1.64 0 0 1 .384 1.279l-1.388 4.114M7 11H4v6.5A1.5 1.5 0 0 0 5.5 19v0A1.5 1.5 0 0 0 7 17.5V11Zm6.5-1h4.915c.286 0 .372.014.626.15.254.135.472.332.637.572a1.874 1.874 0 0 1 .215 1.673l-2.098 6.4C17.538 19.52 17.368 20 16.12 20c-2.303 0-4.79-.943-6.67-1.475" />
                                    </svg>
                                    <span class="text-green-800 dark:text-green-500 text-xs sm:text-sm">{{
                                        conteoLikes[comment.id] || 0 }}</span>
                                </button>
                                <!-- DISLIKE -->
                                <button @click="toggleDislike(comment.id)"
                                    class="focus:outline-none flex items-center gap-0.5 sm:gap-1">
                                    <svg class="w-4 h-4 sm:w-5 sm:h-5 text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                                        :fill="dislikedComments[comment.id] ? 'currentColor' : 'none'"
                                        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M17 13c-.889.086-1.416.543-2.156 1.057a22.322 22.322 0 0 0-3.958 5.084 1.6 1.6 0 0 1-.582.628 1.549 1.549 0 0 1-1.466.087 1.587 1.587 0 0 1-.537-.406 1.666 1.666 0 0 1-.384-1.279l1.389-4.114M17 13h3V6.5A1.5 1.5 0 0 0 18.5 5v0A1.5 1.5 0 0 0 17 6.5V13Zm-6.5 1H5.585c-.286 0-.372-.014-.626-.15a1.797 1.797 0 0 1-.637-.572 1.873 1.873 0 0 1-.215-1.673l2.098-6.4C6.462 4.48 6.632 4 7.88 4c2.302 0 4.79.943 6.67 1.475" />
                                    </svg>
                                    <span class="text-red-600 dark:text-red-400 text-xs sm:text-sm">{{
                                        conteoDisLikes[comment.id] || 0 }}</span>
                                </button>
                            </div>
                            <!-- BOTON DE RESPUESTA -->
                            <div class="ml-auto">
                                <button @click="toggleReply(comment.id)"
                                    class="px-2 py-0.5 sm:px-3 sm:py-1 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900 dark:hover:bg-blue-800 text-blue-600 dark:text-blue-300 rounded-lg text-xs sm:text-sm  flex items-center">
                                    <i class="fa fa-reply text-xs sm:text-sm mr-0.5 sm:mr-1"></i> Responder
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Subcomentarios -->
                <div v-if="comment.subcomments && comment.subcomments.length > 0"
                    class="ml-4 sm:ml-6 md:ml-8 pl-2 sm:pl-3 md:pl-4 border-l-2 border-amber-200 dark:border-gray-600 space-y-2 sm:space-y-3">
                    <div v-for="subcomment in comment.subcomments" :key="subcomment.id"
                        class="bg-amber-50 dark:bg-gray-800 p-2 sm:p-3 rounded-lg">
                        <div v-if="editingSubcommentId === subcomment.id">
                            <textarea v-model="editedSubcomment" rows="2"
                                class="resize-none w-full px-2 py-1 sm:px-3 sm:py-1 text-sm sm:text-base rounded-lg border-2 border-amber-300 dark:border-amber-500 focus:ring-2 focus:ring-amber-500 focus:border-amber-500  bg-white/80 dark:bg-gray-700 text-gray-900 dark:text-gray-100"></textarea>
                            <div class="flex flex-wrap gap-1 sm:gap-2 mt-1 sm:mt-2">
                                <button @click="updateSubcomment(subcomment.id)"
                                    class="px-2 py-0.5 sm:px-3 sm:py-1 bg-green-500 hover:bg-green-600 text-white rounded text-xs sm:text-sm">
                                    Guardar
                                </button>
                                <button @click="cancelEditSubcomment"
                                    class="px-2 py-0.5 sm:px-3 sm:py-1 bg-gray-400 hover:bg-gray-500 text-white rounded text-xs sm:text-sm">
                                    Cancelar
                                </button>
                            </div>
                        </div>
                        <div v-else>
                            <!-- Botón que activa el submenú -->
                            <div class="flex justify-end">
                                <div class="relative" :ref="el => subMenuRefs[subcomment.id] = el">
                                    <button @click="toggleSubMenu(subcomment.id)"
                                        class="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-200 rounded-lg text-xs sm:text-sm  flex items-center">
                                        <i class="fa fa-ellipsis-h text-xs sm:text-sm mr-1"></i>
                                    </button>

                                    <!-- Menú desplegable -->
                                    <div v-if="isSubMenuVisible[subcomment.id]"
                                        class="absolute right-0 mt-2 w-40 sm:w-44 bg-white/80 dark:bg-gray-700 shadow-lg rounded-lg z-50 flex flex-col gap-1 p-1 sm:p-2 border border-gray-200 dark:border-gray-600">

                                        <!-- BOTÓN: Reportar -->
                                        <button v-if="userToken" @click="callChildFunction((comment.id))"
                                            class="w-full flex items-center px-2 py-1 text-red-600 dark:text-red-300 bg-red-100 hover:bg-red-200 dark:bg-red-900 dark:hover:bg-red-800 rounded text-xs sm:text-sm ">
                                            <i class="fa fa-flag mr-1"></i> Reportar
                                        </button>

                                        <!-- BOTÓN: Editar -->
                                        <button v-if="userToken == subcomment.userToken || type == 'admin'"
                                            @click="startEditSubcomment(subcomment)"
                                            class="w-full flex items-center px-2 py-1 text-white bg-amber-400 hover:bg-amber-500 dark:bg-amber-500 dark:hover:bg-amber-600 rounded text-xs sm:text-sm ">
                                            <i class="fa fa-pencil mr-1"></i> Editar
                                        </button>

                                        <!-- BOTÓN: Eliminar -->
                                        <button v-if="userToken == subcomment.userToken || type == 'admin'"
                                            @click="deleteSubcomment(subcomment.id)"
                                            class="w-full flex items-center px-2 py-1 text-white bg-red-400 hover:bg-red-500 dark:bg-red-500 dark:hover:bg-red-600 rounded text-xs sm:text-sm ">
                                            <i class="fa fa-trash mr-1"></i> Eliminar
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <p
                                class="text-amber-700 dark:text-amber-300 text-sm sm:text-base break-words w-full max-w-[90%] sm:max-w-[90%] md:max-w-[90%] lg:max-w-[90%]">
                                {{ subcomment.comment }}</p>
                            <p class="text-xs text-amber-500 dark:text-amber-400 mt-0.5 sm:mt-1">Por: {{
                                subcomment.username }}</p>

                        </div>
                    </div>
                </div>

                <!-- Formulario de respuesta (subcomentario) -->
                <div v-if="replyingTo === comment.id" class="mt-2 sm:mt-3 ml-4 sm:ml-6 md:ml-8">
                    <textarea v-model="replyComment" rows="2" placeholder="Escribe tu respuesta..."
                        class="resize-none w-full px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border-2 border-amber-300 dark:border-amber-500 focus:ring-2 focus:ring-amber-500 focus:border-amber-500  bg-white/80 dark:bg-gray-800 text-gray-900 dark:text-gray-100"></textarea>
                    <div class="flex flex-wrap gap-1 sm:gap-2 mt-1 sm:mt-2">
                        <button @click="createSubcomment(comment.id)"
                            class="px-2 py-1 sm:px-4 sm:py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg  text-xs sm:text-sm">
                            Enviar respuesta
                        </button>
                        <button @click="cancelReply"
                            class="px-2 py-1 sm:px-4 sm:py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg  text-xs sm:text-sm">
                            Cancelar
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div v-else
            class="bg-amber-50 dark:bg-gray-700 p-3 sm:p-4 rounded-lg border border-amber-200 dark:border-gray-600 text-center text-amber-700 dark:text-amber-300 mb-4 sm:mb-6 text-sm sm:text-base">
            No hay comentarios aún. ¡Sé el primero en comentar!
        </div>

        <!-- Formulario de comentario principal -->
        <div v-if="userToken !== 'notoken'" class="mt-3 sm:mt-4">
            <textarea v-model="newComment" rows="3" placeholder="Escribe tu comentario..."
                class="resize-none resize-none w-full px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base rounded-lg border-2 border-amber-300 dark:border-amber-500 focus:ring-2 focus:ring-amber-500 focus:border-amber-500  bg-white/80 dark:bg-gray-800 text-gray-900 dark:text-gray-100"></textarea>
            <button @click="createComment"
                class="mt-1 sm:mt-2 w-full py-1.5 sm:py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg  flex items-center justify-center text-sm sm:text-base">
                <i class="fa fa-paper-plane text-xs sm:text-sm mr-1 sm:mr-2"></i> Enviar Comentario
            </button>
        </div>
        <div v-else class="text-center py-2 sm:py-4 text-sm sm:text-base">
            <router-link to="/login"
                class="text-amber-600 hover:text-amber-800 dark:text-amber-400 dark:hover:text-amber-300 font-medium">
                Inicia sesión para dejar un comentario
            </router-link>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps,defineExpose  } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const props = defineProps(['idrecipe','commentsWithSubcomments']);
const subcomments = ref([]);
const comments = ref([]);
defineExpose({fetchRecipe})
const newComment = ref("");
const userToken = ref(localStorage.getItem('userToken') || "notoken");
const router = useRouter();
const replyComment = ref("");
const replyingTo = ref(null);
const recipeId = ref(props.idrecipe)
const commentsWithSubcomments = ref(props.commentsWithSubcomments)
const payload = {
    idrecipe: parseInt(recipeId.value),
    userToken: userToken.value,
    comment: "",
    idcomment: 0
};

function createComment() {
    if (!newComment.value.trim()) return;

    payload.comment = newComment.value;
    payload.idcomment = 0;

    axios.post(`${process.env.VUE_APP_API_URL}/createComment`, payload)
        .then(() => {
            fetchRecipe();
            newComment.value = "";
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
            if (error.response?.status === 401) {
                router.push({ name: "login" });
            }
        });
}

function createSubcomment(commentId) {
    if (!replyComment.value.trim()) return;

    payload.comment = replyComment.value;
    payload.idcomment = commentId;

    axios.post(`${process.env.VUE_APP_API_URL}/createSubComment`, payload)
        .then(() => {
            fetchRecipe();
            replyComment.value = "";
            replyingTo.value = null;
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
            if (error.response?.status === 401) {
                router.push({ name: "login" });
            }
        });

}

function fetchRecipe() {
    console.log("EJECUTADO")
    axios
        .post(`${process.env.VUE_APP_API_URL}/viewComment`, payload)
        .then(response => {
            comments.value = response.data.comment_list;
            subcomments.value = response.data.subcomments_list || [];
            
        })
        .catch(error => console.error("Error en la solicitud:", error));
}

</script>

<style lang="scss" scoped></style>