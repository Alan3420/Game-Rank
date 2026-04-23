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
              <h2>{{ estadoAutenticacion.usuario.name }} {{estadoAutenticacion.usuario.last_name}}</h2>
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
          <h3>Mi Actividad</h3>
          <div class="empty-state">
            <i class="pi pi-star text-indigo"></i>
            <p>Aún no has calificado ningún juego.</p>
            <router-link to="/content/overview" class="browse-link">Explorar juegos</router-link>
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
    import "./style_perfil.css";

    export default {
        name: 'perfil',
        mixins: [jsPerfil]
    };
</script>