<template>
  <div class="profile-page">

    <div v-if="estadoAutenticacion.cargando" aria-busy="true">
      <div class="profile-banner">
        <div class="banner-inner">
          <Skeleton circle width="104px" />
          <div class="banner-identity profile-skel-identity">
            <Skeleton width="260px" height="2.2rem" radius="10px" />
            <Skeleton width="120px" height="0.9rem" />
            <Skeleton width="90px" height="1.5rem" radius="999px" />
          </div>
        </div>
      </div>

      <div class="stats-section">
        <div class="stats-grid">
          <div v-for="n in 6" :key="n" class="stat-card">
            <Skeleton width="42px" height="42px" radius="12px" />
            <div class="profile-skel-stat">
              <Skeleton width="2.5rem" height="1.4rem" />
              <Skeleton width="4.5rem" height="0.7rem" />
            </div>
          </div>
        </div>
      </div>

      <div class="profile-content">
        <aside class="profile-sidebar">
          <div class="profile-card profile-skel-card">
            <Skeleton width="120px" height="1rem" />
            <Skeleton v-for="n in 4" :key="n" width="100%" height="2.6rem" radius="10px" />
          </div>
        </aside>
        <div class="profile-main">
          <div class="favorites-section">
            <Skeleton width="160px" height="1.3rem" class="profile-skel-title" />
            <div class="fav-grid">
              <GameCardSkeleton v-for="n in 4" :key="n" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="estadoAutenticacion.usuario">

      <!-- ── HERO BANNER ── -->
      <div class="profile-banner">
        <div class="banner-inner">
          <div class="avatar-circle">
            {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}{{ estadoAutenticacion.usuario.last_name?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="banner-identity">
            <h1>{{ estadoAutenticacion.usuario.name }} {{ estadoAutenticacion.usuario.last_name }}</h1>
            <span v-if="estadoAutenticacion.usuario.nickname" class="banner-nickname">@{{ estadoAutenticacion.usuario.nickname }}</span>
            <span class="badge" :class="{ 'badge-admin': esAdministrador }">
              <i aria-hidden="true" :class="esAdministrador ? 'pi pi-crown' : 'pi pi-shield'"></i>
              {{ esAdministrador ? 'Administrator' : 'User' }}
            </span>
          </div>
        </div>
      </div>

      <!-- ── ESTADÍSTICAS ── -->
      <div class="stats-section">
        <div class="stats-grid">

          <div class="stat-card stat-card--green">
            <div class="stat-card__icon"><i aria-hidden="true" class="pi pi-check-circle"></i></div>
            <div class="stat-card__body">
              <Skeleton v-if="statsLoading" width="2.5rem" height="1.4rem" />
              <span v-else class="stat-card__value">{{ stats?.coleccion?.completado ?? '—' }}</span>
              <span class="stat-card__label">Completed</span>
            </div>
          </div>

          <div class="stat-card stat-card--blue">
            <div class="stat-card__icon"><i aria-hidden="true" class="pi pi-play-circle"></i></div>
            <div class="stat-card__body">
              <Skeleton v-if="statsLoading" width="2.5rem" height="1.4rem" />
              <span v-else class="stat-card__value">{{ stats?.coleccion?.jugando ?? '—' }}</span>
              <span class="stat-card__label">Playing</span>
            </div>
          </div>

          <div class="stat-card stat-card--amber">
            <div class="stat-card__icon"><i aria-hidden="true" class="pi pi-clock"></i></div>
            <div class="stat-card__body">
              <Skeleton v-if="statsLoading" width="2.5rem" height="1.4rem" />
              <span v-else class="stat-card__value">{{ stats?.coleccion?.pendiente ?? '—' }}</span>
              <span class="stat-card__label">Pending</span>
            </div>
          </div>

          <div class="stat-card stat-card--pink">
            <div class="stat-card__icon"><i aria-hidden="true" class="pi pi-heart-fill"></i></div>
            <div class="stat-card__body">
              <Skeleton v-if="statsLoading" width="2.5rem" height="1.4rem" />
              <span v-else class="stat-card__value">{{ stats?.favoritos ?? '—' }}</span>
              <span class="stat-card__label">Favorites</span>
            </div>
          </div>

          <div class="stat-card stat-card--yellow">
            <div class="stat-card__icon"><i aria-hidden="true" class="pi pi-star-fill"></i></div>
            <div class="stat-card__body">
              <Skeleton v-if="statsLoading" width="2.5rem" height="1.4rem" />
              <span v-else class="stat-card__value">{{ stats?.rating_medio != null ? stats.rating_medio + ' ★' : '—' }}</span>
              <span class="stat-card__label">Average rating</span>
            </div>
          </div>

          <div class="stat-card stat-card--purple">
            <div class="stat-card__icon"><i aria-hidden="true" class="pi pi-comments"></i></div>
            <div class="stat-card__body">
              <Skeleton v-if="statsLoading" width="2.5rem" height="1.4rem" />
              <span v-else class="stat-card__value">{{ stats?.comentarios ?? '—' }}</span>
              <span class="stat-card__label">Reviews</span>
            </div>
          </div>

        </div>
      </div>

      <!-- ── CONTENT GRID ── -->
      <div class="profile-content">

        <!-- ── SIDEBAR ── -->
        <aside class="profile-sidebar">

          <!-- Account Info -->
          <div class="profile-card">
            <div class="card-header">
              <div class="card-header-title">
                <i aria-hidden="true" class="pi pi-user"></i>
                <span>Information</span>
              </div>
              <div class="btn-group" ref="menuEditarRef">
                <button class="btn-edit btn-edit-primary" @click="mostrarMenuEditar = !mostrarMenuEditar"
                  aria-label="Account options" aria-haspopup="menu" :aria-expanded="mostrarMenuEditar">
                  <i aria-hidden="true" class="pi pi-pencil"></i>
                  <i aria-hidden="true" class="pi" :class="mostrarMenuEditar ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
                </button>
                <Transition name="dropdown-edit">
                  <div v-if="mostrarMenuEditar" class="edit-menu-dropdown">
                    <button class="edit-menu-item" @click="abrirModalEditar">
                      <i aria-hidden="true" class="pi pi-pencil"></i>
                      <div class="edit-menu-text">
                        <span class="edit-menu-title">Edit Information</span>
                        <span class="edit-menu-desc">Name and last name</span>
                      </div>
                    </button>
                    <button class="edit-menu-item" @click="abrirModalCambiarContraseña">
                      <i aria-hidden="true" class="pi pi-lock"></i>
                      <div class="edit-menu-text">
                        <span class="edit-menu-title">Change Password</span>
                        <span class="edit-menu-desc">Account security</span>
                      </div>
                    </button>
                  </div>
                </Transition>
              </div>
            </div>
            <div class="info-list">
              <div class="info-item">
                <div class="info-icon-wrap"><i aria-hidden="true" class="pi pi-id-card"></i></div>
                <div class="info-body">
                  <span class="info-label">First name</span>
                  <span class="info-value">{{ estadoAutenticacion.usuario.name }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i aria-hidden="true" class="pi pi-id-card"></i></div>
                <div class="info-body">
                  <span class="info-label">Last name</span>
                  <span class="info-value">{{ estadoAutenticacion.usuario.last_name }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i aria-hidden="true" class="pi pi-tag"></i></div>
                <div class="info-body">
                  <span class="info-label">Nickname</span>
                  <span class="info-value info-nickname-value">
                    {{ estadoAutenticacion.usuario.nickname ? '@' + estadoAutenticacion.usuario.nickname : '—' }}
                  </span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i aria-hidden="true" class="pi pi-envelope"></i></div>
                <div class="info-body">
                  <span class="info-label">Email address</span>
                  <span class="info-value info-value--small">{{ estadoAutenticacion.usuario.email || 'Not provided' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Legal -->
          <div class="profile-legal">
            <router-link to="/terminos" class="profile-legal-link">
              <i aria-hidden="true" class="pi pi-shield"></i>
              <span>Terms and Conditions</span>
              <i aria-hidden="true" class="pi pi-arrow-right profile-legal-arrow"></i>
            </router-link>
          </div>

          <!-- Admin Panel -->
          <div v-if="esAdministrador" class="admin-panel">
            <div class="admin-header">
              <div class="admin-title-group">
                <i aria-hidden="true" class="pi pi-sliders-v"></i>
                <h2>Admin Panel</h2>
                <span class="admin-badge">Admin</span>
              </div>
            </div>
            <div class="admin-actions">
              <button class="admin-action-btn" @click="irAPanelAdmin">
                <i aria-hidden="true" class="pi pi-users"></i>
                <div class="admin-btn-content">
                  <span class="admin-btn-title">Manage Users</span>
                  <span class="admin-btn-desc">View, edit and delete users</span>
                </div>
                <i aria-hidden="true" class="pi pi-arrow-right"></i>
              </button>
              <button class="admin-action-btn" @click="irAModeracion">
                <i aria-hidden="true" class="pi pi-comments"></i>
                <div class="admin-btn-content">
                  <span class="admin-btn-title">Moderation</span>
                  <span class="admin-btn-desc">Manage comments</span>
                </div>
                <i aria-hidden="true" class="pi pi-arrow-right"></i>
              </button>
            </div>
          </div>

        </aside>

        <!-- ── MAIN ── -->
        <div class="profile-main">

          <!-- Mi Colección -->
          <div class="coleccion-section">
            <div class="coleccion-header">
              <div class="coleccion-title-group">
                <i aria-hidden="true" class="pi pi-bookmark-fill"></i>
                <h2>My Collection</h2>
                <span class="coleccion-count">{{ coleccion.length }}</span>
              </div>
              <div class="coleccion-tabs">
                <button
                  class="coleccion-tab"
                  :class="{ 'is-active': filtroColeccion === 'todos' }"
                  @click="filtroColeccion = 'todos'"
                >All</button>
                <button
                  v-for="key in STATUS_LIST"
                  :key="key"
                  class="coleccion-tab"
                  :class="{ 'is-active': filtroColeccion === key }"
                  :style="filtroColeccion === key ? { '--tab-color': STATUS_META[key].solidText, '--tab-bg': STATUS_META[key].solidBg } : {}"
                  @click="filtroColeccion = key"
                >{{ STATUS_META[key].label }}</button>
              </div>
            </div>

            <div v-if="coleccionLoading" class="coleccion-grid" aria-busy="true">
              <div v-for="n in 6" :key="n" class="coleccion-item profile-skel-row">
                <Skeleton width="40px" height="40px" radius="8px" />
                <Skeleton class="coleccion-item-name" height="0.85rem" />
                <Skeleton width="70px" height="22px" radius="999px" />
              </div>
            </div>

            <div v-else-if="coleccion.length === 0" class="coleccion-empty-small">
              <i aria-hidden="true" class="pi pi-bookmark"></i>
              <span>Your collection is empty. Set the status of a game from the catalog.</span>
              <router-link to="/content/overview" class="coleccion-explore-link">Explore</router-link>
            </div>

            <div v-else-if="coleccionFiltrada.length === 0" class="coleccion-empty-small">
              <i aria-hidden="true" :class="'pi ' + STATUS_META[filtroColeccion]?.icon"></i>
              <span>No games in "{{ STATUS_META[filtroColeccion]?.label }}"</span>
            </div>

            <div v-else class="coleccion-grid">
              <div
                v-for="item in coleccionFiltrada"
                :key="item.id_status"
                v-activable
                class="coleccion-item"
                @click="irADetalle(item.game.id)"
              >
                <div class="coleccion-item-thumb">
                  <img v-if="item.game.imge_url" :src="item.game.imge_url" alt="" width="40" height="40" loading="lazy" decoding="async" />
                  <i aria-hidden="true" v-else class="pi pi-gamepad"></i>
                </div>
                <span class="coleccion-item-name">{{ item.game.name }}</span>
                <span
                  class="coleccion-item-status"
                  :style="{ background: STATUS_META[item.status]?.solidBg, color: STATUS_META[item.status]?.solidText }"
                >
                  <i aria-hidden="true" :class="'pi ' + STATUS_META[item.status]?.icon"></i>
                  <span class="status-label">{{ STATUS_META[item.status]?.label }}</span>
                </span>
              </div>
            </div>
          </div>

          <!-- Mis Favoritos -->
          <div class="favorites-section">
            <div class="favorites-header">
              <div class="fav-title-group">
                <i aria-hidden="true" class="pi pi-heart-fill"></i>
                <h2>My Favorites</h2>
                <span class="fav-count">{{ favoritos.length }}</span>
              </div>
            </div>

            <div v-if="favoritosLoading" class="fav-grid" aria-busy="true">
              <GameCardSkeleton v-for="n in 4" :key="n" />
            </div>

            <div v-else-if="favoritos.length === 0" class="fav-empty">
              <div class="fav-empty-icon">
                <i aria-hidden="true" class="pi pi-star"></i>
              </div>
              <p>You have no favorites yet</p>
              <span>Explore the catalog and start saving your favorite games.</span>
              <router-link to="/content/overview" class="fav-explore-btn">
                <i aria-hidden="true" class="pi pi-compass"></i>
                Explore games
              </router-link>
            </div>

            <div v-else class="fav-grid">
              <GameCard
                v-for="(fav, index) in favoritosPaginados"
                :key="fav.id"
                :game="fav"
                :index="index"
                removable
                :is-loading="remover === fav.id"
                :status="statuses.get(fav.id) || null"
                :can-change-status="juegoYaSalio(fav)"
                @click="irADetalle(fav.id)"
                @action="quitarFavorito"
                @update:status="manejarActualizacionEstado"
              />
            </div>

            <Pagination
              v-if="!favoritosLoading"
              :current-page="paginaFavoritos"
              :total-pages="totalPaginasFavoritos"
              @update:current-page="paginaFavoritos = $event"
            />
          </div>

        </div>
      </div>

      <!-- Modal Editar Perfil -->
      <div v-if="mostrarModalEditar" class="edit-modal-overlay" @click.self="cerrarModalEditar">
        <div class="edit-modal" role="dialog" aria-modal="true" aria-labelledby="edit-profile-title">
          <div class="edit-modal-header">
            <div class="edit-modal-title">
              <div class="edit-modal-icon">
                <i aria-hidden="true" class="pi pi-user-edit"></i>
              </div>
              <div>
                <h3 id="edit-profile-title">Edit profile</h3>
                <span>Update your personal information</span>
              </div>
            </div>
            <button class="edit-modal-close" @click="cerrarModalEditar" aria-label="Close">
              <i aria-hidden="true" class="pi pi-times"></i>
            </button>
          </div>

          <div class="edit-modal-body">
            <div class="form-group">
              <label for="perfil-name" class="form-label">
                <i aria-hidden="true" class="pi pi-id-card"></i>
                First Name
              </label>
              <input
                id="perfil-name"
                name="name"
                autocomplete="given-name"
                v-model="formularioEditar.name"
                type="text"
                class="form-input"
                placeholder="Enter your first name…"
                maxlength="50"
                :disabled="guardandoEditar"
              />
            </div>

            <div class="form-group">
              <label for="perfil-last-name" class="form-label">
                <i aria-hidden="true" class="pi pi-id-card"></i>
                Last Name
              </label>
              <input
                id="perfil-last-name"
                name="last_name"
                autocomplete="family-name"
                v-model="formularioEditar.last_name"
                type="text"
                class="form-input"
                placeholder="Enter your last name…"
                maxlength="50"
                :disabled="guardandoEditar"
              />
            </div>

            <div class="form-group">
              <label for="perfil-nickname" class="form-label">
                <i aria-hidden="true" class="pi pi-tag"></i>
                Nickname
              </label>
              <div class="input-prefix-wrap">
                <span class="input-at-prefix">@</span>
                <input
                id="perfil-nickname"
                name="nickname"
                autocomplete="username"
                spellcheck="false"
                  v-model="formularioEditar.nickname"
                  type="text"
                  class="form-input form-input--with-prefix"
                  placeholder="your_nickname"
                  maxlength="30"
                  :disabled="guardandoEditar"
                />
              </div>
              <span class="form-hint">
                <i aria-hidden="true" class="pi pi-info-circle"></i>
                3–30 characters: letters, numbers and underscores (_).
              </span>
            </div>

            <div class="form-group">
              <label for="perfil-email" class="form-label">
                <i aria-hidden="true" class="pi pi-envelope"></i>
                Email address
                <span class="form-badge-disabled">Not editable</span>
              </label>
              <input
                id="perfil-email"
                name="email"
                autocomplete="email"
                spellcheck="false"
                type="email"
                class="form-input is-disabled"
                :value="estadoAutenticacion.usuario?.email || 'Not provided'"
                disabled
              />
              <span class="form-hint">
                <i aria-hidden="true" class="pi pi-info-circle"></i>
                Email address cannot be modified.
              </span>
            </div>

            <div v-if="errorEditar" class="error-alert">
              <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
              {{ errorEditar }}
            </div>
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalEditar" :disabled="guardandoEditar">
              Cancel
            </button>
            <button class="btn-save" @click="guardarCambiosPerfil" :disabled="guardandoEditar">
              <i aria-hidden="true" v-if="!guardandoEditar" class="pi pi-check"></i>
              <i aria-hidden="true" v-else class="pi pi-spin pi-spinner"></i>
              {{ guardandoEditar ? 'Saving…' : 'Save changes' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Cambiar Contraseña -->
      <div v-if="mostrarModalCambiarContraseña" class="edit-modal-overlay" @click.self="cerrarModalCambiarContraseña">
        <div class="edit-modal" role="dialog" aria-modal="true" aria-labelledby="change-password-title">
          <div class="edit-modal-header">
            <div class="edit-modal-title">
              <div class="edit-modal-icon" style="background: #6366f1; color: white;">
                <i aria-hidden="true" class="pi pi-lock"></i>
              </div>
              <div>
                <h3 id="change-password-title">Change password</h3>
                <span>Update your password to keep your account secure</span>
              </div>
            </div>
            <button class="edit-modal-close" @click="cerrarModalCambiarContraseña" aria-label="Close">
              <i aria-hidden="true" class="pi pi-times"></i>
            </button>
          </div>

          <div class="edit-modal-body">
            <div class="form-group">
              <label for="pwd-actual" class="form-label">
                <i aria-hidden="true" class="pi pi-lock"></i>
                Current Password
              </label>
              <input
                id="pwd-actual"
                name="current_password"
                autocomplete="current-password"
                v-model="formularioCambiarContraseña.actual"
                type="password"
                class="form-input"
                placeholder="Enter your current password…"
              />
            </div>

            <div class="form-group">
              <label for="pwd-nueva" class="form-label">
                <i aria-hidden="true" class="pi pi-lock"></i>
                New Password
              </label>
              <input
                id="pwd-nueva"
                name="new_password"
                autocomplete="new-password"
                v-model="formularioCambiarContraseña.nueva"
                type="password"
                class="form-input"
                placeholder="At least 8 characters…"
              />
            </div>

            <div class="form-group">
              <label for="pwd-confirmar" class="form-label">
                <i aria-hidden="true" class="pi pi-lock"></i>
                Confirm Password
              </label>
              <input
                id="pwd-confirmar"
                name="confirm_password"
                autocomplete="new-password"
                v-model="formularioCambiarContraseña.confirmar"
                type="password"
                class="form-input"
                placeholder="Repeat your new password…"
              />
            </div>

            <div v-if="errorCambiarContraseña" class="error-alert">
              <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
              {{ errorCambiarContraseña }}
            </div>
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalCambiarContraseña">
              Cancel
            </button>
            <button class="btn-save" @click="guardarCambioContraseña" :disabled="cambiandoContraseña">
              <i aria-hidden="true" v-if="!cambiandoContraseña" class="pi pi-check"></i>
              <i aria-hidden="true" v-else class="pi pi-spin pi-spinner"></i>
              {{ cambiandoContraseña ? 'Updating…' : 'Change password' }}
            </button>
          </div>
        </div>
      </div>

    </div>


  </div>
</template>


<script>
import jsPerfil from "./script_perfil.js";
import GameCard from "../Cards/GameCard.vue";
import Skeleton from "../Skeleton/Skeleton.vue";
import GameCardSkeleton from "../Skeleton/GameCardSkeleton.vue";
import Pagination from "../Pagination/Pagination.vue";

export default {
  name: 'perfil',
  components: { GameCard, Skeleton, GameCardSkeleton, Pagination },
  mixins: [jsPerfil]
};
</script>
<style scoped src="./style_perfil.css"></style>
