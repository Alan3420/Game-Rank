<template>
  <!-- Iconos propios de los estados: una sola familia solida sobre la
       misma reticula de 24. Se escala con la fuente y usa currentColor, asi que hereda
       tamaño y color de cada vista igual que un icono de PrimeIcons. -->
  <svg class="status-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <path fill="currentColor" fill-rule="evenodd" :d="FORMAS[status] || FORMAS.pendiente" />
  </svg>
</template>

<script setup>
defineProps({
  status: { type: String, required: true }
});

const FORMAS = {
  // reloj de arena con la arena abajo: por jugar
  pendiente: 'M5.5 2h13a1 1 0 0 1 0 2H18v2.4a5 5 0 0 1-2.3 4.2L13.6 12l2.1 1.4a5 5 0 0 1 2.3 4.2V20h.5a1 1 0 0 1 0 2h-13a1 1 0 0 1 0-2H6v-2.4a5 5 0 0 1 2.3-4.2l2.1-1.4-2.1-1.4A5 5 0 0 1 6 6.4V4h-.5a1 1 0 0 1 0-2zM8 4v2.4a3 3 0 0 0 1.4 2.5L12 10.6l2.6-1.7A3 3 0 0 0 16 6.4V4z',
  // mando: jugando
  jugando: 'M7 5h10a5 5 0 0 1 4.9 4l1.1 5.6a3.3 3.3 0 0 1-5.7 2.8L15.3 15.2H8.7l-2 2.2a3.3 3.3 0 0 1-5.7-2.8L2.1 9A5 5 0 0 1 7 5zM6.9 8v1.5H5.4v1.8h1.5v1.5h1.8v-1.5h1.5V9.5H8.7V8zm9.5 0a1.2 1.2 0 1 0 0 2.4a1.2 1.2 0 0 0 0-2.4zm2.2 2.6a1.2 1.2 0 1 0 0 2.4a1.2 1.2 0 0 0 0-2.4z',
  // dos barras: en pausa
  pausado: 'M7.2 4h2.6A1.2 1.2 0 0 1 11 5.2v13.6a1.2 1.2 0 0 1-1.2 1.2H7.2A1.2 1.2 0 0 1 6 18.8V5.2A1.2 1.2 0 0 1 7.2 4zm7 0h2.6A1.2 1.2 0 0 1 18 5.2v13.6a1.2 1.2 0 0 1-1.2 1.2h-2.6a1.2 1.2 0 0 1-1.2-1.2V5.2A1.2 1.2 0 0 1 14.2 4z',
  // circulo con check calado: completado
  completado: 'M12 2a10 10 0 1 1 0 20a10 10 0 0 1 0-20zm4.3 6.2l-5.6 5.6-2.9-2.9-1.5 1.5 4.4 4.4 7.1-7.1z'
};
</script>

<style scoped>
/* los tamaños de cada vista estan pensados para los glifos de PrimeIcons,
   que llenan mas su caja: a 1.3em el icono pesa lo mismo que el texto */
.status-icon {
  display: inline-block;
  flex-shrink: 0;
  width: 1.3em;
  height: 1.3em;
  margin: -0.15em 0;
  vertical-align: -0.28em;
}
</style>
