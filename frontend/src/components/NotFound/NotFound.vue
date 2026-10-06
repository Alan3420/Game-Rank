<template>
  <div class="notfound card-world">
    <div class="nf-shell">

      <!-- ranura vacia del album: la carta que falta -->
      <div class="nf-sleeve" aria-hidden="true">
        <span class="nf-sleeve__art">
          <i class="pi pi-question"></i>
        </span>
        <span class="nf-sleeve__name">Missing card</span>
        <span class="nf-sleeve__set">
          <span class="nf-sleeve__no">No. 404</span>
          <span>Not in the set</span>
        </span>
      </div>

      <div class="nf-text">
        <h1 class="nf-title">This page isn't in the set</h1>
        <p class="nf-lede">The address doesn't match any page in Game Rank. It may have moved, or the link has a typo.</p>
        <p class="nf-path"><span class="sr-only">Requested address: </span><code>{{ ruta }}</code></p>
        <div class="nf-actions">
          <router-link to="/" class="nf-btn nf-btn--primary">
            <i aria-hidden="true" class="pi pi-home"></i>
            Go home
          </router-link>
          <router-link to="/content/overview" class="nf-btn">
            <i aria-hidden="true" class="pi pi-th-large"></i>
            Browse the catalog
          </router-link>
          <button type="button" class="nf-btn nf-btn--quiet" @click="volver">
            <i aria-hidden="true" class="pi pi-arrow-left"></i>
            Go back
          </button>
        </div>
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
