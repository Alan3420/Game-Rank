<template>
  <div class="profile-page">

    <div v-if="estadoAutenticacion.usuario">

      <!-- Banner -->
      <div class="profile-banner">
        <div class="banner-glow"></div>
        <div class="banner-inner">
          <div class="avatar-wrapper">
            <div class="avatar-circle">
              {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}{{ estadoAutenticacion.usuario.last_name?.charAt(0)?.toUpperCase() }}
            </div>
          </div>
          <div class="banner-user-info">
            <h1>{{ estadoAutenticacion.usuario.name }} {{ estadoAutenticacion.usuario.last_name }}</h1>
            <span class="badge" :class="{ 'badge-admin': isAdmin }">
              <i :class="isAdmin ? 'pi pi-crown' : 'pi pi-shield'"></i>
              {{ isAdmin ? 'Administrador' : 'Usuario' }}
            </span>
          </div>
        </div>
      </div>

      <div class="profile-container">

        <!-- Account info -->
        <div class="profile-card">
          <div class="card-header">
            <div class="card-header-title">
              <i class="pi pi-user"></i>
              <span>Información de la Cuenta</span>
            </div>
            <div class="btn-group" ref="menuEditarRef">
              <button class="btn-edit btn-edit-primary" @click="mostrarMenuEditar = !mostrarMenuEditar">
                <i class="pi pi-sliders-v"></i>
                <span>Editar Perfil</span>
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

          <div class="info-grid">
            <div class="info-item">
              <div class="info-icon-wrap">
                <i class="pi pi-id-card"></i>
              </div>
              <div class="info-body">
                <span class="info-label">Nombre de usuario</span>
                <span class="info-value">{{ estadoAutenticacion.usuario.name }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon-wrap">
                <i class="pi pi-envelope"></i>
              </div>
              <div class="info-body">
                <span class="info-label">Correo electrónico</span>
                <span class="info-value">{{ estadoAutenticacion.usuario.email || 'No proporcionado' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Favorites -->
        <div class="favorites-section">
          <div class="favorites-header">
            <div class="fav-title-group">
              <i class="pi pi-heart-fill"></i>
              <h2>Mis Favoritos</h2>
              <span class="fav-count">{{ favoritos.length }}</span>
            </div>
          </div>

          <div v-if="favoritos.length === 0" class="fav-empty">
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
              v-for="fav in favoritos"
              :key="fav.id"
              :game="fav"
              removable
              :is-loading="remover === fav.id"
              @click="goToDetail(fav.id)"
              @action="quitarFavorito"
            />
          </div>
        </div>

        <!-- Admin Panel (solo visible para admins) -->
        <div v-if="isAdmin" class="admin-panel">
          <div class="admin-header">
            <div class="admin-title-group">
              <i class="pi pi-sliders-v"></i>
              <h2>Panel de Administración</h2>
              <span class="admin-badge">Admin</span>
            </div>
            <p class="admin-subtitle">Acceso a herramientas exclusivas de administrador</p>
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

            <button class="admin-action-btn" @click="irAConfigAdmin">
              <i class="pi pi-cog"></i>
              <div class="admin-btn-content">
                <span class="admin-btn-title">Configuración</span>
                <span class="admin-btn-desc">Ajustes del sistema</span>
              </div>
              <i class="pi pi-arrow-right"></i>
            </button>
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
                Nombre de usuario
              </label>
              <input
                type="text"
                class="form-input"
                :value="estadoAutenticacion.usuario?.name"
                placeholder="Ingresa tu nombre"
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
          </div>

          <div class="edit-modal-footer">
            <button class="btn-cancel" @click="cerrarModalEditar">
              Cancelar
            </button>
            <button class="btn-save">
              <i class="pi pi-check"></i>
              Guardar cambios
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

export default {
  name: 'perfil',
  components: { GameCard },
  mixins: [jsPerfil]
};
</script>
<style scoped src="./style_perfil.css"></style>