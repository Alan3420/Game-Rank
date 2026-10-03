<template>
  <div class="catalog card-world">
    <div class="cat-shell">

      <header class="cat-head">
        <h1 class="cat-title">{{ titulo }}</h1>
        <p class="cat-sub">
          <template v-if="tieneFiltrosActivos">
            {{ cantidadFiltrosActivos }} {{ cantidadFiltrosActivos === 1 ? 'filter' : 'filters' }} applied.
            <button type="button" class="cat-link" @click="limpiarFiltros">Clear all</button>
          </template>
          <template v-else>Every game on RAWG, with your status on the ones you own.</template>
        </p>
      </header>

      <div class="cat-layout">
        <!-- Barra lateral de filtros (cajon en movil) -->
        <aside id="cat-filters" class="cat-rail" :class="{ 'is-open': filtrosAbiertos }" aria-label="Catalog filters">
          <FilterPanel :ordering="filters.ordering" @apply="aplicarFiltros" @clear="limpiarFiltros" />
        </aside>

        <section class="cat-results" aria-labelledby="cat-count">
          <div class="cat-bar">
            <div class="cat-bar__summary">
              <h2 id="cat-count" class="cat-count" aria-live="polite">{{ loading ? 'Loading games…' : textoTotal }}</h2>
              <span class="cat-order">Sorted by {{ etiquetaOrden }}</span>
            </div>

            <div class="cat-bar__tools">
              <button type="button" class="cat-btn cat-filters-btn" aria-controls="cat-filters"
                :aria-expanded="filtrosAbiertos" @click="filtrosAbiertos = !filtrosAbiertos">
                <i aria-hidden="true" class="pi pi-sliders-h"></i>
                Filters
                <span v-if="cantidadFiltrosActivos > 0" class="cat-btn__badge">{{ cantidadFiltrosActivos }}</span>
              </button>

              <div class="cat-switch" role="group" aria-label="View">
                <button type="button" class="cat-switch__btn" :aria-pressed="vista === 'grid'" @click="cambiarVista('grid')">
                  <i aria-hidden="true" class="pi pi-th-large"></i>
                  Grid
                </button>
                <button type="button" class="cat-switch__btn" :aria-pressed="vista === 'checklist'" @click="cambiarVista('checklist')">
                  <i aria-hidden="true" class="pi pi-list"></i>
                  Checklist
                </button>
              </div>
            </div>
          </div>

          <!-- Cargando -->
          <div v-if="loading" aria-busy="true">
            <ul v-if="vista === 'grid'" class="cat-grid cat-album">
              <li v-for="n in 8" :key="n"><Skeleton class="cat-card-skel" radius="16px" /></li>
            </ul>
            <div v-else class="cat-table-skel">
              <Skeleton v-for="n in 8" :key="n" width="100%" height="52px" radius="8px" />
            </div>
          </div>

          <!-- Sin resultados -->
          <div v-else-if="games.length === 0" class="cat-empty">
            <i aria-hidden="true" class="pi pi-search"></i>
            <p v-if="game_name">No games match "{{ game_name }}"{{ tieneFiltrosActivos ? ' with these filters' : '' }}.</p>
            <p v-else>No games match these filters.</p>
            <button v-if="tieneFiltrosActivos" type="button" class="cat-btn" @click="limpiarFiltros">Clear filters</button>
          </div>

          <!-- Rejilla: pagina de album -->
          <ul v-else-if="vista === 'grid'" class="cat-grid cat-album">
            <li v-for="game in games" :key="game.id">
              <MiniCard
                :game="game"
                :status="statuses.get(game.id) || null"
                :favorite="favorites.has(game.id)"
                show-favorite
                :can-change-status="puedeCambiarEstado(game)"
                @toggle-favorite="alternarFavorito"
                @update:status="manejarActualizacionEstado"
              />
            </li>
          </ul>

          <!-- Checklist: tabla del set -->
          <div v-else class="cat-table-wrap">
            <table class="cat-table">
              <caption class="sr-only">{{ textoTotal }}, page {{ currentPage }}</caption>
              <thead>
                <tr>
                  <th scope="col" class="cat-th--no">No.</th>
                  <th scope="col" :aria-sort="ariaSort('name')">
                    <button type="button" class="cat-sort" @click="ordenarPor('name')">
                      Game
                      <i aria-hidden="true" class="pi" :class="ariaSort('name') === 'ascending' ? 'pi-sort-up-fill' : ariaSort('name') === 'descending' ? 'pi-sort-down-fill' : 'pi-sort-alt'"></i>
                    </button>
                  </th>
                  <th scope="col" :aria-sort="ariaSort('released')">
                    <button type="button" class="cat-sort" @click="ordenarPor('released')">
                      Released
                      <i aria-hidden="true" class="pi" :class="ariaSort('released') === 'ascending' ? 'pi-sort-up-fill' : ariaSort('released') === 'descending' ? 'pi-sort-down-fill' : 'pi-sort-alt'"></i>
                    </button>
                  </th>
                  <th scope="col" :aria-sort="ariaSort('metacritic')">
                    <button type="button" class="cat-sort" @click="ordenarPor('metacritic')">
                      Metacritic
                      <i aria-hidden="true" class="pi" :class="ariaSort('metacritic') === 'ascending' ? 'pi-sort-up-fill' : ariaSort('metacritic') === 'descending' ? 'pi-sort-down-fill' : 'pi-sort-alt'"></i>
                    </button>
                  </th>
                  <th scope="col">Your status</th>
                  <th scope="col"><span class="sr-only">Actions</span></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="game in games" :key="game.id" class="cat-row cw-frame"
                  :class="statuses.get(game.id) ? 'cw-frame--' + statuses.get(game.id) : ''">
                  <td class="cat-row__no">{{ game.id }}</td>
                  <td class="cat-row__game">
                    <router-link :to="'/game/' + game.id" class="cat-row__link">
                      <span class="cat-row__thumb"><GameImage :src="game.imge_url" alt="" width="160" height="120" /></span>
                      <span class="cat-row__name">{{ game.name }}</span>
                    </router-link>
                  </td>
                  <td class="cat-row__date">{{ formatearFecha(game.release_date) }}</td>
                  <td class="cat-row__mc">
                    <span class="cw-mc" :class="claseMetacritic(game.metacritic)">{{ game.metacritic ?? '—' }}</span>
                  </td>
                  <td class="cat-row__owned">
                    <span v-if="statuses.get(game.id)" class="cat-pill">
                      <i aria-hidden="true" :class="'pi ' + STATUS_META[statuses.get(game.id)].icon"></i>
                      {{ STATUS_META[statuses.get(game.id)].label }}
                    </span>
                    <span v-else-if="favorites.has(game.id)" class="cat-muted">Favorite</span>
                    <span v-else class="cat-muted">—</span>
                  </td>
                  <td class="cat-row__actions">
                    <div class="cat-row__status">
                      <button v-if="puedeCambiarEstado(game)" type="button" class="cat-icon-btn"
                        aria-haspopup="menu" :aria-expanded="menuEstadoAbierto === game.id"
                        :aria-label="'Change status of ' + game.name" @click="alternarMenuEstado(game.id)">
                        <i aria-hidden="true" class="pi pi-bookmark"></i>
                      </button>
                      <Transition name="gsd">
                        <div v-if="menuEstadoAbierto === game.id" class="cat-row__menu">
                          <GameStatusDropdown
                            :game-id="game.id"
                            :current-status="statuses.get(game.id) || null"
                            @close="menuEstadoAbierto = null"
                            @update:status="manejarActualizacionEstado"
                          />
                        </div>
                      </Transition>
                    </div>
                    <button type="button" class="cat-icon-btn" :aria-pressed="favorites.has(game.id)"
                      :aria-label="(favorites.has(game.id) ? 'Remove ' : 'Add ') + game.name + (favorites.has(game.id) ? ' from favorites' : ' to favorites')"
                      @click="alternarFavorito(game.id)">
                      <i aria-hidden="true" :class="favorites.has(game.id) ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <Pagination
            v-if="!loading"
            :current-page="currentPage"
            :total-pages="totalPaginas"
            @update:current-page="cargarPagina"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import contenido from "./script_contenido.js";
import FilterPanel from "../Filters/FilterPanel.vue";
import Pagination from "../Pagination/Pagination.vue";
import Skeleton from "../Skeleton/Skeleton.vue";
import GameImage from "../Image/GameImage.vue";
import MiniCard from "../CardWorld/MiniCard.vue";
import GameStatusDropdown from "../Cards/GameStatusDropdown.vue";

export default {
    name: "Catalog",
    components: { FilterPanel, Pagination, Skeleton, GameImage, MiniCard, GameStatusDropdown },
    ...contenido
};
</script>

<style scoped src="./style_contenido.css"></style>
