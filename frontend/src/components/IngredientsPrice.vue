<template>
  <div>
      <h1>Categorías de Mercadona</h1>
      <div v-for="producto in productos" :key="producto.id">
          <img :src="producto.thumbnail" alt="Imagen del producto">
          <p>{{ producto.display_name }}</p>
          <p>{{ producto.price_instructions?.bulk_price }} €</p>
      </div>
  </div>
</template>

<script setup>
import { ingredientes } from '@/utils/ingredientes.js'
import axios from 'axios'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const id = ref(0)
const productos = ref([])

const route = useRoute() 

const palabra = route.query.ingredients 

if (palabra && typeof palabra === 'string' && palabra.length > 0) {
const palabrasVariantes = [
  palabra.charAt(0).toUpperCase() + palabra.slice(1),
  palabra.slice(0, -1).charAt(0).toUpperCase() + palabra.slice(1, -1),
  palabra.toLowerCase(),
  palabra.slice(0, -1).toLowerCase() + palabra.slice(-1)
]

const producto = async () => {
  try {
    const response = await axios.post(`${process.env.VUE_APP_API_URL}/productos`, { id: id.value })
  //console.log(response.data)
    response.data.categories.forEach(category => {
      console.log(category)
     // if (palabrasVariantes.some(palabraVar => category.name.toLowerCase().includes(palabraVar.toLowerCase()))) {
        category.products.forEach(product => {
          //console.log(product)
          if (palabrasVariantes.some(palabraVar => product.display_name.toLowerCase().includes(palabraVar.toLowerCase()))) {
            productos.value.push(product)
          }
        })
      //}
    })
  } catch (err) {
    console.error("Error fetching products:", err)
  }
}

const cargarCategorias = async () => {
  try {
    const response = await fetch(`${process.env.VUE_APP_API_URL}/categories`)
    const data = await response.json()

    const categoria = ingredientes[palabrasVariantes[0]]
    console.log(palabrasVariantes[0])
    data.results.forEach(element => {
      element.categories.forEach(cat => {
        if (cat.name.includes(categoria)) {
          id.value = cat.id
          if (id.value > 0) {
            producto()
          }
        }
      })
    })
  } catch (err) {
    console.error("Error fetching categories:", err)
  }
}

cargarCategorias()

} else {
console.error('No se ha pasado un ingrediente válido en la URL.')
}
</script>
