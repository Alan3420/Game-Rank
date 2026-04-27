<template>
    <div class="game-detail-page">

        <!-- Loader -->
        <div v-if="loading" class="detail-loader">
            <div class="loader-spinner">
                <i class="pi pi-spin pi-spinner"></i>
            </div>
            <span>Cargando detalles del juego...</span>
        </div>

        <!-- Error -->
        <div v-else-if="!game" class="detail-error">
            <i class="pi pi-exclamation-circle"></i>
            <h2>{{ errorMessage || 'No se pudieron cargar los detalles del juego.' }}</h2>
            <Button icon="pi pi-arrow-left" label="Volver" class="back-btn" @click="goBack" />
        </div>

        <!-- Contenido principal -->
        <div v-else class="detail-layout">

            <!-- NAVEGACIÓN SUPERIOR -->
            <div class="detail-topbar">
                <Button icon="pi pi-arrow-left" label="Volver" class="back-btn" @click="goBack" />
                <span class="breadcrumb-hint">
                    <i class="pi pi-home"></i>
                    <i class="pi pi-angle-right"></i>
                    <span>{{ game.name }}</span>
                </span>
            </div>

            <!-- HERO BANNER -->
            <section class="detail-hero" :style="bannerStyle">
                <div class="hero-gradient"></div>
                <div class="hero-content">
                    <span class="detail-category">
                        <i class="pi pi-gamepad"></i>
                        Videojuego
                    </span>
                    <h1>{{ game.name }}</h1>
                    <div class="detail-stats">
                        <div class="stat-pill">
                            <i class="pi pi-star-fill"></i>
                            <span>{{ game.rating ?? 'N/A' }}</span>
                        </div>
                        <div class="stat-pill">
                            <i class="pi pi-calendar"></i>
                            <span>{{ formatDate(game.release_date) }}</span>
                        </div>
                        <div v-if="game.platforms?.length" class="stat-pill">
                            <i class="pi pi-desktop"></i>
                            <span>{{ game.platforms.length }} plataforma{{ game.platforms.length !== 1 ? 's' : ''
                                }}</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- CUERPO: 2 columnas -->
            <section class="detail-body">

                <!-- COLUMNA PRINCIPAL -->
                <div class="detail-main">

                    <!-- CAPTURAS -->
                    <div v-if="game.screenshots?.length" class="detail-card">
                        <div class="card-header">
                            <i class="pi pi-images"></i>
                            <h3>Capturas de pantalla</h3>
                        </div>
                        <div class="screenshots-grid">
                            <img v-for="shot in game.screenshots" :key="shot.id" :src="shot.image" :alt="game.name"
                                class="screenshot-img" />
                        </div>
                    </div>

                    <!-- DESCRIPCIÓN -->
                    <div class="detail-card">
                        <div class="card-header">
                            <i class="pi pi-align-left"></i>
                            <h3>Descripción</h3>
                        </div>
                        <div class="detail-description"
                            v-html="game.description || '<em>Descripción no disponible.</em>'"></div>
                    </div>

                    <!-- COMENTARIOS -->
                    <div class="detail-card comments-section">
                        <div class="card-header comments-header">
                            <div class="header-left">
                                <i class="pi pi-comments"></i>
                                <h3>Comentarios</h3>
                                <span class="comment-count">{{ comments.length }}</span>
                            </div>
                        </div>

                        <div v-if="comments.length === 0" class="no-comments">
                            <i class="pi pi-inbox"></i>
                            <p>Aún no hay comentarios para este juego.</p>
                        </div>

                        <div v-else class="comments-list">
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
                        </div>

                        <!-- SECCIÓN PARA AGREGAR COMENTARIO -->
                        <div class="add-comment-section">
                            <div class="add-comment-header">
                                <i class="pi pi-plus-circle"></i>
                                <span>Agregar comentario</span>
                            </div>
                            <div class="add-comment-form">
                                <textarea v-model="newComment" placeholder="Escribe tu comentario aquí..."
                                    class="comment-input" rows="4"></textarea>
                                <button @click="addComment" class="send-comment-btn" :disabled="!newComment?.trim()">
                                    <i class="pi pi-send"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                </div>

                <!-- SIDEBAR -->
                <aside class="detail-aside">

                    <!-- Plataformas -->
                    <div class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-desktop"></i>
                            <h3>Plataformas</h3>
                        </div>
                        <div class="tag-list">
                            <span v-if="!game.platforms?.length" class="tag empty">Sin información</span>
                            <span v-for="platform in game.platforms" :key="platform.id" class="tag">{{ platform.name
                                }}</span>
                        </div>
                    </div>

                    <!-- Desarrolladores -->
                    <div class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-users"></i>
                            <h3>Desarrolladores</h3>
                        </div>
                        <div class="dev-list">
                            <div v-if="!game.developers?.length" class="tag empty">Sin información</div>
                            <div v-for="dev in game.developers" :key="dev.id" class="dev-item">
                                <div class="dev-avatar">
                                    <img v-if="dev.image" :src="dev.image" :alt="dev.name" />
                                    <i v-else class="pi pi-building"></i>
                                </div>
                                <div class="dev-info">
                                    <span class="dev-name">{{ dev.name }}</span>
                                    <span class="dev-label">Desarrollador</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Metadatos rápidos -->
                    <div class="detail-card sidebar-card meta-card">
                        <div class="card-header">
                            <i class="pi pi-info-circle"></i>
                            <h3>Información</h3>
                        </div>
                        <ul class="meta-list">
                            <li>
                                <span class="meta-label">Puntuación</span>
                                <span class="meta-value">
                                    <i class="pi pi-star-fill meta-star"></i>
                                    {{ game.rating ?? 'N/A' }}
                                </span>
                            </li>
                            <li>
                                <span class="meta-label">Lanzamiento</span>
                                <span class="meta-value">{{ formatDate(game.release_date) }}</span>
                            </li>
                            <li v-if="game.platforms?.length">
                                <span class="meta-label">Plataformas</span>
                                <span class="meta-value">{{ game.platforms.length }}</span>
                            </li>
                            <li v-if="game.developers?.length">
                                <span class="meta-label">Equipo</span>
                                <span class="meta-value">{{ game.developers.length }} estudio{{ game.developers.length
                                    !== 1 ? 's' : '' }}</span>
                            </li>
                        </ul>
                    </div>

                </aside>
            </section>

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