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
            <router-link to="/" class="browse-link">Explorar juegos</router-link>
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

<script setup>
// Asegúrate de que la ruta de importación coincida con la estructura de tu proyecto
import { estadoAutenticacion } from '../store/autenticacion'; 
</script>

<style scoped>
.profile-page {
  padding: 40px 24px;
  background-color: #f1f5f9; /* Mismo fondo que tu #app */
  min-height: 100%;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header h1 {
  font-size: 2rem;
  color: #1f1f35;
  margin-bottom: 8px;
  font-weight: 800;
}

.page-header p {
  color: #6b7280;
  margin: 0;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Estilos de Tarjetas */
.profile-card, .activity-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  background: #eef2ff;
  color: #6366f1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.user-headline h2 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  color: #1f1f35;
}

.badge {
  background: #eef2ff;
  color: #4f46e5;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 24px 0;
}

.details-section h3, .activity-card h3 {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  color: #1f1f35;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-group .label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-group .value {
  font-size: 1rem;
  color: #1f1f35;
  padding-left: 24px; /* Alineado con el texto, ignorando el icono */
}

.actions-section {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.btn-edit {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1px solid #e5e7eb;
  color: #374151;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

/* Empty state para actividad */
.empty-state {
  text-align: center;
  padding: 32px 0;
  color: #6b7280;
}

.empty-state i {
  font-size: 2.5rem;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-state .text-indigo {
  color: #c7d2fe;
}

.browse-link {
  display: inline-block;
  margin-top: 16px;
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
}

.browse-link:hover {
  text-decoration: underline;
}

/* Estado no autorizado */
.unauthorized-state {
  background: #ffffff;
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.lock-icon {
  font-size: 3rem;
  color: #9ca3af;
  margin-bottom: 16px;
}

.login-btn {
  display: inline-block;
  margin-top: 24px;
  padding: 10px 24px;
  background: #6366f1;
  color: white;
  text-decoration: none;
  font-weight: 600;
  border-radius: 20px;
  transition: background 0.2s;
}

.login-btn:hover {
  background: #4f46e5;
}

/* Responsive */
@media (min-width: 640px) {
  .info-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 24px 16px;
  }
  
  .profile-card, .activity-card {
    padding: 24px;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
  }
  
  .info-group .value {
    padding-left: 0;
  }
}
</style>