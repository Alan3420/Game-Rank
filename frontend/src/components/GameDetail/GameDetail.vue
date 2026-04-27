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

                    <!-- DESCRIPCIÓN -->
                    <div class="detail-card">
                        <div class="card-header">
                            <i class="pi pi-align-left"></i>
                            <h3>Descripción</h3>
                        </div>
                        <div class="detail-description"
                            v-html="game.description || '<em>Descripción no disponible.</em>'"></div>
                    </div>

                    <!-- CAPTURAS DE PANTALLA -->
                    <div v-if="game.screenshots.length" class="detail-card sc-card">

                        <!-- Visor principal con flechas -->
                        <div class="sc-viewer">
                            <img :src="game.screenshots[activeShot].image"
                                :alt="`${game.name} — captura ${activeShot + 1}`" class="sc-viewer__img" />
                            <button class="sc-arrow sc-arrow--l" @click="prevShot"
                                aria-label="Anterior">&#8249;</button>
                            <button class="sc-arrow sc-arrow--r" @click="nextShot"
                                aria-label="Siguiente">&#8250;</button>
                        </div>

                        <!-- Tira de miniaturas con scroll horizontal -->
                        <div class="sc-strip-wrap">
                            <div class="sc-strip">
                                <div v-for="(shot, i) in game.screenshots" :key="shot.id" class="sc-thumb"
                                    :class="{ 'sc-thumb--on': i === activeShot }" @click="activeShot = i">
                                    <img :src="shot.image" :alt="`Captura ${i + 1}`" />
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- COMENTARIOS -->
                    <div class="comments-block">

                        <!-- CABECERA -->
                        <div class="comments-block-header">
                            <div class="cb-title">
                                <i class="pi pi-comments"></i>
                                <h3>Comentarios</h3>
                                <span class="comment-count">{{ comments.length }}</span>
                            </div>
                        </div>

                        <!-- LISTA VACÍA -->
                        <div v-if="comments.length === 0" class="no-comments">
                            <div class="no-comments-icon">
                                <i class="pi pi-comment"></i>
                            </div>
                            <p>Aún no hay comentarios.</p>
                            <span>Sé el primero en dejar tu opinión sobre este juego.</span>
                        </div>

                        <!-- LISTA DE COMENTARIOS -->
                        <div v-else class="comments-list">
                            <div v-for="comment in comments" :key="comment.id_comment" class="comment-item">
                                <!-- Avatar -->
                                <div class="comment-avatar">
                                    <i class="pi pi-user"></i>
                                </div>

                                <!-- Contenido -->
                                <div class="comment-content">
                                    <div class="comment-top">
                                        <div class="comment-meta">
                                            <span class="comment-user">{{ comment.username }}</span>
                                            <span class="comment-dot"></span>
                                            <span class="comment-date">{{ formatDate(comment.date_of_comment) }}</span>
                                        </div>
                                        <button v-if="comment.id_user === data_user.id_user" class="comment-delete-btn"
                                            @click="delComment(comment.id_comment)" title="Eliminar comentario">
                                            <i class="pi pi-trash"></i>
                                        </button>
                                        <button v-if="comment.id_user === data_user.id_user" class="comment-edit-btn"
                                            @click="editar(comment)" title="Editar comentario">
                                            <i class="pi pi-pencil"></i>
                                        </button>
                                    </div>
                                    <p class="comment-body">{{ comment.description }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- SEPARADOR -->
                        <div class="comments-divider">
                            <span>Dejar un comentario</span>
                        </div>

                        <!-- FORMULARIO -->
                        <div class="add-comment-form">
                            <div class="comment-avatar comment-avatar-form">
                                <i class="pi pi-user"></i>
                            </div>
                            <div class="comment-input-wrap">
                                <textarea v-model="newComment" placeholder="Escribe tu opinión sobre este juego..."
                                    class="comment-textarea" maxlength="255" rows="3"></textarea>
                                <div class="comment-form-footer">
                                    <div class="form-footer-left">
                                        <span class="comment-char-hint" :class="{ active: newComment?.length > 0 }">
                                            {{ newComment?.length || 0 }} / 255 caracteres
                                        </span>
                                    </div>
                                    <div class="grp-botones">
                                        <!-- Botón cancelar, solo visible al editar -->
                                        <button v-if="editingId" class="comment-cancel-btn" @click="cancelarEdit()">
                                            Cancelar
                                        </button>
                                        <button class="comment-submit-btn" :class="{ editingId: editDescription }"
                                            @click="editingId ? updComment() : addComment()"
                                            :disabled="!newComment?.trim()">
                                            <i :class="editingId ? 'pi pi-check' : 'pi pi-send'"></i>
                                            {{ editingId ? 'Actualizar' : 'Publicar' }}
                                        </button>
                                    </div>
                                </div>
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