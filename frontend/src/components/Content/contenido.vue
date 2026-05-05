<template>


    <div class="content-overview">
        <div class="catalogo-header">
            <div class="catalogo-header-texto">
                <span class="catalogo-eyebrow">
                    <i class="pi pi-th-large"></i>
                    Catálogo de juegos
                </span>
                <h1>Explora nuestra colección</h1>
                <p>Encuentra tu próximo juego favorito entre cientos de títulos</p>
            </div>

            <div class="catalogo-buscador">
                <div class="buscador-wrap">
                    <i class="pi pi-search buscador-icono"></i>
                    <InputText class="buscador-input" v-model="game_name" placeholder="Buscar un juego..."
                        @keyup.enter="getContentCard" />
                    <Button label="Buscar" class="buscador-btn" @click="getContentCard" />
                </div>
            </div>
        </div>

        <!-- Card del juego -->
        <div class="card_content">
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

        <div v-if="showLoadMoreButton" class="load-more-container">
            <Button label="Cargar más juegos" @click="loadMore" :loading="loading" class="load-more-btn" />
        </div>

        <div v-if="loading" class="loader">
            <span>Cargando más juegos...</span>
        </div>
    </div>

</template>

<script>
import contenido from "./script_contenido.js";
import InputText from "primevue/inputtext"
import Button from "primevue/button"

export default {
    name: 'contenido',
    components: { InputText, Button },
    ...contenido
};
</script>

<style scoped src="./style_contenido.css"></style>