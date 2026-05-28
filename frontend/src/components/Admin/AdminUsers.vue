<template>
  <div class="admin-users-page">
    <!-- Topbar -->
    <div class="admin-topbar">
      <div class="topbar-content">
        <button class="back-btn" @click="volver">
          <i class="pi pi-arrow-left"></i>
          Back
        </button>
        <div class="topbar-title">
          <i class="pi pi-users"></i>
          <h1>User Management</h1>
        </div>
        <div class="topbar-stats">
          <span class="stat-badge">{{ usuarios.length }} registered users</span>
        </div>
      </div>
    </div>

    <!-- Contenido -->
    <div class="admin-container">
      <!-- Header de tabla -->
      <div class="users-section">
        <div class="section-header">
          <h2>User List</h2>
          <div class="filter-group">
            <input
              v-model="filtro"
              type="text"
              placeholder="Search by name or email..."
              class="search-input"
            />
          </div>
        </div>

        <!-- Loader -->
        <Loader v-if="loading" message="Loading users..." />

        <!-- Tabla de usuarios -->
        <div v-else-if="usuarios.length > 0" class="users-table-wrap">
          <table class="users-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Registration Date</th>
                <th>Actions</th>
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
                    <span class="user-nickname">@{{ usuario.nickname }}</span>
                  </div>
                </td>
                <td class="user-email">{{ usuario.email }}</td>
                <td class="user-role">
                  <span class="role-badge" :class="{ 'role-admin': usuario.role === 'admin' }">
                    {{ usuario.role === 'admin' ? 'Administrator' : 'User' }}
                  </span>
                </td>
                <td class="user-date">{{ formatearFecha(usuario.date_of_registration) }}</td>
                <td class="user-actions">
                  <button
                    v-if="usuario.role !== 'admin'"
                    class="action-btn promote-btn"
                    @click="promoverAdmin(usuario)"
                    title="Promote to admin"
                  >
                    <i class="pi pi-arrow-up"></i>
                  </button>
                  <button
                    v-else
                    class="action-btn demote-btn"
                    @click="degradarAdmin(usuario)"
                    title="Demote to user"
                  >
                    <i class="pi pi-arrow-down"></i>
                  </button>
                  <button
                    class="action-btn delete-btn"
                    @click="eliminarUsuario(usuario)"
                    title="Delete user"
                  >
                    <i class="pi pi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Estado vacío -->
        <div v-else-if="!loading" class="users-empty">
          <div class="empty-icon">
            <i class="pi pi-users"></i>
          </div>
          <p>No users match the search</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jsAdminUsers from "./script_AdminUsers.js";
import Loader from "../Loader/Loader.vue";

export default {
  name: 'AdminUsers',
  components: { Loader },
  mixins: [jsAdminUsers]
};
</script>

<style scoped src="./style_AdminUsers.css"></style>