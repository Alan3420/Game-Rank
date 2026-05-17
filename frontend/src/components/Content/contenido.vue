<template>
  <div class="content-overview">
    <div class="catalogo-header">
      <div class="catalogo-header-texto">
        <span class="catalogo-eyebrow">
          <i class="pi pi-th-large"></i>
          Game Catalog
        </span>
        <h1>
          <template v-if="game_name && hasActiveFilters">Filtered results for "{{ game_name }}"</template>
          <template v-else-if="game_name">Results for "{{ game_name }}"</template>
          <template v-else-if="hasActiveFilters">Filtered Catalog</template>
          <template v-else>Explore Our Collection</template>
        </h1>
        <p>
          <template v-if="game_name && hasActiveFilters">Search with {{ activeFiltersCount }} filter{{ activeFiltersCount !== 1 ? 's' : '' }} applied</template>
          <template v-else-if="game_name">Showing search results</template>
          <template v-else-if="hasActiveFilters">{{ activeFiltersCount }} filter{{ activeFiltersCount !== 1 ? 's' : '' }} applied</template>
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
      <h2>No Results</h2>
      <p v-if="game_name">No games found matching "{{ game_name }}"{{ hasActiveFilters ? ' with the applied filters' : '' }}.</p>
      <p v-else>No games found with the applied filters.</p>
    </div>

    <!-- Cards -->
    <Loader v-if="loading" size="small" :message="game_name ? 'Searching games...' : 'Loading games...'" />

    <div v-else-if="!isFiltering || games.length > 0" class="card_content">
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

    <!-- Paginación -->
    <div v-if="!loading && totalPages > 1" class="catalogo-pagination">
      <button
        class="cat-page-btn cat-page-nav"
        :disabled="currentPage === 1"
        @click="fetchPage(currentPage - 1)"
        aria-label="Previous page"
      >
        <i class="pi pi-chevron-left"></i>
      </button>

      <template v-for="(item, i) in paginasVisibles" :key="i">
        <span v-if="item === '...'" class="cat-page-ellipsis">…</span>
        <button
          v-else
          class="cat-page-btn"
          :class="{ 'is-active': currentPage === item }"
          @click="fetchPage(item)"
        >{{ item }}</button>
      </template>

      <button
        class="cat-page-btn cat-page-nav"
        :disabled="currentPage === totalPages"
        @click="fetchPage(currentPage + 1)"
        aria-label="Next page"
      >
        <i class="pi pi-chevron-right"></i>
      </button>
    </div>
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
