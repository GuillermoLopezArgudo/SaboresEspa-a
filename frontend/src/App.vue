<template>
  <div>
    <button @click="submit()">Moniato</button>
  </div>
</template>

<script setup>
import axios from "axios";
const enviar = "Hola desde Frontend"
function submit(){
  axios
    .post("http://127.0.0.1:5000/", { enviar })
    .then((response) => {
      const recibir = response.data.message;
      console.log(recibir)
    })
    .catch((error) => {
      console.log(error)
    })
}

</script>

<style></style>
