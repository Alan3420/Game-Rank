<template>
  <div class="content-overview">
    <div class="catalogo-header">
      <div class="catalogo-header-texto">
        <span class="catalogo-eyebrow">
          <i class="pi pi-th-large"></i>
          Catálogo de juegos
        </span>
        <h1>{{ game_name ? `Resultados para "${game_name}"` : 'Explora nuestra colección' }}</h1>
        <p>{{ game_name ? `Mostrando resultados de búsqueda` : 'Encuentra tu próximo juego favorito entre cientos de títulos' }}</p>
      </div>
    </div>

    <!-- Empty state búsqueda -->
    <div v-if="game_name && !loading && games.length === 0" class="search-empty">
      <div class="search-empty-icon">
        <i class="pi pi-search"></i>
      </div>
      <h2>Sin resultados</h2>
      <p>No encontramos juegos que coincidan con "{{ game_name }}".</p>
    </div>

    <!-- Cards usando GameCard component -->
    <div v-else class="card_content">
      <GameCard
        v-for="game in games"
        :key="game.id"
        :game="game"
        :is-favorite="favorites.has(game.id)"
        @click="goToDetail(game.id)"
        @action="toggleFavorite"
      />
    </div>

    <div v-if="showLoadMoreButton && !game_name && !loading" class="load-more-container">
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

export default {
    name: 'contenido',
    components: { Button, GameCard, Loader },
    ...contenido
};
</script>

<style scoped src="./style_contenido.css"></style>