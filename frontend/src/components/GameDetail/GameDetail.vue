<template>
    <div class="game-detail-page">

        <!-- Loader -->
        <Loader v-if="loading" message="Loading game details..." full-height />

        <!-- Error -->
        <div v-else-if="!game" class="detail-error">
            <i class="pi pi-exclamation-circle"></i>
            <h2>{{ errorMessage || 'Could not load game details.' }}</h2>
            <Button icon="pi pi-arrow-left" label="Back" class="back-btn" @click="volver" />
        </div>

        <!-- Contenido principal -->
        <div v-else class="detail-layout">

            <!-- NAVEGACIÓN SUPERIOR -->
            <div class="detail-topbar">
                <Button icon="pi pi-arrow-left" label="Back" class="back-btn" @click="volver" />
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
                        <div class="stat-item" title="Metacritic Score">
                            <span class="stat-value">
                                <span v-if="game.metacritic" class="mc-badge" :class="claseMetacritic(game.metacritic)">{{ game.metacritic }}</span>
                                <span v-else class="mc-badge mc-na">N/A</span>
                            </span>
                            <span class="stat-label">Metacritic</span>
                        </div>

                        <div class="stat-sep"></div>

                        <div class="stat-item stat-item--community" title="Game Rank community average">
                            <span class="stat-value">
                                <i class="pi pi-star-fill"></i>
                                {{ communityAvg > 0 ? communityAvg : '—' }}
                            </span>
                            <span class="stat-label">Community</span>
                        </div>

                        <div class="stat-sep"></div>

                        <div class="stat-item">
                            <span class="stat-value">
                                <i class="pi pi-calendar"></i>
                                {{ formatearFecha(game.release_date) }}
                            </span>
                            <span class="stat-label">Release</span>
                        </div>

                        <template v-if="game.platforms?.length">
                            <div class="stat-sep"></div>
                            <div class="stat-item">
                                <span class="stat-value">
                                    <i class="pi pi-desktop"></i>
                                    {{ game.platforms.length }}
                                </span>
                                <span class="stat-label">{{ game.platforms.length !== 1 ? 'Platforms' : 'Platform' }}</span>
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
                        @click="alternarFavorito"
                        :title="isFavorite ? 'Remove from favorites' : 'Add to favorites'"
                    >
                        <i v-if="favoriteLoading" class="pi pi-spin pi-spinner"></i>
                        <i v-else :class="isFavorite ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                    </button>

                    <!-- Status button + dropdown wrapper.
                         Solo se muestra si el juego ya salio: no se puede
                         marcar como "jugando" o "completado" un juego que
                         todavia no esta a la venta. -->
                    <div v-if="juegoYaSalio" class="hero-status-wrap">
                        <button
                            class="hero-status-btn"
                            :class="{ 'has-status': gameStatus }"
                            :style="gameStatus ? { '--status-c': STATUS_META[gameStatus]?.color, '--status-bg': STATUS_META[gameStatus]?.solidBg, color: STATUS_META[gameStatus]?.solidText } : {}"
                            @click.stop="showStatusModal = !showStatusModal"
                            :title="gameStatus ? `Status: ${STATUS_META[gameStatus]?.label}` : 'Set game status'"
                        >
                            <i :class="'pi ' + (gameStatus ? STATUS_META[gameStatus]?.icon : 'pi-bookmark')"></i>
                            <span>{{ gameStatus ? STATUS_META[gameStatus]?.label : 'Status' }}</span>
                        </button>

                        <!-- Dropdown de estado -->
                        <div v-if="showStatusModal && game" class="hero-status-dropdown-wrap">
                            <GameStatusDropdown
                                :game-id="game.id"
                                :current-status="gameStatus"
                                @close="showStatusModal = false"
                                @update:status="manejarActualizacionEstado"
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
                            <h3>Description</h3>
                        </div>
                        <div class="detail-description"
                            v-html="descripcionSanitizada || '<em>Description not available.</em>'"></div>
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
                                :alt="`${game.name} — screenshot ${activeShot + 1}`" class="sc-viewer__img" />
                            <button class="sc-arrow sc-arrow--l" @click="mediaAnterior"
                                aria-label="Previous">&#8249;</button>
                            <button class="sc-arrow sc-arrow--r" @click="mediaSiguiente"
                                aria-label="Next">&#8250;</button>
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
                                    <img v-else :src="item.url" :alt="`Screenshot ${i + 1}`" />
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- LOGROS -->
                    <div v-if="logros.length" class="logros-band">
                        <div class="logros-band__header">
                            <div class="logros-band__title">
                                <i class="pi pi-trophy"></i>
                                <h3>Achievements</h3>
                                <span class="logros-band__count">{{ logros.length }}</span>
                            </div>
                            <div class="logros-leyenda">
                                <span class="rareza-dot rareza-raro"></span><span>Rare</span>
                                <span class="rareza-dot rareza-infrecuente"></span><span>Uncommon</span>
                                <span class="rareza-dot rareza-comun"></span><span>Common</span>
                            </div>
                        </div>
                        <div class="logros-strip">
                            <div
                                v-for="logro in logros"
                                :key="logro.id"
                                class="logro-tile"
                                :class="logroRareza(logro.percent)"
                                :title="logro.description"
                            >
                                <div class="logro-tile__img">
                                    <GameImage v-if="logro.image" :src="logro.image" :alt="logro.name" />
                                    <i v-else class="pi pi-trophy"></i>
                                </div>
                                <div class="logro-tile__info">
                                    <span class="logro-tile__name">{{ logro.name }}</span>
                                    <span v-if="logro.percent !== null" class="logro-tile__pct">{{ logro.percent.toFixed(1) }}%</span>
                                </div>
                                <div class="logro-tile__rareza-bar">
                                    <div class="logro-tile__rareza-fill" :style="{ width: Math.min(logro.percent ?? 0, 100) + '%' }"></div>
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
                                <h3>Comments</h3>
                                <span class="comment-count">{{ totalComments }}</span>
                            </div>
                        </div>

                        <!-- LISTA VACÍA -->
                        <div v-if="comments.length === 0" class="no-comments">
                            <div class="no-comments-icon">
                                <i class="pi pi-comment"></i>
                            </div>
                            <p>No comments yet.</p>
                            <span>Be the first to share your opinion about this game.</span>
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
                                            <span v-if="comment.nickname" class="comment-nickname">@{{ comment.nickname }}</span>
                                            <span class="comment-dot"></span>
                                            <span class="comment-date">{{ formatearFecha(comment.date_of_comment) }}</span>
                                            <span v-if="comment.date_of_update" class="comment-edited">
                                                <span class="comment-dot"></span>
                                                <i class="pi pi-pencil"></i>
                                                edited on {{ formatearFecha(comment.date_of_update) }}
                                            </span>
                                        </div>
                                        <button v-if="comment.id_user === data_user.id_user || data_user?.role === 'admin'" class="comment-delete-btn"
                                            @click="eliminarMiComentario(comment.id_comment)" title="Delete comment">
                                            <i class="pi pi-trash"></i>
                                        </button>
                                        <button v-if="comment.id_user === data_user.id_user" class="comment-edit-btn"
                                            @click="iniciarEdicionComentario(comment)" title="Edit comment">
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

                        <!-- CARGAR MÁS -->
                        <div v-if="hasMoreComments || loadingMore" class="load-more-wrap">
                            <button class="load-more-btn" @click="cargarMasComentarios" :disabled="loadingMore">
                                <i v-if="loadingMore" class="pi pi-spin pi-spinner"></i>
                                <i v-else class="pi pi-chevron-down"></i>
                                {{ loadingMore ? 'Loading...' : `Load more (${totalComments - comments.length} remaining)` }}
                            </button>
                        </div>

                        <!-- SEPARADOR -->
                        <div class="comments-divider">
                            <span>{{ editingId ? 'Edit your comment' : 'Leave a comment' }}</span>
                        </div>

                        <!-- FORMULARIO -->
                        <div class="add-comment-form" :class="{ 'is-disabled': formularioDeshabilitado }">
                            <div class="comment-avatar comment-avatar-form">
                                <i class="pi pi-user"></i>
                            </div>
                            <div class="comment-input-wrap">
                                <div class="rating-input" @mouseleave="formHover = 0">
                                    <span class="rating-input-label">Your rating</span>
                                    <div class="rating-input-stars">
                                        <button v-for="n in 5" :key="n" type="button" class="rating-star-btn"
                                            :class="{ 'is-active': n <= (formHover || formRating) }"
                                            @click="establecerCalificacionFormulario(n)" @mouseenter="formHover = n"
                                            :disabled="formularioDeshabilitado"
                                            :title="`${n} de 5`">
                                            <i class="pi pi-star-fill"></i>
                                        </button>
                                    </div>
                                    <span class="rating-input-value">
                                        {{ (formHover || formRating) ? `${formHover || formRating}/5` : 'Not rated' }}
                                    </span>
                                </div>
                                <textarea v-model="newComment" placeholder="Write your opinion about this game..."
                                    class="comment-textarea" maxlength="255" rows="3"
                                    :disabled="formularioDeshabilitado"></textarea>
                                <div class="comment-form-footer">
                                    <div class="form-footer-left">
                                        <span class="comment-char-hint" :class="{ active: newComment?.length > 0 }">
                                            {{ newComment?.length || 0 }} / 255 characters
                                        </span>
                                    </div>
                                    <div class="grp-botones">
                                        <!-- Botón cancelar, solo visible al editar -->
                                        <button v-if="editingId" class="comment-cancel-btn" @click="cancelarEdicionComentario()">
                                            Cancel
                                        </button>
                                        <button class="comment-submit-btn" :class="{ editingId: editDescription }"
                                            @click="editingId ? actualizarMiComentario() : publicarComentario()"
                                            :disabled="formularioDeshabilitado || !newComment?.trim() || !formRating">
                                            <i :class="editingId ? 'pi pi-check' : 'pi pi-send'"></i>
                                            {{ editingId ? 'Update' : 'Publish' }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- MÁS DE ESTA SAGA -->
                    <div v-if="juegosSaga.length" class="detail-card sugeridos-card">
                        <div class="card-header">
                            <i class="pi pi-th-large"></i>
                            <h3>More from this series</h3>
                        </div>
                        <div class="sugeridos-grid">
                            <GameCard
                                v-for="(juego, i) in juegosSaga"
                                :key="juego.id"
                                :game="juego"
                                :index="i"
                                @click="irAlJuego(juego.id)"
                            />
                        </div>
                    </div>

                </div>

                <!-- SIDEBAR -->
                <aside class="detail-aside">

                    <!-- Plataformas -->
                    <div class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-desktop"></i>
                            <h3>Platforms</h3>
                        </div>
                        <div class="tag-list">
                            <span v-if="!game.platforms?.length" class="tag empty">No information</span>
                            <span v-for="platform in game.platforms" :key="platform.id" class="tag">{{ platform.name
                            }}</span>
                        </div>
                    </div>

                    <!-- Equipo creativo -->
                    <div v-if="game.team?.length" class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-id-card"></i>
                            <h3>Creative Team</h3>
                        </div>
                        <div class="team-list">
                            <div v-for="member in game.team" :key="member.id" class="team-item">
                                <div class="team-avatar">
                                    <GameImage v-if="member.image" :src="member.image" :alt="member.name" />
                                    <i v-else class="pi pi-user"></i>
                                </div>
                                <div class="team-info">
                                    <span class="team-name">{{ member.name }}</span>
                                    <span class="team-roles">{{ member.roles.join(', ') || 'Team' }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DLCs y expansiones -->
                    <div v-if="adiciones.length" class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-plus-circle"></i>
                            <h3>DLCs &amp; Expansions</h3>
                        </div>
                        <div class="adiciones-list">
                            <div
                                v-for="dlc in adiciones"
                                :key="dlc.id"
                                class="adicion-item"
                                @click="irAlJuego(dlc.id)"
                            >
                                <div class="adicion-thumb">
                                    <GameImage v-if="dlc.imge_url" :src="dlc.imge_url" :alt="dlc.name" />
                                    <i v-else class="pi pi-image"></i>
                                </div>
                                <div class="adicion-info">
                                    <span class="adicion-name">{{ dlc.name }}</span>
                                    <span class="adicion-date">{{ formatearFecha(dlc.release_date) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Estudios -->
                    <div class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-users"></i>
                            <h3>Studios</h3>
                        </div>
                        <div class="dev-list">
                            <div v-if="!game.developers?.length" class="tag empty">No information</div>
                            <div v-for="dev in game.developers" :key="dev.id" class="dev-item">
                                <div class="dev-avatar">
                                    <GameImage v-if="dev.image" :src="dev.image" :alt="dev.name" />
                                    <i v-else class="pi pi-building"></i>
                                </div>
                                <div class="dev-info">
                                    <span class="dev-name">{{ dev.name }}</span>
                                    <span class="dev-label">Studio</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Metadatos rápidos -->
                    <div class="detail-card sidebar-card meta-card">
                        <div class="card-header">
                            <i class="pi pi-info-circle"></i>
                            <h3>Information</h3>
                        </div>
                        <ul class="meta-list">
                            <li>
                                <span class="meta-label">Metacritic</span>
                                <span class="meta-value">
                                    <span v-if="game.metacritic" class="mc-badge" :class="claseMetacritic(game.metacritic)">{{ game.metacritic }}</span>
                                    <span v-else>—</span>
                                </span>
                            </li>
                            <li>
                                <span class="meta-label">Community score</span>
                                <span class="meta-value">
                                    <i class="pi pi-star-fill meta-star meta-star-community"></i>
                                    {{ communityAvg > 0 ? communityAvg : '0' }}
                                </span>
                            </li>
                            <li>
                                <span class="meta-label">Release</span>
                                <span class="meta-value">{{ formatearFecha(game.release_date) }}</span>
                            </li>
                            <li v-if="game.platforms?.length">
                                <span class="meta-label">Platforms</span>
                                <span class="meta-value">{{ game.platforms.length }}</span>
                            </li>
                            <li v-if="game.developers?.length">
                                <span class="meta-label">Team</span>
                                <span class="meta-value">{{ game.developers.length }} studio{{ game.developers.length
                                    !== 1 ? 's' : '' }}</span>
                            </li>
                        </ul>
                    </div>
                    
                    <!-- Dónde comprar -->
                    <div v-if="game.stores?.length" class="detail-card sidebar-card">
                        <div class="card-header">
                            <i class="pi pi-shopping-cart"></i>
                            <h3>Where to buy</h3>
                        </div>
                        <div class="store-list">
                            <button
                                v-for="store in game.stores"
                                :key="store.id"
                                class="store-btn"
                                @click="abrirEnlaceExterno(store.url, store.name)"
                            >
                                <i :class="'pi ' + obtenerIconoDeTienda(store.slug)"></i>
                                <span>{{ store.name }}</span>
                                <i class="pi pi-external-link store-btn__ext"></i>
                            </button>
                        </div>
                    </div>


                </aside>
            </section>

        </div>
    </div>

    <!-- Modal aviso enlace externo -->
    <div v-if="externalLink.open" class="ext-modal-overlay" @click.self="cancelarEnlaceExterno">
        <div class="ext-modal" role="dialog" aria-modal="true">
            <div class="ext-modal__icon">
                <i class="pi pi-external-link"></i>
            </div>
            <h2 class="ext-modal__title">Leaving GameRank</h2>
            <p class="ext-modal__body">
                You are about to visit <strong>{{ externalLink.storeName }}</strong>,
                an external site not controlled by GameRank.
                Do you want to continue?
            </p>
            <div class="ext-modal__actions">
                <button class="ext-modal__btn ext-modal__btn--cancel" @click="cancelarEnlaceExterno">
                    Cancel
                </button>
                <button class="ext-modal__btn ext-modal__btn--confirm" @click="confirmarEnlaceExterno">
                    <i class="pi pi-external-link"></i>
                    Continue
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import jsDetalles from "./script_GameDetail.js";
import Button from 'primevue/button';
import Loader from '../Loader/Loader.vue';
import GameImage from '../Image/GameImage.vue';
import GameStatusDropdown from '../Cards/GameStatusDropdown.vue';
import GameCard from '../Cards/GameCard.vue';
export default {
    name: 'GameDetail',
    components: { Button, Loader, GameImage, GameStatusDropdown, GameCard },
    mixins: [jsDetalles]
};
</script>

<style scoped src="./styles_GameDetail.css"></style>