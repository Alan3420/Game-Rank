<template>
  <div class="tendencias-page">

    <!-- Cabecera -->
    <div class="tendencias-header">
      <span class="tendencias-eyebrow">
        <i class="pi pi-chart-line"></i>
        Comunidad
      </span>
      <h1>Tendencias</h1>
      <p>Descubre los juegos más populares según lo que vota, comenta y colecciona la comunidad.</p>
    </div>

    <!-- Cargando -->
    <div v-if="loading" class="tendencias-loading">
      <i class="pi pi-spin pi-spinner" style="color: var(--color-primary);"></i>
      <span>Calculando tendencias...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="tendencias-error">
      <i class="pi pi-exclamation-circle"></i>
      <span>{{ error }}</span>
    </div>

    <template v-else>

      <!-- Tabs -->
      <div class="tendencias-tabs">
        <button
          v-for="seccion in secciones"
          :key="seccion.key"
          class="tab-btn"
          :class="{ 'is-active': activeTab === seccion.key }"
          @click="activeTab = seccion.key"
        >
          <i class="pi" :class="seccion.icono"></i>
          {{ seccion.label }}
        </button>
      </div>

      <p class="seccion-subtitulo">{{ seccionActiva.subtitulo }}</p>

      <!-- Sin datos -->
      <div v-if="juegosActivos.length === 0" class="seccion-vacia">
        Sin datos suficientes aún. ¡Sé el primero en participar!
      </div>

      <!-- Grid bento -->
      <div v-else class="trend-grid">
        <div
          v-for="game in juegosActivos"
          :key="game.id"
          class="trend-card"
          @click="goToGame(game.id)"
        >
          <img
            v-if="game.imge_url"
            class="trend-card__img"
            :src="game.imge_url"
            :alt="game.name"
            loading="lazy"
          />
          <div v-else class="trend-card__placeholder">
            <i class="pi pi-image"></i>
          </div>

          <div class="trend-card__overlay"></div>

          <div class="trend-card__body">
            <h3 class="trend-card__name">{{ game.name }}</h3>
            <div class="trend-card__meta">
              <span
                class="mc-badge"
                :class="game.metacritic ? metacriticClass(game.metacritic) : 'mc-na'"
              >
                {{ game.metacritic ?? '—' }}
              </span>
              <span class="trend-card__stat">{{ game.stat_label }}</span>
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script>
import tendenciasScript from './script_tendencias.js';

export default {
    name: 'Tendencias',
    ...tendenciasScript,
};
</script>

<style scoped src="./styles_tendencias.css"></style>
