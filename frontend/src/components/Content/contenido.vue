<template>


    <div class="content-overview">
        <div class="header">
            <h1>Contenido Principal</h1>

            <div class="conten_view">
                <div class="buscar_contenido">
                    <div class="google-search">
                        <InputText class="google-input" v-model="game_name" placeholder="Nombre del juego..." />
                        <Button icon="pi pi-search" class="google-btn" @click="getContentCard" />
                    </div>
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
    import "./style_contenido.css";
    import InputText from "primevue/inputtext"
    import Button from "primevue/button"

    export default {
        name: 'contenido',
        components: {InputText, Button},
        ...contenido
    };
</script>