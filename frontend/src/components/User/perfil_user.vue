<template>
  <div class="profile-page">
    <div class="profile-container">

      <div class="page-header">
        <h1>Mi Perfil</h1>
        <p>Gestiona tu información y preferencias en Game Rank</p>
      </div>

      <div v-if="estadoAutenticacion.usuario" class="profile-content">
        <div class="profile-card">
          <div class="avatar-section">
            <div class="avatar-circle">
              <i class="pi pi-user"></i>
            </div>
            <div class="user-headline">
              <h2>{{ estadoAutenticacion.usuario.name }} {{ estadoAutenticacion.usuario.last_name }}</h2>
              <span class="badge">Jugador Registrado</span>
            </div>
          </div>

          <div class="divider"></div>

          <div class="details-section">
            <h3>Información de la Cuenta</h3>

            <div class="info-grid">
              <div class="info-group">
                <span class="label"><i class="pi pi-id-card"></i> Nombre de usuario</span>
                <span class="value">{{ estadoAutenticacion.usuario.name }}</span>
              </div>

              <div class="info-group">
                <span class="label"><i class="pi pi-envelope"></i> Correo electrónico</span>
                <span class="value">{{ estadoAutenticacion.usuario.email || 'No proporcionado' }}</span>
              </div>
            </div>
          </div>

          <div class="actions-section">
            <button class="btn-edit">
              <i class="pi pi-pencil"></i> Editar Perfil
            </button>
          </div>
        </div>

        <div class="activity-card">
          <div class="activity-header">
            <div class="activity-titulo">
              <i class="pi pi-heart"></i>
              <h3>Mis Favoritos</h3>
            </div>
            <span class="activity-count">{{ favoritos.length }}</span>
          </div>

          <div v-if="favoritos.length === 0" class="activity-vacio">
            <div class="activity-vacio-icono">
              <i class="pi pi-star"></i>
            </div>
            <p>Aún no has encontrado ningún juego.</p>
            <span>Explora el catálogo y empieza a valorar tus favoritos.</span>
            <router-link to="/content/overview" class="activity-explorar">
              <i class="pi pi-compass"></i>
              Explorar juegos
            </router-link>
          </div>

          <div v-else class="activity-lista">
            <div v-for="fav in favoritos" :key="fav.id_game" class="activity-item">
              <div class="activity-item-img">
                <img :src="fav.imge_url" :alt="fav.name" />
              </div>
              <div class="activity-item-info">
                <span class="activity-item-nombre">{{ fav.name }}</span>
                <span class="activity-item-fecha">
                  <i class="pi pi-calendar"></i>
                  {{ fav.release_date ?? 'N/A' }}
                </span>
              </div>
              <div class="activity-item-rating">
                <i class="pi pi-star-fill"></i>
                <span>{{ fav.rating ?? 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <div v-else class="unauthorized-state">
        <i class="pi pi-lock lock-icon"></i>
        <h2>Acceso Denegado</h2>
        <p>Debes iniciar sesión para ver tu perfil.</p>
        <router-link to="/login" class="login-btn">Ir a Iniciar Sesión</router-link>
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