<template>
  <div class="profile-page">

    <Loader v-if="estadoAutenticacion.cargando" size="large" :fullHeight="true" message="Loading profile..." />

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
              <i :class="esAdministrador ? 'pi pi-crown' : 'pi pi-shield'"></i>
              {{ esAdministrador ? 'Administrator' : 'User' }}
            </span>
          </div>
        </div>
      </div>

      <!-- ── ESTADÍSTICAS ── -->
      <div class="stats-section">
        <div class="stats-grid">

          <div class="stat-card stat-card--green">
            <div class="stat-card__icon"><i class="pi pi-check-circle"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.coleccion?.completado ?? '—' }}</span>
              <span class="stat-card__label">Completed</span>
            </div>
          </div>

          <div class="stat-card stat-card--blue">
            <div class="stat-card__icon"><i class="pi pi-play-circle"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.coleccion?.jugando ?? '—' }}</span>
              <span class="stat-card__label">Playing</span>
            </div>
          </div>

          <div class="stat-card stat-card--amber">
            <div class="stat-card__icon"><i class="pi pi-clock"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.coleccion?.pendiente ?? '—' }}</span>
              <span class="stat-card__label">Pending</span>
            </div>
          </div>

          <div class="stat-card stat-card--pink">
            <div class="stat-card__icon"><i class="pi pi-heart-fill"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.favoritos ?? '—' }}</span>
              <span class="stat-card__label">Favorites</span>
            </div>
          </div>

          <div class="stat-card stat-card--yellow">
            <div class="stat-card__icon"><i class="pi pi-star-fill"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.rating_medio != null ? stats.rating_medio + ' ★' : '—' }}</span>
              <span class="stat-card__label">Average rating</span>
            </div>
          </div>

          <div class="stat-card stat-card--purple">
            <div class="stat-card__icon"><i class="pi pi-comments"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.comentarios ?? '—' }}</span>
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
                <i class="pi pi-user"></i>
                <span>Information</span>
              </div>
              <div class="btn-group" ref="menuEditarRef">
                <button class="btn-edit btn-edit-primary" @click="mostrarMenuEditar = !mostrarMenuEditar">
                  <i class="pi pi-pencil"></i>
                  <i class="pi" :class="mostrarMenuEditar ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
                </button>
                <Transition name="dropdown-edit">
                  <div v-if="mostrarMenuEditar" class="edit-menu-dropdown">
                    <button class="edit-menu-item" @click="abrirModalEditar">
                      <i class="pi pi-pencil"></i>
                      <div class="edit-menu-text">
                        <span class="edit-menu-title">Edit Information</span>
                        <span class="edit-menu-desc">Name and last name</span>
                      </div>
                    </button>
                    <button class="edit-menu-item" @click="abrirModalCambiarContraseña">
                      <i class="pi pi-lock"></i>
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
                <div class="info-icon-wrap"><i class="pi pi-id-card"></i></div>
                <div class="info-body">
                  <span class="info-label">First name</span>
                  <span class="info-value">{{ estadoAutenticacion.usuario.name }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i class="pi pi-id-card"></i></div>
                <div class="info-body">
                  <span class="info-label">Last name</span>
                  <span class="info-value">{{ estadoAutenticacion.usuario.last_name }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i class="pi pi-tag"></i></div>
                <div class="info-body">
                  <span class="info-label">Nickname</span>
                  <span class="info-value info-nickname-value">
                    {{ estadoAutenticacion.usuario.nickname ? '@' + estadoAutenticacion.usuario.nickname : '—' }}
                  </span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i class="pi pi-envelope"></i></div>
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
              <i class="pi pi-shield"></i>
              <span>Terms and Conditions</span>
              <i class="pi pi-arrow-right profile-legal-arrow"></i>
            </router-link>
          </div>

          <!-- Admin Panel -->
          <div v-if="esAdministrador" class="admin-panel">
            <div class="admin-header">
              <div class="admin-title-group">
                <i class="pi pi-sliders-v"></i>
                <h2>Admin Panel</h2>
                <span class="admin-badge">Admin</span>
              </div>
            </div>
            <div class="admin-actions">
              <button class="admin-action-btn" @click="irAPanelAdmin">
                <i class="pi pi-users"></i>
                <div class="admin-btn-content">
                  <span class="admin-btn-title">Manage Users</span>
                  <span class="admin-btn-desc">View, edit and delete users</span>
                </div>
                <i class="pi pi-arrow-right"></i>
              </button>
              <button class="admin-action-btn" @click="irAModeracion">
                <i class="pi pi-comments"></i>
                <div class="admin-btn-content">
                  <span class="admin-btn-title">Moderation</span>
                  <span class="admin-btn-desc">Manage comments</span>
                </div>
                <i class="pi pi-arrow-right"></i>
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
                <i class="pi pi-bookmark-fill"></i>
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

            <Loader v-if="coleccionLoading" message="Loading..." />

            <div v-else-if="coleccion.length === 0" class="coleccion-empty-small">
              <i class="pi pi-bookmark"></i>
              <span>Your collection is empty. Set the status of a game from the catalog.</span>
              <router-link to="/content/overview" class="coleccion-explore-link">Explore</router-link>
            </div>

            <div v-else-if="coleccionFiltrada.length === 0" class="coleccion-empty-small">
              <i :class="'pi ' + STATUS_META[filtroColeccion]?.icon"></i>
              <span>No games in "{{ STATUS_META[filtroColeccion]?.label }}"</span>
            </div>

            <div v-else class="coleccion-grid">
              <div
                v-for="item in coleccionFiltrada"
                :key="item.id_status"
                class="coleccion-item"
                @click="irADetalle(item.game.id)"
              >
                <div class="coleccion-item-thumb">
                  <img v-if="item.game.imge_url" :src="item.game.imge_url" :alt="item.game.name" />
                  <i v-else class="pi pi-gamepad"></i>
                </div>
                <span class="coleccion-item-name">{{ item.game.name }}</span>
                <span
                  class="coleccion-item-status"
                  :style="{ background: STATUS_META[item.status]?.solidBg, color: STATUS_META[item.status]?.solidText }"
                >
                  <i :class="'pi ' + STATUS_META[item.status]?.icon"></i>
                  <span class="status-label">{{ STATUS_META[item.status]?.label }}</span>
                </span>
                <button
                  class="coleccion-item-fav"
                  :class="{ 'is-fav': favoritosIds.has(item.game.id), 'is-loading': favLoadingId === item.game.id }"
                  @click.stop="alternarFavoritoColeccion(item.game.id)"
                  :title="favoritosIds.has(item.game.id) ? 'Remove from favorites' : 'Add to favorites'"
                >
                  <i v-if="favLoadingId === item.game.id" class="pi pi-spin pi-spinner"></i>
                  <i v-else :class="favoritosIds.has(item.game.id) ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- Mis Favoritos -->
          <div class="favorites-section">
            <div class="favorites-header">
              <div class="fav-title-group">
                <i class="pi pi-heart-fill"></i>
                <h2>My Favorites</h2>
                <span class="fav-count">{{ favoritos.length }}</span>
              </div>
            </div>

            <Loader v-if="favoritosLoading" message="Loading your favorites..." />

            <div v-else-if="favoritos.length === 0" class="fav-empty">
              <div class="fav-empty-icon">
                <i class="pi pi-star"></i>
              </div>
              <p>You have no favorites yet</p>
              <span>Explore the catalog and start saving your favorite games.</span>
              <router-link to="/content/overview" class="fav-explore-btn">
                <i class="pi pi-compass"></i>
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
                @click="irADetalle(fav.id)"
                @action="quitarFavorito"
                @update:status="manejarActualizacionEstado"
              />
            </div>

            <div v-if="!favoritosLoading && favoritos.length > FAVS_POR_PAGINA" class="fav-pagination">
              <button
                class="fav-page-btn fav-page-nav"
                :disabled="paginaFavoritos === 1"
                @click="paginaFavoritos--"
                aria-label="Previous page"
              >
                <i class="pi pi-chevron-left"></i>
              </button>

              <button
                v-for="n in totalPaginasFavoritos"
                :key="n"
                class="fav-page-btn"
                :class="{ 'is-active': paginaFavoritos === n }"
                @click="paginaFavoritos = n"
              >{{ n }}</button>

              <button
                class="fav-page-btn fav-page-nav"
                :disabled="paginaFavoritos === totalPaginasFavoritos"
                @click="paginaFavoritos++"
                aria-label="Next page"
              >
                <i class="pi pi-chevron-right"></i>
              </button>
            </div>
          </div>

        </div>
      </div>

      <!-- Modal Editar Perfil -->
      <div v-if="mostrarModalEditar" class="edit-modal-overlay" @click.self="cerrarModalEditar">
        <div class="edit-modal">
          <div class="edit-modal-header">
            <div class="edit-modal-title">
              <div class="edit-modal-icon">
                <i class="pi pi-user-edit"></i>
              </div>
              <div>
                <h3>Edit Profile</h3>
                <span>Update your personal information</span>
              </div>
            </div>
            <button class="edit-modal-close" @click="cerrarModalEditar">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <div class="edit-modal-body">
            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-id-card"></i>
                First Name
              </label>
              <input
                v-model="formularioEditar.name"
                type="text"
                class="form-input"
                placeholder="Enter your first name"
                maxlength="50"
                :disabled="guardandoEditar"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-id-card"></i>
                Last Name
              </label>
              <input
                v-model="formularioEditar.last_name"
                type="text"
                class="form-input"
                placeholder="Enter your last name"
                maxlength="50"
                :disabled="guardandoEditar"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-tag"></i>
                Nickname
              </label>
              <div class="input-prefix-wrap">
                <span class="input-at-prefix">@</span>
                <input
                  v-model="formularioEditar.nickname"
                  type="text"
                  class="form-input form-input--with-prefix"
                  placeholder="tu_nickname"
                  maxlength="30"
                  :disabled="guardandoEditar"
                />
              </div>
              <span class="form-hint">
                <i class="pi pi-info-circle"></i>
                3–30 characters: letters, numbers and underscores (_).
              </span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-envelope"></i>
                Email address
                <span class="form-badge-disabled">Not editable</span>
              </label>
              <input
                type="email"
                class="form-input is-disabled"
                :value="estadoAutenticacion.usuario?.email || 'Not provided'"
                disabled
              />
              <span class="form-hint">
                <i class="pi pi-info-circle"></i>
                Email address cannot be modified.
              </span>
            </div>

            <div v-if="errorEditar" class="error-alert">
              <i class="pi pi-exclamation-circle"></i>
              {{ errorEditar }}
            </div>
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalEditar" :disabled="guardandoEditar">
              Cancel
            </button>
            <button class="btn-save" @click="guardarCambiosPerfil" :disabled="guardandoEditar">
              <i v-if="!guardandoEditar" class="pi pi-check"></i>
              <i v-else class="pi pi-spin pi-spinner"></i>
              {{ guardandoEditar ? 'Saving...' : 'Save changes' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Cambiar Contraseña -->
      <div v-if="mostrarModalCambiarContraseña" class="edit-modal-overlay" @click.self="cerrarModalCambiarContraseña">
        <div class="edit-modal">
          <div class="edit-modal-header">
            <div class="edit-modal-title">
              <div class="edit-modal-icon" style="background: #6366f1; color: white;">
                <i class="pi pi-lock"></i>
              </div>
              <div>
                <h3>Change Password</h3>
                <span>Update your password to keep your account secure</span>
              </div>
            </div>
            <button class="edit-modal-close" @click="cerrarModalCambiarContraseña">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <div class="edit-modal-body">
            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-lock"></i>
                Current Password
              </label>
              <input
                v-model="formularioCambiarContraseña.actual"
                type="password"
                class="form-input"
                placeholder="Enter your current password"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-lock"></i>
                New Password
              </label>
              <input
                v-model="formularioCambiarContraseña.nueva"
                type="password"
                class="form-input"
                placeholder="Enter your new password (min. 8 characters)"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-lock"></i>
                Confirm Password
              </label>
              <input
                v-model="formularioCambiarContraseña.confirmar"
                type="password"
                class="form-input"
                placeholder="Confirm your new password"
              />
            </div>

            <div v-if="errorCambiarContraseña" class="error-alert">
              <i class="pi pi-exclamation-circle"></i>
              {{ errorCambiarContraseña }}
            </div>
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalCambiarContraseña">
              Cancel
            </button>
            <button class="btn-save" @click="guardarCambioContraseña" :disabled="cambiandoContraseña">
              <i v-if="!cambiandoContraseña" class="pi pi-check"></i>
              <i v-else class="pi pi-spin pi-spinner"></i>
              {{ cambiandoContraseña ? 'Updating...' : 'Change Password' }}
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
import Loader from "../Loader/Loader.vue";

export default {
  name: 'perfil',
  components: { GameCard, Loader },
  mixins: [jsPerfil]
};
</script>
<style scoped src="./style_perfil.css"></style>
