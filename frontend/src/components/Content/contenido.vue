<template>
  <div class="content-overview">
    <div class="catalogo-header">
      <div class="catalogo-header-texto">
        <span class="catalogo-eyebrow">
          <i class="pi pi-th-large"></i>
          Catálogo de juegos
        </span>
        <h1>
          <template v-if="game_name && hasActiveFilters">Resultados filtrados para "{{ game_name }}"</template>
          <template v-else-if="game_name">Resultados para "{{ game_name }}"</template>
          <template v-else-if="hasActiveFilters">Catálogo filtrado</template>
          <template v-else>Explora nuestra colección</template>
        </h1>
        <p>
          <template v-if="game_name && hasActiveFilters">Búsqueda con {{ activeFiltersCount }} filtro{{ activeFiltersCount !== 1 ? 's' : '' }} aplicado{{ activeFiltersCount !== 1 ? 's' : '' }}</template>
          <template v-else-if="game_name">Mostrando resultados de búsqueda</template>
          <template v-else-if="hasActiveFilters">{{ activeFiltersCount }} filtro{{ activeFiltersCount !== 1 ? 's' : '' }} aplicado{{ activeFiltersCount !== 1 ? 's' : '' }}</template>
          <template v-else>Encuentra tu próximo juego favorito entre cientos de títulos</template>
        </p>
      </div>

      <div class="catalogo-header-actions">
        <button
          class="filter-toggle-btn"
          :class="{ 'is-active': filterPanelOpen }"
          @click="filterPanelOpen = !filterPanelOpen"
        >
          <i class="pi pi-sliders-h"></i>
          <span>Filtros</span>
          <span v-if="activeFiltersCount > 0" class="filter-badge">{{ activeFiltersCount }}</span>
          <i class="pi" :class="filterPanelOpen ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
        </button>
      </div>
    </div>

    <div class="filter-panel-anchor">
      <FilterPanel :open="filterPanelOpen" @apply="applyFilters" @clear="clearFilters" />
    </div>

    <!-- Empty state -->
    <div v-if="isFiltering && !loading && games.length === 0" class="search-empty">
      <div class="search-empty-icon">
        <i class="pi pi-search"></i>
      </div>
      <h2>Sin resultados</h2>
      <p v-if="game_name">No encontramos juegos que coincidan con "{{ game_name }}"{{ hasActiveFilters ? ' con los filtros aplicados' : '' }}.</p>
      <p v-else>No encontramos juegos con los filtros aplicados.</p>
    </div>

    <!-- Cards -->
    <div v-else class="card_content">
      <GameCard
        v-for="(game, index) in games"
        :key="game.id"
        :game="game"
        :index="index"
        :is-favorite="favorites.has(game.id)"
        :status="statuses.get(game.id) || null"
        @click="goToDetail(game.id)"
        @action="toggleFavorite"
        @update:status="handleStatusUpdate"
      />
    </div>

    <div v-if="showLoadMoreButton && !loading" class="load-more-container">
      <Button label="Cargar más juegos" @click="loadMore" class="load-more-btn" />
    </div>

    <Loader v-if="loading" size="small" :message="game_name ? 'Buscando juegos...' : 'Cargando más juegos...'" />
  </div>
</template>

<script>
import contenido from "./script_contenido.js";
import Button from "primevue/button"
import GameCard from "../Cards/GameCard.vue"
import Loader from "../Loader/Loader.vue"
import FilterPanel from "../Filters/FilterPanel.vue"

export default {
    name: 'contenido',
    components: { Button, GameCard, Loader, FilterPanel },
    ...contenido
};
</script>

<style scoped src="./style_contenido.css"></style>
