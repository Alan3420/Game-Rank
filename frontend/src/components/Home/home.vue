<template>
  <div class="home card-world">

    <!-- ══ INVITADO ══ -->
    <div v-if="!estadoAutenticacion.usuario" class="hm-shell">
      <section class="hm-guest" aria-labelledby="hm-guest-title">
        <div class="hm-guest__text">
          <h1 id="hm-guest-title" class="hm-guest__title">Every game you play becomes a card you own.</h1>
          <p class="hm-guest__lead">
            Find games, read what the community thinks, and keep your collection in one album:
            pending, playing, paused or completed.
          </p>
          <div class="hm-guest__actions">
            <button type="button" class="hm-btn hm-btn--primary" @click="irARegistro">
              <i aria-hidden="true" class="pi pi-user-plus"></i>
              Create an account
            </button>
            <button type="button" class="hm-btn hm-btn--ghost" @click="irALogin">
              <i aria-hidden="true" class="pi pi-sign-in"></i>
              Sign in
            </button>
          </div>
        </div>

        <figure class="hm-trailer cw-frame">
          <div class="hm-trailer__face">
            <div v-if="heroVideo && heroVideo.name" class="hm-trailer__band">
              <span class="hm-trailer__name">{{ heroVideo.name }}</span>
              <span class="cw-mc" :class="claseMetacritic(heroVideo.metacritic)"><span class="sr-only">Metacritic</span>{{ heroVideo.metacritic ?? '—' }}</span>
            </div>
            <div class="hm-trailer__art">
              <video v-if="heroVideo" ref="heroVideoRef" :autoplay="!videoPausado" muted loop playsinline aria-hidden="true">
                <source :src="heroVideo.video_url" type="video/mp4" />
              </video>
              <Skeleton v-else-if="!heroVideoCargado" class="hm-trailer__skel" radius="0" />
              <p v-else class="hm-trailer__none">Trailer unavailable right now.</p>
              <button v-if="heroVideo" type="button" class="hm-trailer__toggle" @click="alternarVideo"
                :aria-label="videoPausado ? 'Play trailer' : 'Pause trailer'">
                <i aria-hidden="true" class="pi" :class="videoPausado ? 'pi-play' : 'pi-pause'"></i>
              </button>
            </div>
            <figcaption class="hm-trailer__caption">
              <span v-if="heroVideo && heroVideo.id" class="hm-trailer__number">No. {{ heroVideo.id }}</span>
              <span v-else>Featured trailer</span>
              <span>Data by RAWG</span>
            </figcaption>
          </div>
        </figure>
      </section>

      <section class="hm-frames" aria-labelledby="hm-frames-title">
        <h2 id="hm-frames-title" class="cw-h2">Your status is the frame</h2>
        <p class="hm-frames__lead">The same card changes its frame as your game moves through your album.</p>
        <ul class="hm-frames__list">
          <li v-for="key in STATUS_LIST" :key="key" class="hm-frames__item">
            <MiniCard :game="juegoDemo" :status="key" />
            <span class="hm-frames__desc">{{ STATUS_META[key].desc }}</span>
          </li>
        </ul>
      </section>
    </div>

    <!-- ══ JUGADOR ══ -->
    <div v-else class="hm-shell">

      <header class="hm-greet">
        <h1 class="hm-greet__title">Welcome back, {{ nombreJugador }}</h1>
        <dl class="hm-greet__totals" aria-label="Your totals">
          <div>
            <dt>In your album</dt>
            <dd>{{ stats ? stats.coleccion.total : coleccion.length }}</dd>
          </div>
          <div>
            <dt>Favorites</dt>
            <dd>{{ stats ? stats.favoritos : '—' }}</dd>
          </div>
          <div>
            <dt>Reviews</dt>
            <dd>{{ stats ? stats.comentarios : '—' }}</dd>
          </div>
          <div>
            <dt>Avg. rating</dt>
            <dd>
              <i v-if="stats && stats.rating_medio" aria-hidden="true" class="pi pi-star-fill"></i>
              {{ stats && stats.rating_medio ? stats.rating_medio : '—' }}
            </dd>
          </div>
        </dl>
      </header>

      <!-- ── EL ALBUM ABIERTO ── -->
      <div class="hm-spread">

        <!-- pagina izquierda: tu archivador -->
        <section class="hm-album cw-frame" :class="'cw-frame--' + tabActiva" aria-labelledby="hm-album-title">
          <div class="hm-album__head">
            <h2 id="hm-album-title" class="cw-h2">Your album</h2>
            <router-link to="/user/profile" class="hm-link">
              Open profile
              <i aria-hidden="true" class="pi pi-arrow-right"></i>
            </router-link>
          </div>

          <div class="hm-tabs" role="tablist" aria-label="Collection status"
            @keydown="moverPestana($event, STATUS_LIST, tabActiva, function (v) { tabActiva = v; })">
            <button
              v-for="key in STATUS_LIST"
              :key="key"
              :id="'hm-tab-' + key"
              type="button"
              role="tab"
              class="hm-tab cw-frame"
              :class="'cw-frame--' + key"
              :aria-selected="tabActiva === key"
              :tabindex="tabActiva === key ? 0 : -1"
              aria-controls="hm-pockets"
              @click="tabActiva = key"
            >
              <i aria-hidden="true" :class="'pi ' + STATUS_META[key].icon"></i>
              {{ STATUS_META[key].label }}
              <span class="hm-tab__count">{{ coleccionLoading ? '·' : conteoPorEstado[key] }}</span>
            </button>
          </div>

          <div id="hm-pockets" class="hm-pockets" role="tabpanel" :aria-labelledby="'hm-tab-' + tabActiva">
            <template v-if="coleccionLoading">
              <Skeleton v-for="n in 6" :key="n" class="hm-pocket-skel" radius="16px" />
            </template>

            <div v-else-if="cartasVisibles.length === 0" class="hm-empty">
              <i aria-hidden="true" :class="'pi ' + STATUS_META[tabActiva].icon"></i>
              <p>No games marked as {{ STATUS_META[tabActiva].label.toLowerCase() }} yet.</p>
              <router-link to="/content/overview" class="hm-btn hm-btn--ghost hm-btn--sm">
                Browse the catalog
              </router-link>
            </div>

            <ul v-else class="hm-pockets__grid">
              <li v-for="item in cartasVisibles" :key="item.game.id">
                <MiniCard :game="item.game" :status="item.status" />
              </li>
              <li v-for="n in fundasVacias" :key="'funda-' + n" class="hm-sleeve" aria-hidden="true"></li>
              <li v-if="hayBolsilloCatalogo" class="hm-sleeve hm-sleeve--link">
                <router-link to="/content/overview" class="hm-sleeve__link">
                  <i aria-hidden="true" class="pi pi-plus"></i>
                  Find your next game
                </router-link>
              </li>
            </ul>
          </div>

          <p v-if="!coleccionLoading && cartasDeLaPestana.length > cartasVisibles.length" class="hm-album__more">
            Showing {{ cartasVisibles.length }} of {{ cartasDeLaPestana.length }}.
            <router-link to="/user/profile" class="hm-link">See them all in your profile</router-link>
          </p>
        </section>

        <!-- pagina derecha: lo que ofrece el mundo -->
        <div class="hm-right" aria-label="This year and this month">
          <section class="hm-checklist" aria-labelledby="hm-best-title">
            <div class="hm-checklist__head">
              <h2 id="hm-best-title" class="cw-h2">Top rated of {{ anioActual }}</h2>
              <span class="hm-muted">Player ratings on RAWG</span>
            </div>
            <ol v-if="mejoresLoading" class="hm-rows">
              <li v-for="n in 5" :key="n" class="hm-row hm-row--skel">
                <Skeleton width="100%" height="44px" radius="8px" />
              </li>
            </ol>
            <p v-else-if="mejoresAnio.length === 0" class="hm-muted">No rated releases this year yet.</p>
            <ol v-else class="hm-rows">
              <li v-for="(juego, i) in mejoresAnio" :key="juego.id">
                <router-link :to="'/game/' + juego.id" class="hm-row cw-frame" :class="estadoPorJuego[juego.id] ? 'cw-frame--' + estadoPorJuego[juego.id] : ''">
                  <span class="hm-row__rank">{{ i + 1 }}</span>
                  <span class="hm-row__thumb"><GameImage :src="juego.imge_url" alt="" width="160" height="120" /></span>
                  <span class="hm-row__text">
                    <span class="hm-row__name">{{ juego.name }}</span>
                    <span class="hm-row__meta">
                      <span class="hm-row__no">No. {{ juego.id }}</span>
                      {{ formatearFecha(juego.release_date) }}
                      <span v-if="estadoPorJuego[juego.id]" class="hm-row__owned">{{ STATUS_META[estadoPorJuego[juego.id]].label }}</span>
                    </span>
                  </span>
                  <span class="hm-row__score" :aria-label="`Rated ${juego.rating} of 5 by RAWG players`">
                    <i aria-hidden="true" class="pi pi-star-fill"></i>{{ Number(juego.rating).toFixed(1) }}
                  </span>
                </router-link>
              </li>
            </ol>
          </section>

          <section class="hm-checklist" aria-labelledby="hm-new-title">
            <h2 id="hm-new-title" class="cw-h2">New this month</h2>
            <ol v-if="novedadesLoading" class="hm-rows">
              <li v-for="n in 5" :key="n" class="hm-row hm-row--skel">
                <Skeleton width="100%" height="44px" radius="8px" />
              </li>
            </ol>
            <p v-else-if="novedades.length === 0" class="hm-muted">No releases this month yet.</p>
            <ol v-else class="hm-rows">
              <li v-for="(juego, i) in novedades" :key="juego.id">
                <router-link :to="'/game/' + juego.id" class="hm-row cw-frame" :class="estadoPorJuego[juego.id] ? 'cw-frame--' + estadoPorJuego[juego.id] : ''">
                  <span class="hm-row__rank">{{ i + 1 }}</span>
                  <span class="hm-row__thumb"><GameImage :src="juego.imge_url" alt="" width="160" height="120" /></span>
                  <span class="hm-row__text">
                    <span class="hm-row__name">{{ juego.name }}</span>
                    <span class="hm-row__meta">
                      <span class="hm-row__no">No. {{ juego.id }}</span>
                      {{ formatearFecha(juego.release_date) }}
                      <span v-if="estadoPorJuego[juego.id]" class="hm-row__owned">{{ STATUS_META[estadoPorJuego[juego.id]].label }}</span>
                    </span>
                  </span>
                  <span v-if="juego.metacritic" class="cw-mc" :class="claseMetacritic(juego.metacritic)"><span class="sr-only">Metacritic</span>{{ juego.metacritic }}</span>
                </router-link>
              </li>
            </ol>
          </section>
        </div>
      </div>

      <!-- ── PARTE BAJA ── -->
      <div class="hm-lower">
        <section class="hm-trends" aria-labelledby="hm-trends-title">
          <div class="hm-section-head">
            <h2 id="hm-trends-title" class="cw-h2">Trending in Game Rank</h2>
            <div class="hm-seg" role="tablist" aria-label="Trend"
              @keydown="moverPestana($event, SECCIONES_TENDENCIAS.map(function (s) { return s.key; }), tabTendencia, function (v) { tabTendencia = v; })">
              <button
                v-for="sec in SECCIONES_TENDENCIAS"
                :key="sec.key"
                :id="'hm-trend-' + sec.key"
                type="button"
                role="tab"
                class="hm-seg__btn"
                :aria-selected="tabTendencia === sec.key"
                :tabindex="tabTendencia === sec.key ? 0 : -1"
                aria-controls="hm-trends-panel"
                @click="tabTendencia = sec.key"
              >{{ sec.label }}</button>
            </div>
          </div>

          <div id="hm-trends-panel" role="tabpanel" :aria-labelledby="'hm-trend-' + tabTendencia">
            <ol v-if="tendenciasLoading" class="hm-trends__grid">
              <li v-for="n in 4" :key="n"><Skeleton class="hm-pocket-skel" radius="16px" /></li>
            </ol>
            <p v-else-if="juegosTendencia.length === 0" class="hm-muted">
              Not enough community activity yet. Rate and collect games to start the rankings.
            </p>
            <ol v-else class="hm-trends__grid">
              <li v-for="(juego, i) in juegosTendencia" :key="juego.id" class="hm-trend">
                <span class="hm-trend__rank">#{{ i + 1 }}</span>
                <MiniCard :game="juego" :status="estadoPorJuego[juego.id] || null" />
                <span class="hm-trend__stat">{{ etiquetaTendencia(juego) }}</span>
              </li>
            </ol>
          </div>
        </section>

        <section class="hm-upcoming" aria-labelledby="hm-upcoming-title">
          <h2 id="hm-upcoming-title" class="cw-h2">Coming soon</h2>
          <ul class="hm-cal" :aria-busy="proximosLoading">
            <template v-if="proximosLoading">
              <li v-for="n in 5" :key="n"><Skeleton width="100%" height="56px" radius="10px" /></li>
            </template>
            <li v-else-if="proximos.length === 0" class="hm-muted">No upcoming releases found.</li>
            <template v-else>
              <li v-for="juego in proximos" :key="juego.id">
                <router-link :to="'/game/' + juego.id" class="hm-cal__item">
                  <span class="hm-cal__date">
                    <span class="hm-cal__month">{{ mesCorto(juego.release_date) }}</span>
                    <span class="hm-cal__day">{{ juego.release_date ? Number(juego.release_date.split('-')[2]) : '—' }}</span>
                    <span v-if="anioDe(juego.release_date) !== anioActual" class="hm-cal__year">{{ anioDe(juego.release_date) }}</span>
                  </span>
                  <span class="hm-cal__name">{{ juego.name }}</span>
                  <i aria-hidden="true" class="pi pi-chevron-right hm-cal__go"></i>
                </router-link>
              </li>
            </template>
          </ul>
          <div class="hm-pager">
            <button type="button" class="hm-btn hm-btn--ghost hm-btn--sm" :disabled="paginaProximos <= 1 || proximosLoading"
              @click="cargarProximos(paginaProximos - 1)" aria-label="Previous releases">
              <i aria-hidden="true" class="pi pi-chevron-left"></i>
            </button>
            <span class="hm-muted hm-tabular">Page {{ paginaProximos }} of {{ totalPaginasProximos }}</span>
            <button type="button" class="hm-btn hm-btn--ghost hm-btn--sm" :disabled="paginaProximos >= totalPaginasProximos || proximosLoading"
              @click="cargarProximos(paginaProximos + 1)" aria-label="Next releases">
              <i aria-hidden="true" class="pi pi-chevron-right"></i>
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import jsHome from "./script_home.js";
import Skeleton from "../Skeleton/Skeleton.vue";
import GameImage from "../Image/GameImage.vue";
import MiniCard from "../CardWorld/MiniCard.vue";

export default {
  name: 'Home',
  components: { Skeleton, GameImage, MiniCard },
  mixins: [jsHome]
};
</script>

<style scoped src="./style_home.css"></style>
