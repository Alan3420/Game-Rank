<template>
  <div class="profile-page">

    <div v-if="estadoAutenticacion.usuario">

      <!-- ── HERO BANNER ── -->
      <div class="profile-banner">
        <div class="banner-inner">
          <div class="avatar-circle">
            {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}{{ estadoAutenticacion.usuario.last_name?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="banner-identity">
            <h1>{{ estadoAutenticacion.usuario.name }} {{ estadoAutenticacion.usuario.last_name }}</h1>
            <span class="badge" :class="{ 'badge-admin': isAdmin }">
              <i :class="isAdmin ? 'pi pi-crown' : 'pi pi-shield'"></i>
              {{ isAdmin ? 'Administrador' : 'Usuario' }}
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
              <span class="stat-card__label">Completados</span>
            </div>
          </div>

          <div class="stat-card stat-card--blue">
            <div class="stat-card__icon"><i class="pi pi-play-circle"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.coleccion?.jugando ?? '—' }}</span>
              <span class="stat-card__label">Jugando</span>
            </div>
          </div>

          <div class="stat-card stat-card--amber">
            <div class="stat-card__icon"><i class="pi pi-clock"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.coleccion?.pendiente ?? '—' }}</span>
              <span class="stat-card__label">Pendientes</span>
            </div>
          </div>

          <div class="stat-card stat-card--pink">
            <div class="stat-card__icon"><i class="pi pi-heart-fill"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.favoritos ?? '—' }}</span>
              <span class="stat-card__label">Favoritos</span>
            </div>
          </div>

          <div class="stat-card stat-card--yellow">
            <div class="stat-card__icon"><i class="pi pi-star-fill"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.rating_medio != null ? stats.rating_medio + ' ★' : '—' }}</span>
              <span class="stat-card__label">Rating medio</span>
            </div>
          </div>

          <div class="stat-card stat-card--purple">
            <div class="stat-card__icon"><i class="pi pi-comments"></i></div>
            <div class="stat-card__body">
              <span class="stat-card__value">{{ stats?.comentarios ?? '—' }}</span>
              <span class="stat-card__label">Reseñas</span>
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
                <span>Información</span>
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
                        <span class="edit-menu-title">Editar Información</span>
                        <span class="edit-menu-desc">Nombre y apellidos</span>
                      </div>
                    </button>
                    <button class="edit-menu-item" @click="abrirModalCambiarContraseña">
                      <i class="pi pi-lock"></i>
                      <div class="edit-menu-text">
                        <span class="edit-menu-title">Cambiar Contraseña</span>
                        <span class="edit-menu-desc">Seguridad de tu cuenta</span>
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
                  <span class="info-label">Nombre</span>
                  <span class="info-value">{{ estadoAutenticacion.usuario.name }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i class="pi pi-id-card"></i></div>
                <div class="info-body">
                  <span class="info-label">Apellido</span>
                  <span class="info-value">{{ estadoAutenticacion.usuario.last_name }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon-wrap"><i class="pi pi-envelope"></i></div>
                <div class="info-body">
                  <span class="info-label">Correo electrónico</span>
                  <span class="info-value info-value--small">{{ estadoAutenticacion.usuario.email || 'No proporcionado' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Legal -->
          <div class="profile-legal">
            <router-link to="/terminos" class="profile-legal-link">
              <i class="pi pi-shield"></i>
              <span>Términos y Condiciones</span>
              <i class="pi pi-arrow-right profile-legal-arrow"></i>
            </router-link>
          </div>

          <!-- Admin Panel -->
          <div v-if="isAdmin" class="admin-panel">
            <div class="admin-header">
              <div class="admin-title-group">
                <i class="pi pi-sliders-v"></i>
                <h2>Panel Admin</h2>
                <span class="admin-badge">Admin</span>
              </div>
            </div>
            <div class="admin-actions">
              <button class="admin-action-btn" @click="irAPanelAdmin">
                <i class="pi pi-users"></i>
                <div class="admin-btn-content">
                  <span class="admin-btn-title">Gestionar Usuarios</span>
                  <span class="admin-btn-desc">Ver, editar y eliminar usuarios</span>
                </div>
                <i class="pi pi-arrow-right"></i>
              </button>
              <button class="admin-action-btn" @click="irAModeracion">
                <i class="pi pi-comments"></i>
                <div class="admin-btn-content">
                  <span class="admin-btn-title">Moderación</span>
                  <span class="admin-btn-desc">Gestionar comentarios</span>
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
                <h2>Mi Colección</h2>
                <span class="coleccion-count">{{ coleccion.length }}</span>
              </div>
              <div class="coleccion-tabs">
                <button
                  class="coleccion-tab"
                  :class="{ 'is-active': filtroColeccion === 'todos' }"
                  @click="filtroColeccion = 'todos'"
                >Todos</button>
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

            <Loader v-if="coleccionLoading" message="Cargando..." />

            <div v-else-if="coleccion.length === 0" class="coleccion-empty-small">
              <i class="pi pi-bookmark"></i>
              <span>Tu colección está vacía. Marca el estado de un juego desde el catálogo.</span>
              <router-link to="/content/overview" class="coleccion-explore-link">Explorar</router-link>
            </div>

            <div v-else-if="coleccionFiltrada.length === 0" class="coleccion-empty-small">
              <i :class="'pi ' + STATUS_META[filtroColeccion]?.icon"></i>
              <span>Sin juegos en "{{ STATUS_META[filtroColeccion]?.label }}"</span>
            </div>

            <div v-else class="coleccion-grid">
              <div
                v-for="item in coleccionFiltrada"
                :key="item.id_status"
                class="coleccion-item"
                @click="goToDetail(item.game.id)"
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
                  @click.stop="toggleFavoritoColeccion(item.game.id)"
                  :title="favoritosIds.has(item.game.id) ? 'Quitar de favoritos' : 'Añadir a favoritos'"
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
                <h2>Mis Favoritos</h2>
                <span class="fav-count">{{ favoritos.length }}</span>
              </div>
            </div>

            <Loader v-if="favoritosLoading" message="Cargando tus favoritos..." />

            <div v-else-if="favoritos.length === 0" class="fav-empty">
              <div class="fav-empty-icon">
                <i class="pi pi-star"></i>
              </div>
              <p>Aún no tienes favoritos</p>
              <span>Explora el catálogo y empieza a guardar tus juegos favoritos.</span>
              <router-link to="/content/overview" class="fav-explore-btn">
                <i class="pi pi-compass"></i>
                Explorar juegos
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
                @click="goToDetail(fav.id)"
                @action="quitarFavorito"
                @update:status="handleStatusUpdate"
              />
            </div>

            <div v-if="!favoritosLoading && favoritos.length > FAVS_POR_PAGINA" class="fav-pagination">
              <button
                class="fav-page-btn fav-page-nav"
                :disabled="paginaFavoritos === 1"
                @click="paginaFavoritos--"
                aria-label="Página anterior"
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
                aria-label="Página siguiente"
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
                <h3>Editar Perfil</h3>
                <span>Actualiza tu información personal</span>
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
                Nombre
              </label>
              <input
                v-model="formularioEditar.name"
                type="text"
                class="form-input"
                placeholder="Ingresa tu nombre"
                maxlength="50"
                :disabled="guardandoEditar"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-id-card"></i>
                Apellido
              </label>
              <input
                v-model="formularioEditar.last_name"
                type="text"
                class="form-input"
                placeholder="Ingresa tu apellido"
                maxlength="50"
                :disabled="guardandoEditar"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-envelope"></i>
                Correo electrónico
                <span class="form-badge-disabled">No editable</span>
              </label>
              <input
                type="email"
                class="form-input is-disabled"
                :value="estadoAutenticacion.usuario?.email || 'No proporcionado'"
                disabled
              />
              <span class="form-hint">
                <i class="pi pi-info-circle"></i>
                El correo electrónico no se puede modificar.
              </span>
            </div>

            <div v-if="errorEditar" class="error-alert">
              <i class="pi pi-exclamation-circle"></i>
              {{ errorEditar }}
            </div>
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalEditar" :disabled="guardandoEditar">
              Cancelar
            </button>
            <button class="btn-save" @click="guardarCambiosPerfil" :disabled="guardandoEditar">
              <i v-if="!guardandoEditar" class="pi pi-check"></i>
              <i v-else class="pi pi-spin pi-spinner"></i>
              {{ guardandoEditar ? 'Guardando...' : 'Guardar cambios' }}
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
                <h3>Cambiar Contraseña</h3>
                <span>Actualiza tu contraseña para mantener tu cuenta segura</span>
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
                Contraseña Actual
              </label>
              <input
                v-model="formularioCambiarContraseña.actual"
                type="password"
                class="form-input"
                placeholder="Ingresa tu contraseña actual"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-lock"></i>
                Nueva Contraseña
              </label>
              <input
                v-model="formularioCambiarContraseña.nueva"
                type="password"
                class="form-input"
                placeholder="Ingresa tu nueva contraseña (mín. 8 caracteres)"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="pi pi-lock"></i>
                Confirmar Contraseña
              </label>
              <input
                v-model="formularioCambiarContraseña.confirmar"
                type="password"
                class="form-input"
                placeholder="Confirma tu nueva contraseña"
              />
            </div>

            <div v-if="errorCambiarContraseña" class="error-alert">
              <i class="pi pi-exclamation-circle"></i>
              {{ errorCambiarContraseña }}
            </div>
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalCambiarContraseña">
              Cancelar
            </button>
            <button class="btn-save" @click="guardarCambioContraseña" :disabled="cambiandoContraseña">
              <i v-if="!cambiandoContraseña" class="pi pi-check"></i>
              <i v-else class="pi pi-spin pi-spinner"></i>
              {{ cambiandoContraseña ? 'Actualizando...' : 'Cambiar Contraseña' }}
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Unauthorized -->
    <div v-else class="unauthorized-state">
      <div class="unauthorized-card">
        <div class="lock-icon-wrap">
          <i class="pi pi-lock"></i>
        </div>
        <h2>Acceso Denegado</h2>
        <p>Debes iniciar sesión para ver tu perfil.</p>
        <router-link to="/login" class="login-btn">
          <i class="pi pi-sign-in"></i>
          Iniciar Sesión
        </router-link>
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
