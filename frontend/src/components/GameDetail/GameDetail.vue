<template>
    <div class="game-detail-page">

        <!-- Skeleton: misma estructura que la ficha (carta + columna) -->
        <div v-if="loading" class="gd-shell" aria-busy="true">
            <div class="gd-topbar">
                <Skeleton width="84px" height="36px" radius="10px" />
            </div>
            <div class="gd-grid">
                <div class="gd-card-col">
                    <div class="gd-card gd-card--skeleton">
                        <div class="gd-card__face">
                            <div class="gd-card__band">
                                <Skeleton width="70%" height="1.6rem" radius="6px" />
                                <Skeleton width="44px" height="1.6rem" radius="6px" />
                            </div>
                            <Skeleton class="gd-card__art-skel" radius="10px" />
                            <Skeleton width="55%" height="0.85rem" />
                            <div class="gd-card__stats">
                                <Skeleton v-for="n in 3" :key="n" height="3.2rem" radius="8px" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="gd-main-col">
                    <div class="gd-panel gd-skel-stack">
                        <Skeleton width="120px" height="1rem" />
                        <Skeleton width="100%" height="2.75rem" radius="10px" />
                    </div>
                    <div class="gd-panel gd-skel-stack">
                        <Skeleton width="90px" height="1rem" />
                        <Skeleton width="100%" height="0.85rem" />
                        <Skeleton width="100%" height="0.85rem" />
                        <Skeleton width="80%" height="0.85rem" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Error -->
        <div v-else-if="!game" class="gd-error">
            <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
            <h2>{{ errorMessage || 'Could not load game details.' }}</h2>
            <button type="button" class="gd-btn gd-btn--ghost" @click="volver">
                <i aria-hidden="true" class="pi pi-arrow-left"></i>
                Back
            </button>
        </div>

        <!-- Ficha -->
        <div v-else class="gd-shell">

            <div class="gd-topbar">
                <button type="button" class="gd-btn gd-btn--ghost gd-btn--sm" @click="volver">
                    <i aria-hidden="true" class="pi pi-arrow-left"></i>
                    Back
                </button>
            </div>

            <div class="gd-grid" :class="gameStatus && isFavorite ? `gd-frame--${gameStatus}` : ''">

                <!-- ── LA CARTA ── -->
                <div class="gd-card-col">
                    <article class="gd-card" aria-labelledby="gd-title">
                        <div class="gd-card__face">
                            <header class="gd-card__band">
                                <h1 id="gd-title" class="gd-card__name">{{ game.name }}</h1>
                                <span
                                    class="gd-card__mc"
                                    :class="game.metacritic ? claseMetacritic(game.metacritic) : 'mc-na'"
                                    :title="game.metacritic ? 'Metacritic score' : 'No Metacritic score'"
                                >
                                    <span class="gd-card__mc-label">MC</span>
                                    <span class="gd-card__mc-value">{{ game.metacritic ?? '—' }}</span>
                                    <span class="sr-only">Metacritic score</span>
                                </span>
                            </header>

                            <div class="gd-card__art">
                                <GameImage :src="game.imge_url" :alt="game.name" eager width="1280" height="960" />
                                <span v-if="holoKey" :key="holoKey" class="gd-card__sweep" aria-hidden="true"></span>
                            </div>

                            <p v-if="game.genres?.length" class="gd-card__type">
                                {{ game.genres.map(function (g) { return g.name; }).join(', ') }}
                            </p>

                            <dl class="gd-card__stats">
                                <div class="gd-stat">
                                    <dt>Community</dt>
                                    <dd>
                                        <i aria-hidden="true" class="pi pi-star-fill"></i>
                                        {{ communityAvg > 0 ? communityAvg : '—' }}
                                    </dd>
                                </div>
                                <div class="gd-stat">
                                    <dt>Release</dt>
                                    <dd>{{ formatearFecha(game.release_date) }}</dd>
                                </div>
                                <div class="gd-stat">
                                    <dt>{{ game.platforms?.length === 1 ? 'Platform' : 'Platforms' }}</dt>
                                    <dd>{{ game.platforms?.length || '—' }}</dd>
                                </div>
                            </dl>

                            <footer class="gd-card__set">
                                <span class="gd-card__number">No. {{ game.id }}</span>
                                <span class="gd-card__credit">Data by RAWG</span>
                                <span v-if="isFavorite" class="gd-card__stamp">
                                    <i aria-hidden="true" :class="'pi ' + (gameStatus ? STATUS_META[gameStatus]?.icon : 'pi-heart-fill')"></i>
                                    {{ gameStatus ? STATUS_META[gameStatus]?.label : 'Favorite' }}
                                </span>
                            </footer>
                        </div>
                    </article>
                </div>

                <!-- ── COLUMNA DE TRABAJO ── -->
                <div class="gd-main-col">

                    <!-- Tu copia: acciones del jugador -->
                    <section class="gd-copy" aria-labelledby="gd-copy-title">
                        <h2 id="gd-copy-title" class="gd-h2">Your copy</h2>

                        <div class="gd-copy__row">
                            <button
                                type="button"
                                class="gd-btn"
                                :class="isFavorite ? 'gd-btn--ghost' : 'gd-btn--primary'"
                                :disabled="favoriteLoading"
                                :aria-pressed="isFavorite"
                                @click="alternarFavorito"
                            >
                                <i aria-hidden="true" v-if="favoriteLoading" class="pi pi-spin pi-spinner"></i>
                                <i aria-hidden="true" v-else :class="isFavorite ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                                {{ isFavorite ? 'In your favorites' : 'Add to favorites' }}
                            </button>

                            <!-- Estado: solo para favoritos ya lanzados -->
                            <div v-if="juegoYaSalio && isFavorite" class="gd-status">
                                <button
                                    type="button"
                                    class="gd-btn gd-btn--ghost gd-status__btn"
                                    :class="gameStatus ? `gd-status__btn--${gameStatus}` : ''"
                                    aria-haspopup="menu"
                                    :aria-expanded="showStatusModal"
                                    @click.stop="showStatusModal = !showStatusModal"
                                >
                                    <i aria-hidden="true" :class="'pi ' + (gameStatus ? STATUS_META[gameStatus]?.icon : 'pi-bookmark')"></i>
                                    {{ gameStatus ? STATUS_META[gameStatus]?.label : 'Set status' }}
                                    <i aria-hidden="true" class="pi pi-chevron-down gd-status__chev"></i>
                                </button>

                                <Transition name="gsd">
                                    <div v-if="showStatusModal && game" class="gd-status__menu">
                                        <GameStatusDropdown
                                            :game-id="game.id"
                                            :current-status="gameStatus"
                                            @close="showStatusModal = false"
                                            @update:status="cambiarEstadoDesdeCarta"
                                        />
                                    </div>
                                </Transition>
                            </div>

                            <a href="#gd-reviews" class="gd-btn gd-btn--ghost">
                                <i aria-hidden="true" class="pi pi-star"></i>
                                {{ formRating && !editingId ? `Your rating ${formRating}/5` : 'Rate & review' }}
                            </a>
                        </div>

                        <p v-if="isFavorite && !juegoYaSalio" class="gd-hint">
                            Status becomes available once the game is released.
                        </p>
                        <p v-else-if="!isFavorite" class="gd-hint">
                            Add it to your favorites to track it as Pending, Playing, Paused or Completed.
                        </p>
                    </section>

                    <!-- Descripción -->
                    <section class="gd-panel" aria-labelledby="gd-about-title">
                        <h2 id="gd-about-title" class="gd-h2">About</h2>
                        <div id="gd-about-text" class="gd-prose" :class="{ 'is-clamped': descripcionLarga && !descripcionAbierta }"
                            v-html="descripcionSanitizada || '<p>Description not available.</p>'"></div>
                        <button v-if="descripcionLarga" type="button" class="gd-btn gd-btn--ghost gd-btn--sm gd-readmore"
                            aria-controls="gd-about-text" :aria-expanded="descripcionAbierta"
                            @click="descripcionAbierta = !descripcionAbierta">
                            {{ descripcionAbierta ? 'Show less' : 'Read more' }}
                            <i aria-hidden="true" :class="descripcionAbierta ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"></i>
                        </button>
                    </section>

                    <!-- Detalles: cada dato una sola vez -->
                    <section class="gd-panel" aria-labelledby="gd-details-title">
                        <h2 id="gd-details-title" class="gd-h2">Details</h2>
                        <dl class="gd-details">
                            <div class="gd-details__row">
                                <dt>Platforms</dt>
                                <dd>
                                    <ul v-if="game.platforms?.length" class="gd-chips">
                                        <li v-for="platform in game.platforms" :key="platform.id">{{ platform.name }}</li>
                                    </ul>
                                    <span v-else class="gd-muted">No information</span>
                                </dd>
                            </div>
                            <div class="gd-details__row">
                                <dt>Studios</dt>
                                <dd>
                                    <ul v-if="game.developers?.length" class="gd-people">
                                        <li v-for="dev in game.developers" :key="dev.id">
                                            <span class="gd-people__avatar">
                                                <GameImage v-if="dev.image" :src="dev.image" alt="" width="96" height="96" />
                                                <i aria-hidden="true" v-else class="pi pi-building"></i>
                                            </span>
                                            {{ dev.name }}
                                        </li>
                                    </ul>
                                    <span v-else class="gd-muted">No information</span>
                                </dd>
                            </div>
                            <div v-if="game.team?.length" class="gd-details__row">
                                <dt>Creative team</dt>
                                <dd>
                                    <ul class="gd-people">
                                        <li v-for="member in game.team" :key="member.id">
                                            <span class="gd-people__avatar">
                                                <GameImage v-if="member.image" :src="member.image" alt="" width="96" height="96" />
                                                <i aria-hidden="true" v-else class="pi pi-user"></i>
                                            </span>
                                            <span>
                                                {{ member.name }}
                                                <span class="gd-muted">{{ member.roles.join(', ') || 'Team' }}</span>
                                            </span>
                                        </li>
                                    </ul>
                                </dd>
                            </div>
                            <div v-if="game.stores?.length" class="gd-details__row">
                                <dt>Where to buy</dt>
                                <dd>
                                    <ul class="gd-chips">
                                        <li v-for="store in game.stores" :key="store.id">
                                            <button type="button" class="gd-store" @click="abrirEnlaceExterno(store.url, store.name)">
                                                <i aria-hidden="true" :class="'pi ' + obtenerIconoDeTienda(store.slug)"></i>
                                                {{ store.name }}
                                                <i aria-hidden="true" class="pi pi-external-link gd-store__ext"></i>
                                            </button>
                                        </li>
                                    </ul>
                                </dd>
                            </div>
                        </dl>
                    </section>
                </div>
            </div>

            <!-- ── SECCIONES A TODO EL ANCHO ── -->

            <!-- Galería -->
            <section v-if="mediaItems.length" class="gd-section" aria-labelledby="gd-media-title">
                <h2 id="gd-media-title" class="gd-h2">Media <span class="gd-count">{{ mediaItems.length }}</span></h2>
                <div class="gd-media">
                    <div class="gd-media__viewer">
                        <video v-if="mediaItems[activeShot]?.type === 'video'" :src="mediaItems[activeShot].url"
                            :poster="mediaItems[activeShot].preview" width="1280" height="720" controls muted loop></video>
                        <img v-else :src="mediaItems[activeShot]?.url"
                            :alt="`${game.name}, screenshot ${activeShot + 1}`" width="1280" height="720" />
                        <button type="button" class="gd-media__arrow gd-media__arrow--l" @click="mediaAnterior" aria-label="Previous media">
                            <i aria-hidden="true" class="pi pi-chevron-left"></i>
                        </button>
                        <button type="button" class="gd-media__arrow gd-media__arrow--r" @click="mediaSiguiente" aria-label="Next media">
                            <i aria-hidden="true" class="pi pi-chevron-right"></i>
                        </button>
                    </div>
                    <div class="gd-media__strip">
                        <button
                            v-for="(item, i) in mediaItems"
                            :key="i"
                            type="button"
                            class="gd-media__thumb"
                            :class="{ 'is-on': i === activeShot }"
                            :aria-label="`Show ${item.type === 'video' ? 'video' : 'screenshot'} ${i + 1}`"
                            :aria-current="i === activeShot ? 'true' : null"
                            @click="activeShot = i"
                        >
                            <img v-if="item.type !== 'video'" :src="item.url" alt="" width="160" height="90" loading="lazy" decoding="async" />
                            <img v-else-if="item.preview" :src="item.preview" alt="" width="160" height="90" loading="lazy" decoding="async" />
                            <i v-if="item.type === 'video'" aria-hidden="true" class="pi pi-play gd-media__play"></i>
                        </button>
                    </div>
                </div>
            </section>

            <!-- Logros -->
            <section v-if="logros.length" class="gd-section" aria-labelledby="gd-ach-title">
                <div class="gd-section__head">
                    <h2 id="gd-ach-title" class="gd-h2">Achievements <span class="gd-count">{{ logros.length }}</span></h2>
                    <p class="gd-legend">
                        <span class="gd-legend__item"><i aria-hidden="true" class="pi pi-star-fill gd-rarity gd-rarity--rare"></i>Rare, under 10%</span>
                        <span class="gd-legend__item"><i aria-hidden="true" class="pi pi-stop gd-rarity gd-rarity--uncommon"></i>Uncommon, under 40%</span>
                        <span class="gd-legend__item"><i aria-hidden="true" class="pi pi-circle-fill gd-rarity gd-rarity--common"></i>Common</span>
                    </p>
                </div>
                <ul class="gd-ach">
                    <li v-for="logro in logros" :key="logro.id" class="gd-ach__item" :class="'gd-ach__item--' + logroRareza(logro.percent)" :title="logro.description">
                        <span class="gd-ach__img">
                            <GameImage v-if="logro.image" :src="logro.image" alt="" width="96" height="96" />
                            <i aria-hidden="true" v-else class="pi pi-trophy"></i>
                        </span>
                        <span class="gd-ach__name">{{ logro.name }}</span>
                        <span class="gd-ach__pct">
                            <i aria-hidden="true" class="pi gd-rarity" :class="{ 'pi-star-fill gd-rarity--rare': logroRareza(logro.percent) === 'rareza-raro', 'pi-stop gd-rarity--uncommon': logroRareza(logro.percent) === 'rareza-infrecuente', 'pi-circle-fill gd-rarity--common': logroRareza(logro.percent) === 'rareza-comun' }"></i>
                            <template v-if="logro.percent !== null">{{ logro.percent.toFixed(1) }}% of players</template>
                            <template v-else>Rarity unknown</template>
                        </span>
                    </li>
                </ul>
            </section>

            <!-- Reseñas -->
            <section id="gd-reviews" class="gd-section" aria-labelledby="gd-reviews-title">
                <h2 id="gd-reviews-title" class="gd-h2">Reviews <span class="gd-count">{{ totalComments }}</span></h2>

                <div class="gd-reviews">
                    <!-- Formulario -->
                    <div class="gd-panel gd-review-form" :class="{ 'is-disabled': formularioDeshabilitado }">
                        <h3 class="gd-h3">{{ editingId ? 'Edit your review' : 'Write a review' }}</h3>
                        <div class="gd-rate" @mouseleave="formHover = 0">
                            <span class="gd-rate__label" id="gd-rate-label">Your rating</span>
                            <div class="gd-rate__stars" role="group" aria-labelledby="gd-rate-label">
                                <button v-for="n in 5" :key="n" type="button" class="gd-rate__star"
                                    :class="{ 'is-on': n <= (formHover || formRating) }"
                                    @click="establecerCalificacionFormulario(n)" @mouseenter="formHover = n"
                                    :disabled="formularioDeshabilitado"
                                    :aria-label="`Rate ${n} of 5`"
                                    :aria-pressed="n <= formRating">
                                    <i aria-hidden="true" class="pi pi-star-fill"></i>
                                </button>
                            </div>
                            <span class="gd-rate__value">{{ (formHover || formRating) ? `${formHover || formRating}/5` : 'Not rated' }}</span>
                        </div>
                        <textarea v-model="newComment" name="comment" aria-label="Your review"
                            placeholder="What did you think of this game?…"
                            class="gd-textarea" maxlength="255" rows="4"
                            :disabled="formularioDeshabilitado"></textarea>
                        <div class="gd-review-form__foot">
                            <span class="gd-muted gd-tabular">{{ newComment?.length || 0 }} / 255</span>
                            <div class="gd-review-form__actions">
                                <button v-if="editingId" type="button" class="gd-btn gd-btn--ghost" @click="cancelarEdicionComentario()">
                                    Cancel
                                </button>
                                <button type="button" class="gd-btn gd-btn--primary"
                                    @click="editingId ? actualizarMiComentario() : publicarComentario()"
                                    :disabled="formularioDeshabilitado || !newComment?.trim() || !formRating">
                                    <i aria-hidden="true" :class="editingId ? 'pi pi-check' : 'pi pi-send'"></i>
                                    {{ editingId ? 'Update review' : 'Publish review' }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Lista -->
                    <div class="gd-reviews__list">
                        <div v-if="comments.length === 0" class="gd-empty">
                            <i aria-hidden="true" class="pi pi-comment"></i>
                            <p>No reviews yet. Rate it and write the first one.</p>
                        </div>

                        <TransitionGroup v-else tag="ul" name="comment" class="comments-list">
                            <li v-for="comment in comments" :key="comment.id_comment" class="comment-item gd-review">
                                <div class="gd-review__head">
                                    <span class="gd-review__avatar" aria-hidden="true">{{ comment.username?.charAt(0)?.toUpperCase() }}</span>
                                    <span class="gd-review__who">
                                        <span class="gd-review__name">{{ comment.username }}</span>
                                        <span class="gd-muted">
                                            <template v-if="comment.nickname">@{{ comment.nickname }}, </template>{{ formatearFecha(comment.date_of_comment) }}<template v-if="comment.date_of_update">, edited {{ formatearFecha(comment.date_of_update) }}</template>
                                        </span>
                                    </span>
                                    <span v-if="comment.rating" class="gd-review__rating" role="img" :aria-label="`Rated ${comment.rating} of 5`">
                                        <i aria-hidden="true" class="pi pi-star-fill"></i>{{ comment.rating }}
                                    </span>
                                    <span class="gd-review__tools">
                                        <button v-if="comment.id_user === data_user.id_user" type="button" class="gd-icon-btn"
                                            @click="iniciarEdicionComentario(comment)" title="Edit review" aria-label="Edit review">
                                            <i aria-hidden="true" class="pi pi-pencil"></i>
                                        </button>
                                        <button v-if="comment.id_user === data_user.id_user || data_user?.role === 'admin'" type="button" class="gd-icon-btn gd-icon-btn--danger"
                                            @click="eliminarMiComentario(comment.id_comment)" title="Delete review" aria-label="Delete review">
                                            <i aria-hidden="true" class="pi pi-trash"></i>
                                        </button>
                                    </span>
                                </div>
                                <p class="gd-review__body">{{ comment.description }}</p>
                            </li>
                        </TransitionGroup>

                        <button v-if="hasMoreComments || loadingMore" type="button" class="gd-btn gd-btn--ghost gd-more"
                            @click="cargarMasComentarios" :disabled="loadingMore">
                            <i aria-hidden="true" :class="loadingMore ? 'pi pi-spin pi-spinner' : 'pi pi-chevron-down'"></i>
                            {{ loadingMore ? 'Loading…' : `Load more (${totalComments - comments.length} remaining)` }}
                        </button>
                    </div>
                </div>
            </section>

            <!-- DLC -->
            <section v-if="adiciones.length" class="gd-section" aria-labelledby="gd-dlc-title">
                <h2 id="gd-dlc-title" class="gd-h2">DLC &amp; expansions <span class="gd-count">{{ adiciones.length }}</span></h2>
                <ul class="gd-dlc">
                    <li v-for="dlc in adiciones" :key="dlc.id">
                        <router-link :to="'/game/' + dlc.id" class="gd-dlc__item">
                            <span class="gd-dlc__thumb">
                                <GameImage v-if="dlc.imge_url" :src="dlc.imge_url" alt="" width="160" height="90" />
                                <i aria-hidden="true" v-else class="pi pi-image"></i>
                            </span>
                            <span class="gd-dlc__name">{{ dlc.name }}</span>
                            <span class="gd-muted">{{ formatearFecha(dlc.release_date) }}</span>
                        </router-link>
                    </li>
                </ul>
            </section>

            <!-- Saga -->
            <section v-if="juegosSaga.length" class="gd-section" aria-labelledby="gd-series-title">
                <h2 id="gd-series-title" class="gd-h2">More from this series</h2>
                <ul class="gd-series">
                    <li v-for="juego in juegosSaga" :key="juego.id" class="gd-mini">
                        <router-link :to="'/game/' + juego.id" class="gd-mini__link">
                            <span class="gd-mini__band">
                                <span class="gd-mini__name" :title="juego.name">{{ juego.name }}</span>
                                <span class="gd-mini__mc" :class="juego.metacritic ? claseMetacritic(juego.metacritic) : 'mc-na'">
                                    <span class="sr-only">Metacritic</span>{{ juego.metacritic ?? '—' }}
                                </span>
                            </span>
                            <span class="gd-mini__art">
                                <GameImage :src="juego.imge_url" alt="" width="640" height="480" />
                            </span>
                            <span class="gd-mini__set">
                                <span class="gd-card__number">No. {{ juego.id }}</span>
                                <span>{{ juego.release_date ? juego.release_date.split('-')[0] : 'TBA' }}</span>
                            </span>
                        </router-link>
                        <button type="button" class="gd-icon-btn gd-mini__fav"
                            :aria-pressed="sagaFavoritos.has(juego.id)"
                            :aria-label="(sagaFavoritos.has(juego.id) ? 'Remove ' : 'Add ') + juego.name + (sagaFavoritos.has(juego.id) ? ' from favorites' : ' to favorites')"
                            @click="alternarFavoritoSaga(juego.id)">
                            <i aria-hidden="true" :class="sagaFavoritos.has(juego.id) ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                        </button>
                    </li>
                </ul>
            </section>
        </div>
    </div>

    <!-- Modal aviso enlace externo -->
    <Transition name="modal">
      <div v-if="externalLink.open" class="ext-modal-overlay" @click.self="cancelarEnlaceExterno">
          <div class="ext-modal" role="dialog" aria-modal="true" aria-labelledby="ext-modal-title">
              <div class="ext-modal__icon">
                  <i aria-hidden="true" class="pi pi-external-link"></i>
              </div>
              <h2 id="ext-modal-title" class="ext-modal__title">Leaving Game Rank</h2>
              <p class="ext-modal__body">
                  You are about to visit <strong>{{ externalLink.storeName }}</strong>,
                  an external site not controlled by Game Rank.
                  Do you want to continue?
              </p>
              <div class="ext-modal__actions">
                  <button type="button" class="ext-modal__btn ext-modal__btn--cancel" @click="cancelarEnlaceExterno">
                      Cancel
                  </button>
                  <button type="button" class="ext-modal__btn ext-modal__btn--confirm" @click="confirmarEnlaceExterno">
                      <i aria-hidden="true" class="pi pi-external-link"></i>
                      Continue
                  </button>
              </div>
          </div>
      </div>
    </Transition>
</template>

<script>
import '@fontsource/barlow/400.css';
import '@fontsource/barlow/500.css';
import '@fontsource/barlow/600.css';
import '@fontsource/barlow/700.css';
import '@fontsource/barlow-condensed/700.css';
import '@fontsource/barlow-condensed/800.css';
import jsDetalles from "./script_GameDetail.js";
import Skeleton from '../Skeleton/Skeleton.vue';
import GameImage from '../Image/GameImage.vue';
import GameStatusDropdown from '../Cards/GameStatusDropdown.vue';

export default {
    name: 'GameDetail',
    components: { Skeleton, GameImage, GameStatusDropdown },
    mixins: [jsDetalles],

    data() {
        return {
            // Cambia cada vez que el jugador cambia el estado: re-monta la
            // franja holografica para que el barrido corra una sola vez
            holoKey: 0,
            descripcionAbierta: false
        };
    },

    computed: {
        // Las descripciones de RAWG pueden ser muy largas (a veces incluyen
        // una segunda version en otro idioma): por encima de ~700 caracteres
        // se recortan y se ofrece "Read more"
        descripcionLarga() {
            var texto = (this.descripcionSanitizada || '').replace(/<[^>]+>/g, '');
            return texto.length > 700;
        }
    },

    methods: {
        // El barrido solo responde a un cambio hecho por el jugador, no a la
        // carga inicial del estado desde la API
        cambiarEstadoDesdeCarta(payload) {
            this.manejarActualizacionEstado(payload);
            if (payload && payload.status) {
                this.holoKey += 1;
            }
        }
    }
};
</script>

<style scoped src="./styles_GameDetail.css"></style>
