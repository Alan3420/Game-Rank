<template>
  <div class="admin-users-page">
    <!-- Topbar -->
    <div class="admin-topbar">
      <div class="topbar-content">
        <button class="back-btn" @click="goBack">
          <i class="pi pi-arrow-left"></i>
          Volver
        </button>
        <div class="topbar-title">
          <i class="pi pi-users"></i>
          <h1>Gestión de Usuarios</h1>
        </div>
        <div class="topbar-stats">
          <span class="stat-badge">{{ usuarios.length }} usuarios registrados</span>
        </div>
      </div>
    </div>

    <!-- Contenido -->
    <div class="admin-container">
      <!-- Header de tabla -->
      <div class="users-section">
        <div class="section-header">
          <h2>Lista de Usuarios</h2>
          <div class="filter-group">
            <input
              v-model="filtro"
              type="text"
              placeholder="Buscar por nombre o email..."
              class="search-input"
            />
          </div>
        </div>

        <!-- Tabla de usuarios -->
        <div v-if="usuarios.length > 0" class="users-table-wrap">
          <table class="users-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Fecha de Registro</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="usuario in usuariosFiltrados" :key="usuario.id_user" class="user-row">
                <td class="user-name-cell">
                  <div class="user-avatar">
                    {{ usuario.name?.charAt(0)?.toUpperCase() }}{{ usuario.last_name?.charAt(0)?.toUpperCase() }}
                  </div>
                  <div class="user-info">
                    <span class="user-fullname">{{ usuario.name }} {{ usuario.last_name }}</span>
                  </div>
                </td>
                <td class="user-email">{{ usuario.email }}</td>
                <td class="user-role">
                  <span class="role-badge" :class="{ 'role-admin': usuario.role === 'admin' }">
                    {{ usuario.role === 'admin' ? 'Administrador' : 'Usuario' }}
                  </span>
                </td>
                <td class="user-date">{{ formatDate(usuario.date_of_registration) }}</td>
                <td class="user-actions">
                  <button
                    v-if="usuario.role !== 'admin'"
                    class="action-btn promote-btn"
                    @click="promoverAdmin(usuario)"
                    title="Promover a admin"
                  >
                    <i class="pi pi-arrow-up"></i>
                  </button>
                  <button
                    v-else
                    class="action-btn demote-btn"
                    @click="degradarAdmin(usuario)"
                    title="Degradar a usuario"
                  >
                    <i class="pi pi-arrow-down"></i>
                  </button>
                  <button
                    class="action-btn delete-btn"
                    @click="eliminarUsuario(usuario)"
                    title="Eliminar usuario"
                  >
                    <i class="pi pi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Estado vacío -->
        <div v-else class="users-empty">
          <div class="empty-icon">
            <i class="pi pi-users"></i>
          </div>
          <p>No hay usuarios que coincidan con la búsqueda</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jsAdminUsers from "./script_AdminUsers.js";

export default {
  name: 'AdminUsers',
  mixins: [jsAdminUsers]
};
</script>

<style scoped src="./style_AdminUsers.css"></style>