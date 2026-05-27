<template>
  <div class="content-overview">
    <div class="catalogo-header">
      <div class="catalogo-header-texto">
        <span class="catalogo-eyebrow">
          <i class="pi pi-th-large"></i>
          Game Catalog
        </span>
        <h1>
          <template v-if="game_name && tieneFiltrosActivos">Filtered results for "{{ game_name }}"</template>
          <template v-else-if="game_name">Results for "{{ game_name }}"</template>
          <template v-else-if="tieneFiltrosActivos">Filtered Catalog</template>
          <template v-else>Explore Our Collection</template>
        </h1>
        <p>
          <template v-if="game_name && tieneFiltrosActivos">Search with {{ cantidadFiltrosActivos }} filter{{ cantidadFiltrosActivos !== 1 ? 's' : '' }} applied</template>
          <template v-else-if="game_name">Showing search results</template>
          <template v-else-if="tieneFiltrosActivos">{{ cantidadFiltrosActivos }} filter{{ cantidadFiltrosActivos !== 1 ? 's' : '' }} applied</template>
          <template v-else>Find your next favorite game among hundreds of titles</template>
        </p>
      </div>

      <div class="catalogo-header-actions">
        <button
          class="filter-toggle-btn"
          :class="{ 'is-active': filterPanelOpen }"
          @click="filterPanelOpen = !filterPanelOpen"
        >
          <i class="pi pi-sliders-h"></i>
          <span>Filters</span>
          <span v-if="cantidadFiltrosActivos > 0" class="filter-badge">{{ cantidadFiltrosActivos }}</span>
          <i class="pi" :class="filterPanelOpen ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
        </button>
      </div>
    </div>

    <div class="filter-panel-anchor">
      <FilterPanel :open="filterPanelOpen" @apply="aplicarFiltros" @clear="limpiarFiltros" />
    </div>

    <!-- Empty state -->
    <div v-if="estaFiltrando && !loading && games.length === 0" class="search-empty">
      <div class="search-empty-icon">
        <i class="pi pi-search"></i>
      </div>
      <h2>No Results</h2>
      <p v-if="game_name">No games found matching "{{ game_name }}"{{ tieneFiltrosActivos ? ' with the applied filters' : '' }}.</p>
      <p v-else>No games found with the applied filters.</p>
    </div>

    <!-- Cards -->
    <Loader v-if="loading" size="small" :message="game_name ? 'Searching games...' : 'Loading games...'" />

    <div v-else-if="!estaFiltrando || games.length > 0" class="card_content">
      <GameCard
        v-for="(game, index) in games"
        :key="game.id"
        :game="game"
        :index="index"
        :is-favorite="favorites.has(game.id)"
        :status="statuses.get(game.id) || null"
        @click="irADetalle(game.id)"
        @action="alternarFavorito"
        @update:status="manejarActualizacionEstado"
      />
    </div>

    <!-- Paginación -->
    <Pagination
      v-if="!loading"
      :current-page="currentPage"
      :total-pages="totalPaginas"
      @update:current-page="cargarPagina"
    />
  </div>
</template>

<script>
import contenido from "./script_contenido.js";
import Button from "primevue/button"
import GameCard from "../Cards/GameCard.vue"
import Loader from "../Loader/Loader.vue"
import FilterPanel from "../Filters/FilterPanel.vue"
import Pagination from "../Pagination/Pagination.vue"

export default {
    name: 'contenido',
    components: { Button, GameCard, Loader, FilterPanel, Pagination },
    ...contenido
};
</script>

<style scoped src="./style_contenido.css"></style>
