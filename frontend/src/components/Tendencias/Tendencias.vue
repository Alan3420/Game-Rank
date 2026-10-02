<template>
  <div class="tendencias-page">

    <!-- Cabecera -->
    <div class="tendencias-header">
      <span class="tendencias-eyebrow">
        <i aria-hidden="true" class="pi pi-chart-line"></i>
        Community
      </span>
      <h1>Trends</h1>
      <p>Discover the most popular games based on what the community votes, comments and collects.</p>
    </div>

    <!-- Cargando -->
    <div v-if="loading" aria-busy="true">
      <div class="tendencias-tabs">
        <Skeleton v-for="n in 4" :key="n" width="110px" height="36px" radius="999px" />
      </div>

      <div v-for="s in 2" :key="s" class="tendencias-seccion">
        <div class="seccion-header">
          <Skeleton width="2rem" height="2rem" radius="10px" />
          <div class="trend-skel-header-text">
            <Skeleton width="180px" height="1.2rem" />
            <Skeleton width="280px" height="0.8rem" />
          </div>
        </div>
        <div class="trend-grid">
          <Skeleton v-for="n in 5" :key="n" class="trend-skel" radius="16px" />
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="tendencias-error">
      <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
      <span>{{ error }}</span>
    </div>

    <template v-else>

      <!-- Nav de scroll -->
      <div class="tendencias-tabs">
        <button
          v-for="seccion in secciones"
          :key="seccion.key"
          class="tab-btn"
          @click="desplazarASeccion(seccion.key)"
        >
          <i aria-hidden="true" class="pi" :class="seccion.icono"></i>
          {{ seccion.label }}
        </button>
      </div>

      <!-- Secciones -->
      <div
        v-for="seccion in secciones"
        :key="seccion.key"
        :id="seccion.key"
        class="tendencias-seccion"
      >
        <div class="seccion-header">
          <i aria-hidden="true" class="pi seccion-header__icono" :class="seccion.icono"></i>
          <div>
            <h2 class="seccion-header__titulo">{{ seccion.titulo }}</h2>
            <p class="seccion-subtitulo">{{ seccion.subtitulo }}</p>
          </div>
        </div>

        <div v-if="!tendencias[seccion.key] || tendencias[seccion.key].length === 0" class="seccion-vacia">
          Not enough data yet. Be the first to participate!
        </div>

        <div v-else class="trend-grid">
          <div
            v-for="game in tendencias[seccion.key]"
            :key="game.id"
            v-activable
            class="trend-card"
            :aria-label="game.name"
            @click="irAJuego(game.id)"
          >
            <img
              v-if="game.imge_url"
              class="trend-card__img"
              :src="game.imge_url"
              alt=""
              width="640"
              height="360"
              loading="lazy"
              decoding="async"
            />
            <div v-else class="trend-card__placeholder">
              <i aria-hidden="true" class="pi pi-image"></i>
            </div>

            <div class="trend-card__overlay"></div>

            <div class="trend-card__body">
              <h3 class="trend-card__name">{{ game.name }}</h3>
              <div class="trend-card__meta">
                <span
                  class="mc-badge"
                  :class="game.metacritic ? claseMetacritic(game.metacritic) : 'mc-na'"
                >
                  {{ game.metacritic ?? '—' }}
                </span>
                <span class="trend-card__stat">{{ formatearEtiquetaTendencia(seccion.key, game.stat_value) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script>
import tendenciasScript from './script_tendencias.js';
import Skeleton from '../Skeleton/Skeleton.vue';

export default {
    name: 'Tendencias',
    components: { Skeleton },
    ...tendenciasScript,
};
</script>

<style scoped src="./styles_tendencias.css"></style>
