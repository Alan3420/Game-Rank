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
            <span class="badge">
              <i class="pi pi-shield"></i>
              Explorador
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
            <button class="btn-edit" @click="abrirModalEditar">
              <i class="pi pi-pencil"></i>
              Editar
            </button>
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
            <div v-for="fav in favoritos" :key="fav.id" class="fav-card">
              <div class="fav-img-wrap">
                <img :src="fav.imge_url" :alt="fav.name" />
                <div class="fav-img-overlay">
                  <div class="fav-rating-badge">
                    <i class="pi pi-star-fill"></i>
                    <span>{{ fav.rating ?? 'N/A' }}</span>
                  </div>
                </div>
                <button
                  class="fav-remove-btn"
                  :class="{ 'is-loading': remover === fav.id }"
                  @click.stop="quitarFavorito(fav.id)"
                  :disabled="remover === fav.id"
                  title="Quitar de favoritos"
                >
                  <i :class="remover === fav.id ? 'pi pi-spin pi-spinner' : 'pi pi-trash'"></i>
                </button>
              </div>
              <div class="fav-info">
                <span class="fav-name">{{ fav.name }}</span>
                <span class="fav-date">
                  <i class="pi pi-calendar"></i>
                  {{ fav.release_date ?? 'N/A' }}
                </span>
              </div>
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

export default {
  name: 'perfil',
  mixins: [jsPerfil]
};
</script>
<style scoped src="./style_perfil.css"></style>