<template>
  <div class="admin card-world">
    <div class="ad-shell">

      <header class="ad-head">
        <div class="ad-head__text">
          <h1 class="ad-title">Comments <span class="cw-count">{{ comentarios.length }}</span></h1>
        </div>
        <nav class="ad-nav" aria-label="Administration">
          <router-link to="/admin/users" class="ad-nav__link">
            <i aria-hidden="true" class="pi pi-users"></i> Users
          </router-link>
          <router-link to="/admin/comments" class="ad-nav__link" aria-current="page">
            <i aria-hidden="true" class="pi pi-comments"></i> Comments
          </router-link>
        </nav>
      </header>

      <div class="ad-tools">
        <label class="ad-search">
          <i aria-hidden="true" class="pi pi-search"></i>
          <input v-model="filtro" type="search" name="filtro_comentarios" autocomplete="off"
            aria-label="Search comments by user, game number or text" placeholder="Search by user, game No. or text…" />
        </label>
        <p class="ad-tools__count" aria-live="polite">
          <template v-if="!loading">{{ comentariosFiltrados.length }} of {{ comentarios.length }}</template>
        </p>
      </div>

      <div v-if="loading" class="ad-page" aria-busy="true">
        <div class="ad-skel">
          <Skeleton v-for="n in 6" :key="n" width="100%" height="60px" radius="8px" />
        </div>
      </div>

      <div v-else-if="comentariosFiltrados.length > 0" class="ad-page">
        <table role="table" class="ad-table ad-table--comments">
          <thead role="rowgroup">
            <tr role="row">
              <th scope="col" role="columnheader">User</th>
              <th scope="col" role="columnheader">Game</th>
              <th scope="col" role="columnheader">Comment</th>
              <th scope="col" role="columnheader">Date</th>
              <th scope="col" role="columnheader"><span class="sr-only">Actions</span></th>
            </tr>
          </thead>
          <tbody role="rowgroup">
            <tr role="row" v-for="c in comentariosFiltrados" :key="c.id_comment">
              <td role="cell" class="ad-cell-user">
                <span class="ad-user">
                  <span class="ad-avatar" aria-hidden="true">
                    {{ c.username?.charAt(0)?.toUpperCase() }}{{ c.user_last_name?.charAt(0)?.toUpperCase() }}
                  </span>
                  <span class="ad-who">
                    <span class="ad-who__name">{{ c.username }} {{ c.user_last_name }}</span>
                    <span class="ad-who__handle">@{{ c.nickname }}</span>
                  </span>
                </span>
              </td>
              <td role="cell" class="ad-cell-game">
                <router-link :to="'/game/' + c.id_game_api" class="ad-game" target="_blank"
                  :aria-label="'Open game No. ' + c.id_game_api + ' in a new tab'">
                  No. {{ c.id_game_api }}
                  <i aria-hidden="true" class="pi pi-external-link"></i>
                </router-link>
              </td>
              <td role="cell" class="ad-cell-text">
                <span v-if="c.rating" class="ad-rating" :aria-label="'Rated ' + c.rating + ' of 5'">
                  <i aria-hidden="true" class="pi pi-star-fill"></i>{{ c.rating }}
                </span>
                <span class="ad-excerpt">{{ c.description }}</span>
              </td>
              <td role="cell" class="ad-cell-date">{{ formatearFecha(c.date_of_comment) }}</td>
              <td role="cell" class="ad-cell-actions">
                <button type="button" class="ad-icon-btn ad-icon-btn--danger" @click="eliminarComentario(c)"
                  :aria-label="'Delete comment by ' + c.username">
                  <i aria-hidden="true" class="pi pi-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="ad-empty">
        <i aria-hidden="true" class="pi pi-comments"></i>
        <p>{{ filtro ? 'No comments match "' + filtro + '".' : 'No comments yet.' }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import jsAdminComments from "./script_AdminComments.js";
import Skeleton from "../Skeleton/Skeleton.vue";

export default {
  name: 'AdminComments',
  components: { Skeleton },
  mixins: [jsAdminComments]
};
</script>

<style scoped src="./style_admin.css"></style>
