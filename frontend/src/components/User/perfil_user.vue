<template>
  <div class="profile card-world">

    <!-- Cargando la sesion -->
    <div v-if="estadoAutenticacion.cargando" class="pf-shell" aria-busy="true">
      <Skeleton width="320px" height="2.6rem" radius="10px" />
      <div class="pf-plates pf-plates--skel">
        <Skeleton v-for="n in 7" :key="n" height="110px" radius="14px" />
      </div>
      <Skeleton width="100%" height="56px" radius="12px" />
    </div>

    <div v-else-if="estadoAutenticacion.usuario" class="pf-shell">

      <!-- ── BANDA DE NOMBRE ── -->
      <header class="pf-head">
        <span class="pf-avatar" aria-hidden="true">
          {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}{{ estadoAutenticacion.usuario.last_name?.charAt(0)?.toUpperCase() }}
        </span>
        <div class="pf-head__id">
          <h1 class="pf-name">{{ estadoAutenticacion.usuario.name }} {{ estadoAutenticacion.usuario.last_name }}</h1>
          <p class="pf-handle">
            <span v-if="estadoAutenticacion.usuario.nickname">@{{ estadoAutenticacion.usuario.nickname }}</span>
            <span class="pf-role">
              <i aria-hidden="true" :class="esAdministrador ? 'pi pi-crown' : 'pi pi-user'"></i>
              {{ esAdministrador ? 'Administrator' : 'Player' }}
            </span>
          </p>
        </div>
        <button id="pf-settings-btn" type="button" class="pf-btn pf-btn--ghost" aria-haspopup="dialog"
          :aria-expanded="panelCuenta" aria-controls="pf-panel" @click="abrirPanelCuenta">
          <i aria-hidden="true" class="pi pi-cog"></i>
          Account settings
        </button>
      </header>

      <!-- ── VITRINA: PLACAS DE TROFEO ── -->
      <section class="pf-cabinet" aria-labelledby="pf-cabinet-title">
        <h2 id="pf-cabinet-title" class="sr-only">Your totals</h2>
        <ul class="pf-plates">
          <li v-for="key in ['completado', 'jugando', 'pausado', 'pendiente']" :key="key" class="pf-plate cw-frame" :class="'cw-frame--' + key">
            <span class="pf-plate__face">
              <i aria-hidden="true" :class="'pi ' + STATUS_META[key].icon + ' pf-plate__icon'"></i>
              <span class="pf-plate__value">
                <Skeleton v-if="statsLoading" width="2.5rem" height="2.2rem" />
                <template v-else>{{ stats?.coleccion?.[key] ?? 0 }}</template>
              </span>
              <span class="pf-plate__label">{{ STATUS_META[key].label }}</span>
            </span>
          </li>
          <li class="pf-plate cw-frame">
            <span class="pf-plate__face">
              <i aria-hidden="true" class="pi pi-heart-fill pf-plate__icon"></i>
              <span class="pf-plate__value">
                <Skeleton v-if="statsLoading" width="2.5rem" height="2.2rem" />
                <template v-else>{{ stats?.favoritos ?? 0 }}</template>
              </span>
              <span class="pf-plate__label">Favorites</span>
            </span>
          </li>
          <li class="pf-plate cw-frame">
            <span class="pf-plate__face">
              <i aria-hidden="true" class="pi pi-comments pf-plate__icon"></i>
              <span class="pf-plate__value">
                <Skeleton v-if="statsLoading" width="2.5rem" height="2.2rem" />
                <template v-else>{{ stats?.comentarios ?? 0 }}</template>
              </span>
              <span class="pf-plate__label">Reviews</span>
            </span>
          </li>
          <li class="pf-plate cw-frame">
            <span class="pf-plate__face">
              <i aria-hidden="true" class="pi pi-star-fill pf-plate__icon pf-plate__icon--star"></i>
              <span class="pf-plate__value">
                <Skeleton v-if="statsLoading" width="2.5rem" height="2.2rem" />
                <template v-else>{{ stats?.rating_medio ?? '—' }}</template>
              </span>
              <span class="pf-plate__label">Avg. rating</span>
            </span>
          </li>
        </ul>

        <!-- reparto del album por estado -->
        <div class="pf-split">
          <p class="pf-split__total">
            <strong>{{ coleccion.length }}</strong> {{ coleccion.length === 1 ? 'game' : 'games' }} in your album
          </p>
          <div v-if="coleccion.length" class="pf-split__bar" role="img" :aria-label="resumenReparto">
            <span v-for="parte in repartoColeccion" v-show="parte.n > 0" :key="parte.key"
              class="pf-split__seg cw-frame" :class="'cw-frame--' + parte.key" :style="{ flexGrow: parte.n }"></span>
          </div>
          <div v-else class="pf-split__bar pf-split__bar--empty" aria-hidden="true"></div>
          <ul class="pf-split__legend" aria-hidden="true">
            <li v-for="parte in repartoColeccion" :key="parte.key" class="cw-frame" :class="'cw-frame--' + parte.key">
              <span class="pf-split__dot"></span>{{ STATUS_META[parte.key].label }} <strong>{{ parte.n }}</strong>
            </li>
          </ul>
        </div>
      </section>

      <!-- ── COLECCION + FAVORITOS/RESEÑAS ── -->
      <div class="pf-lower">

        <section class="pf-collection" aria-labelledby="pf-col-title">
          <h2 id="pf-col-title" class="cw-h2">Your collection</h2>

          <div class="pf-tabs" role="tablist" aria-label="Filter collection by status">
            <button type="button" role="tab" class="pf-tab cw-frame" :aria-selected="filtroColeccion === 'todos'"
              :tabindex="filtroColeccion === 'todos' ? 0 : -1" @click="filtroColeccion = 'todos'">
              All <span class="pf-tab__count">{{ coleccion.length }}</span>
            </button>
            <button v-for="key in STATUS_LIST" :key="key" type="button" role="tab" class="pf-tab cw-frame"
              :class="'cw-frame--' + key" :aria-selected="filtroColeccion === key"
              :tabindex="filtroColeccion === key ? 0 : -1" @click="filtroColeccion = key">
              <i aria-hidden="true" :class="'pi ' + STATUS_META[key].icon"></i>
              {{ STATUS_META[key].label }}
              <span class="pf-tab__count">{{ coleccionPorEstado[key].length }}</span>
            </button>
          </div>

          <div role="tabpanel" aria-labelledby="pf-col-title">
            <ul v-if="coleccionLoading" class="pf-grid" aria-busy="true">
              <li v-for="n in 6" :key="n"><Skeleton class="pf-card-skel" radius="16px" /></li>
            </ul>

            <div v-else-if="coleccion.length === 0" class="pf-empty">
              <i aria-hidden="true" class="pi pi-bookmark"></i>
              <p>Your album is empty. Favorite a game and set its status to start your collection.</p>
              <router-link to="/content/overview" class="pf-btn pf-btn--ghost pf-btn--sm">Browse the catalog</router-link>
            </div>

            <div v-else-if="coleccionFiltrada.length === 0" class="pf-empty">
              <i aria-hidden="true" :class="'pi ' + STATUS_META[filtroColeccion]?.icon"></i>
              <p>No games marked as {{ STATUS_META[filtroColeccion]?.label.toLowerCase() }}.</p>
            </div>

            <ul v-else class="pf-grid">
              <li v-for="item in coleccionFiltrada" :key="item.game.id">
                <MiniCard
                  :game="item.game"
                  :status="item.status"
                  favorite
                  show-favorite
                  :can-change-status="juegoYaSalio(item.game)"
                  @toggle-favorite="quitarFavorito"
                  @update:status="manejarActualizacionEstado"
                />
              </li>
            </ul>
          </div>
        </section>

        <div class="pf-side">
          <!-- Favoritos: checklist del set -->
          <section class="pf-panel" aria-labelledby="pf-fav-title">
            <h2 id="pf-fav-title" class="pf-panel__title">Favorites <span class="cw-count">{{ favoritos.length }}</span></h2>

            <div v-if="favoritosLoading" class="pf-rows-skel" aria-busy="true">
              <Skeleton v-for="n in 4" :key="n" width="100%" height="48px" radius="8px" />
            </div>
            <p v-else-if="favoritos.length === 0" class="pf-muted">
              No favorites yet. Tap the heart on any game to save it here.
            </p>
            <ul v-else class="pf-rows">
              <li v-for="fav in favoritosPaginados" :key="fav.id" class="pf-row cw-frame"
                :class="statuses.get(fav.id) ? 'cw-frame--' + statuses.get(fav.id) : ''">
                <router-link :to="'/game/' + fav.id" class="pf-row__link">
                  <span class="pf-row__thumb"><GameImage :src="fav.imge_url" alt="" width="160" height="120" /></span>
                  <span class="pf-row__text">
                    <span class="pf-row__name">{{ fav.name }}</span>
                    <span class="pf-row__meta">
                      <span class="pf-row__no">No. {{ fav.id }}</span>
                      <span v-if="statuses.get(fav.id)" class="pf-pill">{{ STATUS_META[statuses.get(fav.id)].label }}</span>
                      <span v-else>No status</span>
                    </span>
                  </span>
                </router-link>
                <button type="button" class="pf-icon-btn" :disabled="remover === fav.id"
                  :aria-label="'Remove ' + fav.name + ' from favorites'" @click="quitarFavorito(fav.id)">
                  <i aria-hidden="true" :class="remover === fav.id ? 'pi pi-spin pi-spinner' : 'pi pi-trash'"></i>
                </button>
              </li>
            </ul>
            <Pagination
              v-if="!favoritosLoading && totalPaginasFavoritos > 1"
              :current-page="paginaFavoritos"
              :total-pages="totalPaginasFavoritos"
              @update:current-page="paginaFavoritos = $event"
            />
          </section>

          <!-- Reseñas propias -->
          <section class="pf-panel" aria-labelledby="pf-rev-title">
            <h2 id="pf-rev-title" class="pf-panel__title">Your reviews <span class="cw-count">{{ misResenas.length }}</span></h2>

            <div v-if="resenasLoading" class="pf-rows-skel" aria-busy="true">
              <Skeleton v-for="n in 3" :key="n" width="100%" height="64px" radius="8px" />
            </div>
            <p v-else-if="misResenas.length === 0" class="pf-muted">
              You haven't reviewed any game yet. Rate one from its page.
            </p>
            <ul v-else class="pf-reviews">
              <li v-for="r in misResenas.slice(0, 5)" :key="r.id_comment" class="pf-review">
                <div class="pf-review__head">
                  <router-link :to="'/game/' + r.id_game_api" class="pf-review__game">
                    {{ nombrePorJuego[r.id_game_api] || 'Game No. ' + r.id_game_api }}
                  </router-link>
                  <span v-if="r.rating" class="pf-review__rating" :aria-label="`Rated ${r.rating} of 5`">
                    <i aria-hidden="true" class="pi pi-star-fill"></i>{{ r.rating }}
                  </span>
                </div>
                <p class="pf-review__body">{{ r.description }}</p>
                <span class="pf-muted pf-review__date">{{ formatearFecha(r.date_of_update || r.date_of_comment) }}</span>
              </li>
            </ul>
          </section>
        </div>
      </div>

      <!-- ── PANEL DE CUENTA ── -->
      <Teleport to="body">
        <Transition name="pf-drawer">
          <div v-if="panelCuenta" class="pf-drawer-overlay cw-scope" @click.self="cerrarPanelCuenta" @keydown.esc="cerrarPanelCuenta">
            <aside id="pf-panel" class="pf-drawer" role="dialog" aria-modal="true" aria-labelledby="pf-panel-title">
              <div class="pf-drawer__head">
                <h2 id="pf-panel-title" class="pf-drawer__title">Account settings</h2>
                <button id="pf-panel-close" type="button" class="pf-icon-btn" aria-label="Close account settings" @click="cerrarPanelCuenta">
                  <i aria-hidden="true" class="pi pi-times"></i>
                </button>
              </div>

              <dl class="pf-info">
                <div><dt>First name</dt><dd>{{ estadoAutenticacion.usuario.name }}</dd></div>
                <div><dt>Last name</dt><dd>{{ estadoAutenticacion.usuario.last_name }}</dd></div>
                <div><dt>Nickname</dt><dd>{{ estadoAutenticacion.usuario.nickname ? '@' + estadoAutenticacion.usuario.nickname : '—' }}</dd></div>
                <div><dt>Email</dt><dd class="pf-info__email">{{ estadoAutenticacion.usuario.email || 'Not provided' }}</dd></div>
              </dl>

              <div class="pf-drawer__actions">
                <button type="button" class="pf-btn pf-btn--primary" @click="editarDesdePanel">
                  <i aria-hidden="true" class="pi pi-pencil"></i>
                  Edit profile
                </button>
                <button type="button" class="pf-btn pf-btn--ghost" @click="contrasenaDesdePanel">
                  <i aria-hidden="true" class="pi pi-lock"></i>
                  Change password
                </button>
              </div>

              <div v-if="esAdministrador" class="pf-drawer__group">
                <h3 class="pf-drawer__sub">Administration</h3>
                <button type="button" class="pf-link-row" @click="irAPanelAdmin">
                  <i aria-hidden="true" class="pi pi-users"></i> Manage users
                </button>
                <button type="button" class="pf-link-row" @click="irAModeracion">
                  <i aria-hidden="true" class="pi pi-comments"></i> Moderate comments
                </button>
              </div>

              <div class="pf-drawer__group">
                <router-link to="/terminos" class="pf-link-row" @click="panelCuenta = false">
                  <i aria-hidden="true" class="pi pi-file"></i> Terms and Conditions
                </router-link>
              </div>
            </aside>
          </div>
        </Transition>
      </Teleport>

      <!-- Modal: editar perfil -->
      <Transition name="modal">
        <div v-if="mostrarModalEditar" class="edit-modal-overlay" @click.self="cerrarModalEditar" @keydown.esc="cerrarModalEditar">
          <div class="edit-modal" role="dialog" aria-modal="true" aria-labelledby="edit-profile-title">
            <div class="edit-modal-header">
              <h3 id="edit-profile-title" class="edit-modal-title">Edit profile</h3>
              <button type="button" class="pf-icon-btn" @click="cerrarModalEditar" aria-label="Close">
                <i aria-hidden="true" class="pi pi-times"></i>
              </button>
            </div>

            <div class="edit-modal-body">
              <div class="form-group">
                <label for="perfil-name" class="form-label">First name</label>
                <input id="perfil-name" name="name" autocomplete="given-name" v-model="formularioEditar.name" type="text"
                  class="form-input" placeholder="Enter your first name…" maxlength="50" :disabled="guardandoEditar" />
              </div>
              <div class="form-group">
                <label for="perfil-last-name" class="form-label">Last name</label>
                <input id="perfil-last-name" name="last_name" autocomplete="family-name" v-model="formularioEditar.last_name"
                  type="text" class="form-input" placeholder="Enter your last name…" maxlength="50" :disabled="guardandoEditar" />
              </div>
              <div class="form-group">
                <label for="perfil-nickname" class="form-label">Nickname</label>
                <div class="input-prefix-wrap">
                  <span class="input-at-prefix" aria-hidden="true">@</span>
                  <input id="perfil-nickname" name="nickname" autocomplete="username" spellcheck="false"
                    v-model="formularioEditar.nickname" type="text" class="form-input form-input--with-prefix"
                    placeholder="your_nickname" maxlength="30" :disabled="guardandoEditar" aria-describedby="perfil-nickname-hint" />
                </div>
                <span id="perfil-nickname-hint" class="form-hint">3–30 characters: letters, numbers and underscores.</span>
              </div>
              <div class="form-group">
                <label for="perfil-email" class="form-label">Email</label>
                <input id="perfil-email" name="email" autocomplete="email" spellcheck="false" type="email"
                  class="form-input" :value="estadoAutenticacion.usuario?.email || 'Not provided'" disabled
                  aria-describedby="perfil-email-hint" />
                <span id="perfil-email-hint" class="form-hint">Your email can't be changed.</span>
              </div>

              <div v-if="errorEditar" class="error-alert" role="alert">
                <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
                {{ errorEditar }}
              </div>
            </div>

            <div class="edit-modal-footer">
              <button type="button" class="pf-btn pf-btn--ghost" @click="cerrarModalEditar" :disabled="guardandoEditar">Cancel</button>
              <button type="button" class="pf-btn pf-btn--primary" @click="guardarCambiosPerfil" :disabled="guardandoEditar">
                <i aria-hidden="true" :class="guardandoEditar ? 'pi pi-spin pi-spinner' : 'pi pi-check'"></i>
                {{ guardandoEditar ? 'Saving…' : 'Save changes' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Modal: cambiar contraseña -->
      <Transition name="modal">
        <div v-if="mostrarModalCambiarContraseña" class="edit-modal-overlay" @click.self="cerrarModalCambiarContraseña" @keydown.esc="cerrarModalCambiarContraseña">
          <div class="edit-modal" role="dialog" aria-modal="true" aria-labelledby="change-password-title">
            <div class="edit-modal-header">
              <h3 id="change-password-title" class="edit-modal-title">Change password</h3>
              <button type="button" class="pf-icon-btn" @click="cerrarModalCambiarContraseña" aria-label="Close">
                <i aria-hidden="true" class="pi pi-times"></i>
              </button>
            </div>

            <div class="edit-modal-body">
              <div class="form-group">
                <label for="pwd-actual" class="form-label">Current password</label>
                <input id="pwd-actual" name="current_password" autocomplete="current-password"
                  v-model="formularioCambiarContraseña.actual" type="password" class="form-input" placeholder="Enter your current password…" />
              </div>
              <div class="form-group">
                <label for="pwd-nueva" class="form-label">New password</label>
                <input id="pwd-nueva" name="new_password" autocomplete="new-password"
                  v-model="formularioCambiarContraseña.nueva" type="password" class="form-input" placeholder="At least 8 characters…" />
              </div>
              <div class="form-group">
                <label for="pwd-confirmar" class="form-label">Confirm new password</label>
                <input id="pwd-confirmar" name="confirm_password" autocomplete="new-password"
                  v-model="formularioCambiarContraseña.confirmar" type="password" class="form-input" placeholder="Repeat your new password…" />
              </div>

              <div v-if="errorCambiarContraseña" class="error-alert" role="alert">
                <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
                {{ errorCambiarContraseña }}
              </div>
            </div>

            <div class="edit-modal-footer">
              <button type="button" class="pf-btn pf-btn--ghost" @click="cerrarModalCambiarContraseña">Cancel</button>
              <button type="button" class="pf-btn pf-btn--primary" @click="guardarCambioContraseña" :disabled="cambiandoContraseña">
                <i aria-hidden="true" :class="cambiandoContraseña ? 'pi pi-spin pi-spinner' : 'pi pi-check'"></i>
                {{ cambiandoContraseña ? 'Updating…' : 'Change password' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import jsPerfil from "./script_perfil.js";
import Skeleton from "../Skeleton/Skeleton.vue";
import GameImage from "../Image/GameImage.vue";
import MiniCard from "../CardWorld/MiniCard.vue";
import Pagination from "../Pagination/Pagination.vue";

export default {
  name: 'perfil',
  components: { Skeleton, GameImage, MiniCard, Pagination },
  mixins: [jsPerfil]
};
</script>

<style scoped src="./style_perfil.css"></style>
