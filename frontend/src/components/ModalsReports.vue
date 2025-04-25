<template>
    <!-- Diálogo de reporte de receta -->
    <div v-if="showReportModal" @click.self="showReportModal = false"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2 sm:p-4">
        <div class="bg-white/80 dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden w-full max-w-xs sm:max-w-md">
            <!-- Encabezado con degradado -->
            <div class="bg-gradient-to-r from-amber-600 to-amber-800 p-3 sm:p-4">
                <h3 class="text-lg sm:text-xl font-bold text-white font-serif" v-if="commentId === undefined">Reportar Receta
                </h3>
                <h3 class="text-lg sm:text-xl font-bold text-white font-serif" v-else>Reportar Comentario</h3>
            </div>

            <!-- Contenido -->
            <div class="p-4 sm:p-6">
                <div class="mb-3 sm:mb-5">
                    <label
                        class="block text-amber-800 dark:text-amber-200 font-medium mb-1 sm:mb-2 text-sm sm:text-base">Motivo
                        del reporte</label>
                    <select v-model="reportReason"
                        class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base border-2 border-amber-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500  bg-white/80 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                        <option value="" disabled selected>Selecciona un motivo</option>
                        <option value="Contenido inapropiado">Contenido inapropiado</option>
                        <option value="Información incorrecta">Información incorrecta</option>
                        <option value="Derechos de autor">Derechos de autor</option>
                        <option value="Spam o publicidad">Spam o publicidad</option>
                        <option value="Otro">Otro</option>
                    </select>
                </div>

                <div v-if="reportReason === 'Otro'" class="mb-3 sm:mb-5">
                    <label
                        class="block text-amber-800 dark:text-amber-200 font-medium mb-1 sm:mb-2 text-sm sm:text-base">Explica
                        el
                        problema</label>
                    <textarea v-model="customReason" rows="3"
                        placeholder="Por favor, describe el problema en detalle..."
                        class="resize-none resize-none w-full px-3 py-2 text-sm sm:text-base border-2 border-amber-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 bg-white/80 dark:bg-gray-700 text-gray-900 dark:text-gray-100"></textarea>
                </div>

                <div class="flex justify-end space-x-2 sm:space-x-3 pt-1 sm:pt-2">
                    <button @click="cancelReport"
                        class="px-3 py-1.5 sm:px-4 sm:py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 font-medium rounded-lg flex items-center text-xs sm:text-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1"
                            viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                clip-rule="evenodd" />
                        </svg>
                        Cancelar
                    </button>
                    <button @click="submitReportRecipe"
                        class="px-3 py-1.5 sm:px-4 sm:py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg flex items-center shadow-md text-xs sm:text-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-0.5 sm:mr-1"
                            viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clip-rule="evenodd" />
                        </svg>
                        Enviar Reporte
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineExpose } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification'

const userToken = ref(localStorage.getItem('userToken'))
const props = defineProps(['idrecipe']);

const recipeId = ref(props.idrecipe)
const commentId = ref()
const reportReason = ref('');
const toast = useToast()
const customReason = ref('');
const showReportModal = ref(false);

const showReportDialog = (idComment) => {
    commentId.value = idComment;
    showReportModal.value = true;
};

defineExpose({showReportDialog})

function cancelReport() {
    showReportModal.value = false;
  }

const submitReportRecipe = async () => {
    if (!reportReason.value) {
        toast.warning('Por favor selecciona un motivo para el reporte');
        return;
    }
    if (commentId.value === undefined) {
        const reason = reportReason.value === 'Otro' ? customReason.value : reportReason.value;

        axios.post(`${process.env.VUE_APP_API_URL}/report-recipe`, {
            idrecipe: recipeId.value,
            reason: reason,
            usertoken: userToken.value
        })
            .then(() => {
                toast.success('Gracias por tu reporte. Hemos notificado al equipo administrativo.');
                showReportModal.value = false;
            })
            .catch(error => {
                console.error("Error al reportar:", error);
                toast.error('Ocurrió un error al enviar el reporte. Por favor intenta nuevamente.');
            });
    } else {
        if (!reportReason.value) {
            toast.error('Por favor selecciona un motivo para el reporte');
            return;
        }

        const reason = reportReason.value === 'Otro'
            ? customReason.value
            : reportReason.value;

        try {


            const response = await axios.post(`${process.env.VUE_APP_API_URL}/report-comment`, {
                commentId: commentId.value,
                reason: reason,
                userToken: userToken.value
            });

            if (response.data.message) {
                toast.success('Reporte enviado correctamente. Gracias por ayudar a mejorar la comunidad.');
            }
        } catch (error) {
            console.error("Error al reportar:", error);
            toast.error('Ocurrió un error al enviar el reporte. Por favor intenta nuevamente.');
        } finally {
            cancelReport()
        }
    }

}

</script>

<style scoped></style>