<template>
  <div class="notfound-page">
    <div class="notfound-card">
      <div class="notfound-code">404</div>
      <div class="notfound-icon">
        <i class="pi pi-map"></i>
      </div>
      <h1 class="notfound-title">Página no encontrada</h1>
      <p class="notfound-description">
        La ruta que buscas no existe o no está disponible.<br>
        Comprueba la URL o vuelve a un lugar seguro.
      </p>
      <span class="notfound-path">{{ ruta }}</span>
      <div class="notfound-actions">
        <button class="notfound-btn notfound-btn--primary" @click="irAlInicio">
          <i class="pi pi-home"></i>
          Ir al inicio
        </button>
        <button class="notfound-btn notfound-btn--secondary" @click="volver">
          <i class="pi pi-arrow-left"></i>
          Volver
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import jsNotFound from './script_NotFound.js';

export default {
  name: 'NotFound',
  mixins: [jsNotFound]
};
</script>

<style scoped src="./style_NotFound.css"></style>
