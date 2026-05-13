<template>
    <div class="game-detail-page">

        <!-- Loader -->
        <Loader v-if="loading" message="Cargando detalles del juego..." full-height />

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
            <section class="detail-hero">
                <GameImage v-if="game.imge_url" :src="game.imge_url" :alt="game.name" class="hero-image" />
                <div class="hero-content">
                    <div class="detail-categories">
                        <span
                            v-for="genre in game.genres"
                            :key="genre.id"
                            class="detail-category"
                        >{{ genre.name }}</span>
                    </div>

                    <h1>{{ game.name }}</h1>

                    <div class="detail-stats">
                        <div class="stat-item" title="Puntuación oficial RAWG">
                            <span class="stat-value">
                                <i class="pi pi-star-fill"></i>
                                {{ game.rating ?? 'N/A' }}
                            </span>
                            <span class="stat-label">RAWG</span>
                        </div>

                        <div class="stat-sep"></div>

                        <div class="stat-item stat-item--community" title="Media de la comunidad de Game Rank">
                            <span class="stat-value">
                                <i class="pi pi-star-fill"></i>
                                {{ communityAvg > 0 ? communityAvg : '—' }}
                            </span>
                            <span class="stat-label">Comunidad</span>
                        </div>

                        <div class="stat-sep"></div>

                        <div class="stat-item">
                            <span class="stat-value">
                                <i class="pi pi-calendar"></i>
                                {{ formatDate(game.release_date) }}
                            </span>
                            <span class="stat-label">Lanzamiento</span>
                        </div>

                        <template v-if="game.platforms?.length">
                            <div class="stat-sep"></div>
                            <div class="stat-item">
                                <span class="stat-value">
                                    <i class="pi pi-desktop"></i>
                                    {{ game.platforms.length }}
                                </span>
                                <span class="stat-label">{{ game.platforms.length !== 1 ? 'Plataformas' : 'Plataforma' }}</span>
                            </div>
                        </template>
                    </div>
                </div>
                <!-- Botones del hero: favorito + estado -->
                <div class="hero-action-group">
                    <button
                        class="hero-fav-btn"
                        :class="{ 'is-fav': isFavorite, 'is-loading': favoriteLoading }"
                        :disabled="favoriteLoading"
                        @click="toggleFavorite"
                        :title="isFavorite ? 'Quitar de favoritos' : 'Añadir a favoritos'"
                    >
                        <i v-if="favoriteLoading" class="pi pi-spin pi-spinner"></i>
                        <i v-else :class="isFavorite ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                    </button>

                    <!-- Status button + dropdown wrapper -->
                    <div class="hero-status-wrap">
                        <button
                            class="hero-status-btn"
                            :class="{ 'has-status': gameStatus }"
                            :style="gameStatus ? { '--status-c': STATUS_META[gameStatus]?.color, '--status-bg': STATUS_META[gameStatus]?.solidBg, color: STATUS_META[gameStatus]?.solidText } : {}"
                            @click.stop="showStatusModal = !showStatusModal"
                            :title="gameStatus ? `Estado: ${STATUS_META[gameStatus]?.label}` : 'Marcar estado del juego'"
                        >
                            <i :class="'pi ' + (gameStatus ? STATUS_META[gameStatus]?.icon : 'pi-bookmark')"></i>
                            <span>{{ gameStatus ? STATUS_META[gameStatus]?.label : 'Estado' }}</span>
                        </button>

                        <!-- Dropdown de estado -->
                        <div v-if="showStatusModal && game" class="hero-status-dropdown-wrap">
                            <GameStatusDropdown
                                :game-id="game.id"
                                :current-status="gameStatus"
                                @close="showStatusModal = false"
                                @update:status="handleStatusUpdate"
                            />
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

                    <!-- Area de fotos y videos  -->
                    <div v-if="game.screenshots?.length || game.movies?.length" class="detail-card sc-card">

                        <!-- Visor principal -->
                        <div class="sc-viewer">
                            <!-- Si el item activo es un vídeo -->
                            <video v-if="mediaItems[activeShot]?.type === 'video'" :src="mediaItems[activeShot].url"
                                class="sc-viewer__img" :poster="mediaItems[activeShot].preview" controls muted loop></video>
                            <!-- Si el item activo es una imagen -->
                            <img v-else :src="mediaItems[activeShot]?.url"
                                :alt="`${game.name} — captura ${activeShot + 1}`" class="sc-viewer__img" />
                            <button class="sc-arrow sc-arrow--l" @click="prevShot"
                                aria-label="Anterior">&#8249;</button>
                            <button class="sc-arrow sc-arrow--r" @click="nextShot"
                                aria-label="Siguiente">&#8250;</button>
                        </div>

                        <!-- Tira de miniaturas -->
                        <div class="sc-strip-wrap">
                            <div class="sc-strip">
                                <div v-for="(item, i) in mediaItems" :key="i" class="sc-thumb"
                                    :class="{ 'sc-thumb--on': i === activeShot }" @click="activeShot = i">
                                    <!-- Miniatura vídeo -->
                                    <div v-if="item.type === 'video'" class="sc-thumb__video">
                                        <video  :poster="item.preview"></video>
                                    </div>
                                    <!-- Miniatura imagen -->
                                    <img v-else :src="item.url" :alt="`Captura ${i + 1}`" />
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
                                            <span v-if="comment.date_of_update" class="comment-edited">
                                                <span class="comment-dot"></span>
                                                <i class="pi pi-pencil"></i>
                                                editado el {{ formatDate(comment.date_of_update) }}
                                            </span>
                                        </div>
                                        <button v-if="comment.id_user === data_user.id_user || data_user?.role === 'admin'" class="comment-delete-btn"
                                            @click="delComment(comment.id_comment)" title="Eliminar comentario">
                                            <i class="pi pi-trash"></i>
                                        </button>
                                        <button v-if="comment.id_user === data_user.id_user" class="comment-edit-btn"
                                            @click="editar(comment)" title="Editar comentario">
                                            <i class="pi pi-pencil"></i>
                                        </button>
                                    </div>
                                    <div v-if="comment.rating" class="comment-stars" :title="`${comment.rating} de 5`">
                                        <i v-for="n in 5" :key="n" class="pi"
                                           :class="n <= comment.rating ? 'pi-star-fill' : 'pi-star'"></i>
                                        <span class="comment-stars-value">{{ comment.rating }}/5</span>
                                    </div>
                                    <p class="comment-body">{{ comment.description }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- SEPARADOR -->
                        <div class="comments-divider">
                            <span>{{ editingId ? 'Editar tu comentario' : 'Dejar un comentario' }}</span>
                        </div>

                        <!-- FORMULARIO -->
                        <div class="add-comment-form" :class="{ 'is-disabled': formDisabled }">
                            <div class="comment-avatar comment-avatar-form">
                                <i class="pi pi-user"></i>
                            </div>
                            <div class="comment-input-wrap">
                                <div class="rating-input" @mouseleave="formHover = 0">
                                    <span class="rating-input-label">Tu valoración</span>
                                    <div class="rating-input-stars">
                                        <button v-for="n in 5" :key="n" type="button" class="rating-star-btn"
                                            :class="{ 'is-active': n <= (formHover || formRating) }"
                                            @click="setFormRating(n)" @mouseenter="formHover = n"
                                            :disabled="formDisabled"
                                            :title="`${n} de 5`">
                                            <i class="pi pi-star-fill"></i>
                                        </button>
                                    </div>
                                    <span class="rating-input-value">
                                        {{ (formHover || formRating) ? `${formHover || formRating}/5` : 'Sin votar' }}
                                    </span>
                                </div>
                                <textarea v-model="newComment" placeholder="Escribe tu opinión sobre este juego..."
                                    class="comment-textarea" maxlength="255" rows="3"
                                    :disabled="formDisabled"></textarea>
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
                                            :disabled="formDisabled || !newComment?.trim() || !formRating">
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
                                    <GameImage v-if="dev.image" :src="dev.image" :alt="dev.name" />
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
                                <span class="meta-label">Puntuación oficial (RAWG)</span>
                                <span class="meta-value">
                                    <i class="pi pi-star-fill meta-star"></i>
                                    {{ game.rating ?? 'N/A' }}
                                </span>
                            </li>
                            <li>
                                <span class="meta-label">Puntuación comunidad</span>
                                <span class="meta-value">
                                    <i class="pi pi-star-fill meta-star meta-star-community"></i>
                                    {{ communityAvg > 0 ? communityAvg : '0' }}
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
import Loader from '../Loader/Loader.vue';
import GameImage from '../Image/GameImage.vue';
import GameStatusDropdown from '../Cards/GameStatusDropdown.vue';
export default {
    name: 'GameDetail',
    components: { Button, Loader, GameImage, GameStatusDropdown },
    mixins: [jsDetalles]
};
</script>

<style scoped src="./styles_GameDetail.css"></style>