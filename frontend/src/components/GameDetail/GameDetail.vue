<template>
    <div class="game-detail-page">
        <div v-if="loading" class="detail-loader">
            <span>Cargando detalles del juego...</span>
        </div>

        <div v-else-if="game" class="detail-layout">
            <section class="detail-banner" :style="bannerStyle">
                <div class="detail-banner-overlay">
                    <div class="detail-banner-content">
                        <span class="detail-category">Detalle del juego</span>
                        <h1>{{ game.name }}</h1>
                        <div class="detail-stats">
                            <div><i class="pi pi-star-fill"></i> {{ game.rating ?? 'N/A' }}</div>
                            <div><i class="pi pi-calendar"></i> {{ formatDate(game.release_date) }}</div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="detail-body">
                <div class="detail-card screenshots-card">
                    <h3>Capturas de pantalla</h3>
                    <div class="screenshots-grid">
                        <img v-for="shot in game.screenshots" :key="shot.id" :src="shot.image" :alt="game.name"
                            class="screenshot-img" />
                    </div>
                </div>
                <div class="detail-card detail-description-card">
                    <h2>Descripción</h2>
                    <div class="detail-description" v-html="game.description || '<em>Descripción no disponible.</em>'">
                    </div>
                </div>

                <aside class="detail-aside">
                    <div class="detail-card">
                        <h3>Plataformas</h3>
                        <div class="tag-list">
                            <span v-if="!game.platforms?.length" class="tag empty">Sin información</span>
                            <span v-for="platform in game.platforms" :key="platform.id" class="tag">{{ platform.name
                            }}</span>
                        </div>
                    </div>

                    <div class="detail-card">
                        <h3>Desarrolladores</h3>
                        <div class="dev-list">
                            <div v-if="!game.developers?.length" class="tag empty">Sin información</div>
                            <div v-for="dev in game.developers" :key="dev.id" class="dev-item">
                                <img v-if="dev.image" :src="dev.image" :alt="dev.name" />
                                <span>{{ dev.name }}</span>
                            </div>
                        </div>
                    </div>
                </aside>
            </section>

            <!-- Aqui van los comentarios -->
            <section class="detail-card comments-section">
                <h2>Comentarios <span class="comment-count">{{ comments.length }}</span></h2>

                <div v-if="comments.length === 0" class="no-comments">
                    <i class="pi pi-comments"></i>
                    <span>Todavía no hay comentarios para este juego</span>
                </div>

                <div v-for="comment in comments" :key="comment.id_comment" class="comment-item">
                    <div class="comment-avatar">
                        <i class="pi pi-user"></i>
                    </div>
                    <div class="comment-content">
                        <div class="comment-header">
                            <span class="comment-user">{{ comment.username }}</span>
                            <span class="comment-date">{{ formatDate(comment.date_of_comment) }}</span>
                        </div>
                        <p class="comment-body">{{ comment.description }}</p>
                    </div>
                </div>
            </section>

            <div class="detail-actions">
                <Button icon="pi pi-arrow-left" class="back-btn" @click="goBack" />
            </div>


        </div>

        <div v-else class="detail-error">
            <h2>{{ errorMessage || 'No se pudieron cargar los detalles del juego.' }}</h2>
            <Button icon="pi pi-arrow-left" class="back-btn" @click="goBack" />
        </div>


    </div>
</template>

<script>
import jsDetalles from "./script_GameDetail.js";
import Button from 'primevue/button';

export default {
    name: 'GameDetail',
    components: { Button },
    mixins: [jsDetalles]
};
</script>

<style scoped src="./styles_GameDetail.css"></style>