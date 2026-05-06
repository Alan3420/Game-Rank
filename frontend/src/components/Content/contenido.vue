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

        <!-- Cards (mismo estilo en catálogo y búsqueda) -->
        <div v-else class="card_content">
            <div v-for="game in games" :key="game.id" class="game-card" @click="goToDetail(game.id)">
                <div class="card-image">
                    <img :src="game.imge_url" :alt="game.name" class="game-image" />
                    <div class="image-overlay"></div>
                    <div class="rating-badge">
                        <i class="pi pi-star-fill"></i>
                        <span>{{ game.rating }}</span>
                    </div>
                    <div class="new-fav">
                        <i v-if="favorites.has(game.id)" @click.stop="toggleFavorite(game.id)" class="pi pi-heart-fill"></i>
                        <i v-else @click.stop="toggleFavorite(game.id)" class="pi pi-heart"></i>
                    </div>
                </div>

                <div class="card-content">
                    <h3 class="game-title">{{ game.name }}</h3>

                    <div class="game-info">
                        <div class="info-item">
                            <i class="pi pi-calendar"></i>
                            <span>{{ game.release_date }}</span>
                        </div>
                    </div>

                    <div class="card-footer">
                        <span class="view-detail">Ver detalles</span>
                        <i class="pi pi-arrow-right"></i>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="showLoadMoreButton && !game_name" class="load-more-container">
            <Button label="Cargar más juegos" @click="loadMore" :loading="loading" class="load-more-btn" />
        </div>

        <div v-if="loading" class="loader">
            <span>{{ game_name ? 'Buscando juegos...' : 'Cargando más juegos...' }}</span>
        </div>
    </div>

</template>

<script>
import contenido from "./script_contenido.js";
import Button from "primevue/button"

export default {
    name: 'contenido',
    components: { Button },
    ...contenido
};
</script>

<style scoped src="./style_contenido.css"></style>