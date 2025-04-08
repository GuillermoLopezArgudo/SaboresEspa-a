<template>
    <footer class="bg-amber-900 text-amber-50 pt-12 pb-6">
      <div class="container mx-auto px-4">
        <!-- Grid de contenido -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <!-- Columna 1: Logo y descripción -->
          <div class="md:col-span-2">
            <div class="flex items-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span class="ml-2 text-2xl font-bold font-serif">Sabores de España</span>
            </div>
            <p class="text-amber-200 mb-4">
              Descubre las auténticas recetas tradicionales de la cocina española, desde la paella valenciana hasta la tortilla de patatas.
            </p>
            <div class="flex space-x-4">
              <a href="#" class="text-amber-300 hover:text-white transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.675 0h-21.35c-.732 0-1.325.593-1.325 1.325v21.351c0 .731.593 1.324 1.325 1.324h11.495v-9.294h-3.128v-3.622h3.128v-2.671c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12v9.293h6.116c.73 0 1.323-.593 1.323-1.325v-21.35c0-.732-.593-1.325-1.325-1.325z"/>
                </svg>
              </a>
              <a href="#" class="text-amber-300 hover:text-white transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </a>
              <a href="#" class="text-amber-300 hover:text-white transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
                </svg>
              </a>
            </div>
          </div>
  
          <!-- Columna 2: Enlaces rápidos -->
          <div>
            <h3 class="text-xl font-bold mb-4 text-amber-300 font-serif">Recetas destacadas</h3>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-amber-300 transition">Paella Valenciana</a></li>
              <li><a href="#" class="hover:text-amber-300 transition">Tortilla Española</a></li>
              <li><a href="#" class="hover:text-amber-300 transition">Gazpacho Andaluz</a></li>
              <li><a href="#" class="hover:text-amber-300 transition">Fabada Asturiana</a></li>
              <li><a href="#" class="hover:text-amber-300 transition">Pulpo a la Gallega</a></li>
            </ul>
          </div>
  
          <!-- Columna 3: Contacto -->
          <div>
            <h3 class="text-xl font-bold mb-4 text-amber-300 font-serif">Contacto</h3>
            <ul class="space-y-3">
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mt-1 mr-2 text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>info@saboresdeespana.com</span>
              </li>
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mt-1 mr-2 text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <span>+34 912 345 678</span>
              </li>
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mt-1 mr-2 text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Calle de la Cocina, 123<br>Madrid, España</span>
              </li>
            </ul>
          </div>
        </div>
  
        <!-- Divider -->
        <div class="border-t border-amber-700 my-6"></div>
  
        <!-- Copyright y enlaces legales -->
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-amber-300 mb-4 md:mb-0">
            © 2023 Sabores de España. Todos los derechos reservados.
          </p>
          <div class="flex space-x-6">
            <a href="#" class="text-amber-200 hover:text-white transition">Política de privacidad</a>
            <a href="#" class="text-amber-200 hover:text-white transition">Términos de servicio</a>
            <a href="#" class="text-amber-200 hover:text-white transition">Aviso legal</a>
          </div>
        </div>
      </div>
    </footer>
  </template>
  
  <script setup>
  // Puedes añadir lógica aquí si es necesario
  </script>
  
  <style scoped>
  /* Efecto hover para los enlaces de recetas */
  a {
    position: relative;
    transition: all 0.3s ease;
  }
  
  a:after {
    content: '';
    position: absolute;
    width: 0;
    height: 1px;
    bottom: 0;
    left: 0;
    background-color: #f59e0b;
    transition: width 0.3s ease;
  }
  
  a:hover:after {
    width: 100%;
  }
  </style>