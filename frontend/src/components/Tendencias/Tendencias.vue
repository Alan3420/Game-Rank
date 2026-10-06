<template>
  <div class="trends card-world">
    <div class="tr-shell">

      <!-- ── TITULO + SELECTOR ── -->
      <header class="tr-head">
        <div class="tr-head__text">
          <h1 class="tr-title">Trends</h1>
          <p class="tr-lede">{{ seccionActiva.descripcion }}</p>
        </div>

        <div class="tr-tabs" role="tablist" aria-label="Ranking" @keydown="moverPestana">
          <button v-for="sec in secciones" :id="'tr-tab-' + sec.slug" :key="sec.key" type="button" role="tab"
            class="tr-tab" aria-controls="tr-board" :aria-selected="activa === sec.key"
            :tabindex="activa === sec.key ? 0 : -1" @click="elegir(sec.key)">
            <i aria-hidden="true" :class="'pi ' + sec.icono"></i>
            {{ sec.titulo }}
          </button>
        </div>
      </header>

      <!-- ── TABLERO ── -->
      <section id="tr-board" class="tr-board" role="tabpanel" :aria-labelledby="'tr-tab-' + seccionActiva.slug"
        :aria-busy="loading ? 'true' : 'false'">

        <div v-if="loading" class="tr-grid">
          <Skeleton class="tr-champ-skel" radius="20px" />
          <div class="tr-rows-skel">
            <Skeleton v-for="n in 7" :key="n" width="100%" height="64px" radius="12px" />
          </div>
        </div>

        <div v-else-if="error" class="tr-empty" role="alert">
          <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
          <p>{{ error }}</p>
        </div>

        <div v-else-if="juegos.length === 0" class="tr-empty">
          <i aria-hidden="true" :class="'pi ' + seccionActiva.icono"></i>
          <p>Not enough community activity for this ranking yet.</p>
        </div>

        <Transition v-else name="tr-swap" mode="out-in">
          <div :key="activa" class="tr-grid">

            <!-- Numero 1: carta campeona -->
            <router-link :to="'/game/' + campeon.id" class="tr-champ cw-frame"
              :class="estadoDe(campeon.id) ? 'cw-frame--' + estadoDe(campeon.id) : ''">
              <span class="tr-champ__band">
                <span class="tr-champ__rank">No. 1</span>
                <span class="tr-champ__lead">{{ ventaja }}</span>
              </span>
              <span class="tr-champ__face">
                <span class="tr-champ__art">
                  <GameImage :src="campeon.imge_url" alt="" width="640" height="360" />
                </span>
                <span class="tr-champ__name">{{ campeon.name }}</span>
                <span class="tr-champ__stat">
                  <strong>{{ valorDe(campeon) }}</strong>
                  <span>{{ unidadDe(campeon) }}</span>
                  <span v-if="campeon.stat_count" class="tr-champ__count">from {{ resenas(campeon.stat_count) }}</span>
                </span>
                <span class="tr-champ__foot">
                  <span class="tr-no">No. {{ campeon.id }}</span>
                  <span v-if="anioDe(campeon)" class="tr-year">{{ anioDe(campeon) }}</span>
                  <span v-if="estadoDe(campeon.id)" class="tr-stamp">
                    <i aria-hidden="true" :class="'pi ' + STATUS_META[estadoDe(campeon.id)].icon"></i>
                    {{ STATUS_META[estadoDe(campeon.id)].label }}
                  </span>
                  <span v-if="campeon.metacritic" class="cw-mc" :class="claseMetacritic(campeon.metacritic)">
                    <span class="sr-only">Metacritic </span>{{ campeon.metacritic }}
                  </span>
                </span>
              </span>
            </router-link>

            <!-- Puestos 2 a 8 -->
            <ol class="tr-rows">
              <li v-for="(juego, i) in resto" :key="juego.id" class="tr-row cw-frame"
                :class="estadoDe(juego.id) ? ['tr-row--owned', 'cw-frame--' + estadoDe(juego.id)] : ''">
                <router-link :to="'/game/' + juego.id" class="tr-row__link">
                  <span class="tr-row__rank" :class="{ 'tr-row__rank--tie': empatado(i + 1) }">
                    <span class="sr-only">Place </span>{{ puestos[i + 1] }}
                  </span>
                  <span class="tr-row__thumb"><GameImage :src="juego.imge_url" alt="" width="160" height="120" /></span>
                  <span class="tr-row__id">
                    <span class="tr-row__name">{{ juego.name }}</span>
                    <span class="tr-row__meta">
                      <span class="tr-no">No. {{ juego.id }}</span>
                      <span v-if="anioDe(juego)" class="tr-year">{{ anioDe(juego) }}</span>
                      <span v-if="estadoDe(juego.id)" class="tr-stamp">
                        <i aria-hidden="true" :class="'pi ' + STATUS_META[estadoDe(juego.id)].icon"></i>
                        <span class="tr-stamp__label">{{ STATUS_META[estadoDe(juego.id)].label }}</span>
                      </span>
                    </span>
                  </span>
                  <span class="tr-row__stat">
                    <span class="tr-row__value">
                      {{ valorDe(juego) }} <span class="tr-row__unit">{{ unidadDe(juego) }}</span>
                      <span v-if="juego.stat_count" class="tr-row__unit tr-row__count">· {{ resenas(juego.stat_count) }}</span>
                    </span>
                    <span class="tr-bar" aria-hidden="true"><span class="tr-bar__fill" :style="{ width: proporcion(juego) + '%' }"></span></span>
                  </span>
                </router-link>
              </li>
            </ol>
          </div>
        </Transition>

        <p v-if="!loading && !error && juegos.length" class="tr-note">
          {{ seccionActiva.nota }} Equal values share a place. Counted from Game Rank players.
        </p>
      </section>
    </div>
  </div>
</template>

<script>
import tendenciasScript from './script_tendencias.js';
import Skeleton from '../Skeleton/Skeleton.vue';
import GameImage from '../Image/GameImage.vue';

export default {
  name: 'Tendencias',
  components: { Skeleton, GameImage },
  mixins: [tendenciasScript]
};
</script>

<style scoped src="./styles_tendencias.css"></style>
