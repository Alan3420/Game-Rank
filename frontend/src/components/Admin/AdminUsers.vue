<template>
  <div class="admin card-world">
    <div class="ad-shell">

      <header class="ad-head">
        <div class="ad-head__text">
          <h1 class="ad-title">Users <span class="cw-count">{{ usuarios.length }}</span></h1>
        </div>
        <nav class="ad-nav" aria-label="Administration">
          <router-link to="/admin/users" class="ad-nav__link" aria-current="page">
            <i aria-hidden="true" class="pi pi-users"></i> Users
          </router-link>
          <router-link to="/admin/comments" class="ad-nav__link">
            <i aria-hidden="true" class="pi pi-comments"></i> Comments
          </router-link>
        </nav>
      </header>

      <div class="ad-tools">
        <label class="ad-search">
          <i aria-hidden="true" class="pi pi-search"></i>
          <input v-model="filtro" type="search" name="filtro_usuarios" autocomplete="off"
            aria-label="Search users by name, nickname or email" placeholder="Search by name, nickname or email…" />
        </label>
        <p class="ad-tools__count" aria-live="polite">
          <template v-if="!loading">{{ usuariosFiltrados.length }} of {{ usuarios.length }}</template>
        </p>
      </div>

      <div v-if="loading" class="ad-page" aria-busy="true">
        <div class="ad-skel">
          <Skeleton v-for="n in 6" :key="n" width="100%" height="52px" radius="8px" />
        </div>
      </div>

      <div v-else-if="usuariosFiltrados.length > 0" class="ad-page">
        <table role="table" class="ad-table ad-table--users">
          <thead role="rowgroup">
            <tr role="row">
              <th scope="col" role="columnheader">User</th>
              <th scope="col" role="columnheader">Email</th>
              <th scope="col" role="columnheader">Role</th>
              <th scope="col" role="columnheader">Joined</th>
              <th scope="col" role="columnheader"><span class="sr-only">Actions</span></th>
            </tr>
          </thead>
          <tbody role="rowgroup">
            <tr role="row" v-for="usuario in usuariosFiltrados" :key="usuario.id_user">
              <td role="cell" class="ad-cell-user">
                <span class="ad-user">
                  <span class="ad-avatar" aria-hidden="true">
                    {{ usuario.name?.charAt(0)?.toUpperCase() }}{{ usuario.last_name?.charAt(0)?.toUpperCase() }}
                  </span>
                  <span class="ad-who">
                    <span class="ad-who__name">{{ usuario.name }} {{ usuario.last_name }}</span>
                    <span class="ad-who__handle">@{{ usuario.nickname }}</span>
                  </span>
                </span>
              </td>
              <td role="cell" class="ad-cell-email">{{ usuario.email }}</td>
              <td role="cell" class="ad-cell-role">
                <span class="ad-role" :class="{ 'ad-role--admin': usuario.role === 'admin' }">
                  <i aria-hidden="true" :class="usuario.role === 'admin' ? 'pi pi-crown' : 'pi pi-user'"></i>
                  {{ usuario.role === 'admin' ? 'Administrator' : 'Player' }}
                </span>
              </td>
              <td role="cell" class="ad-cell-date">{{ formatearFecha(usuario.date_of_registration) }}</td>
              <td role="cell" class="ad-cell-actions">
                <button v-if="usuario.role !== 'admin'" type="button" class="ad-btn" @click="promoverAdmin(usuario)"
                  :aria-label="'Make ' + usuario.name + ' an administrator'">
                  Make admin
                </button>
                <button v-else type="button" class="ad-btn" @click="degradarAdmin(usuario)"
                  :aria-label="'Remove administrator role from ' + usuario.name">
                  Remove admin
                </button>
                <button type="button" class="ad-icon-btn ad-icon-btn--danger" @click="eliminarUsuario(usuario)"
                  :aria-label="'Delete ' + usuario.name + ' ' + usuario.last_name">
                  <i aria-hidden="true" class="pi pi-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="ad-empty">
        <i aria-hidden="true" class="pi pi-users"></i>
        <p>{{ filtro ? 'No users match "' + filtro + '".' : 'No users yet.' }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import jsAdminUsers from "./script_AdminUsers.js";
import Skeleton from "../Skeleton/Skeleton.vue";

export default {
  name: 'AdminUsers',
  components: { Skeleton },
  mixins: [jsAdminUsers]
};
</script>

<style scoped src="./style_admin.css"></style>
