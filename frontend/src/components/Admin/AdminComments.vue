<template>
  <div class="admin-users-page">

    <div class="admin-topbar">
      <div class="topbar-content">
        <button class="back-btn" @click="volver">
          <i class="pi pi-arrow-left"></i>
          Back
        </button>
        <div class="topbar-title">
          <i class="pi pi-comments"></i>
          <h1>Comment Moderation</h1>
        </div>
        <div class="topbar-stats">
          <span class="stat-badge">{{ comentarios.length }} comments</span>
        </div>
      </div>
    </div>

    <div class="admin-container">
      <div class="users-section">
        <div class="section-header">
          <h2>All Comments</h2>
          <div class="filter-group">
            <input
              v-model="filtro"
              type="text"
              placeholder="Search by user or game..."
              class="search-input"
            />
          </div>
        </div>

        <Loader v-if="loading" message="Loading comments..." />

        <div v-else-if="comentariosFiltrados.length > 0" class="users-table-wrap">
          <table class="users-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Game</th>
                <th>Comment</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in comentariosFiltrados" :key="c.id_comment" class="user-row">
                <td class="user-name-cell">
                  <div class="user-avatar">
                    {{ c.username?.charAt(0)?.toUpperCase() }}{{ c.user_last_name?.charAt(0)?.toUpperCase() }}
                  </div>
                  <div class="user-info">
                    <span class="user-fullname">{{ c.username }} {{ c.user_last_name }}</span>
                    <span class="user-nickname">@{{ c.nickname }}</span>
                  </div>
                </td>
                <td>
                  <router-link :to="'/game/' + c.id_game_api" class="game-link" target="_blank">
                    View game
                    <i class="pi pi-external-link" style="font-size:0.75rem"></i>
                  </router-link>
                </td>
                <td class="comment-text-cell">
                  <span class="comment-excerpt" :title="c.description">{{ c.description }}</span>
                </td>
                <td class="user-date">{{ formatearFecha(c.date_of_comment) }}</td>
                <td class="user-actions">
                  <button
                    class="action-btn delete-btn"
                    @click="eliminarComentario(c)"
                    title="Delete comment"
                  >
                    <i class="pi pi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="users-empty">
          <div class="empty-icon"><i class="pi pi-comments"></i></div>
          <p>No matching comments</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jsAdminComments from "./script_AdminComments.js";
import Loader from "../Loader/Loader.vue";

export default {
  name: 'AdminComments',
  components: { Loader },
  mixins: [jsAdminComments]
};
</script>

<style scoped src="./style_AdminUsers.css"></style>
<style scoped>
.comment-text-cell {
  max-width: 340px;
}
.comment-excerpt {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  cursor: default;
}
.game-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
  white-space: nowrap;
}
.game-link:hover {
  text-decoration: underline;
}
</style>
