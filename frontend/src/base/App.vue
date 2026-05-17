<template>
  <header class="main-header">
    <div class="header-container">
      <router-link to="/" class="logo-link">
        <img id="logo" src="/src/assets/game_rank_logo.png" alt="Game Rank Logo" />
      </router-link>

      <div v-if="estadoAutenticacion.usuario" class="header-search">
        <i class="pi pi-search header-search-icon"></i>
        <input type="text" v-model="headerSearch" placeholder="Search a game..." class="header-search-input"
          @keyup.enter="submitHeaderSearch" />
      </div>

      <nav class="nav-menu">
        <button class="theme-toggle" @click="toggleTema" :title="tema === 'dark' ? 'Light mode' : 'Dark mode'">
          <i class="pi" :class="tema === 'dark' ? 'pi-sun' : 'pi-moon'"></i>
        </button>

        <template v-if="estadoAutenticacion.cargando">
        </template>

        <template v-else-if="estadoAutenticacion.usuario">
          <router-link to="/content/overview" class="header-catalog-link">
            <i class="pi pi-th-large"></i>
            <span>Catalog</span>
          </router-link>

          <router-link to="/tendencias" class="header-catalog-link header-trends-link">
            <i class="pi pi-chart-line"></i>
            <span>Trends</span>
          </router-link>

          <div class="user-menu" ref="userMenuRef">
            <button @click="menuAbierto = !menuAbierto" class="options-user" :class="{ 'is-active': menuAbierto }">
              <div class="user-avatar-btn">
                {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}
              </div>
              <span class="user-btn-name">{{ estadoAutenticacion.usuario.name }}</span>
              <i class="pi" :class="menuAbierto ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
            </button>

            <Transition name="dropdown">
              <div v-if="menuAbierto" class="user-dropdown">
                <div class="dropdown-header">
                  <div class="dropdown-avatar">
                    {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}{{
                      estadoAutenticacion.usuario.last_name?.charAt(0)?.toUpperCase() }}
                  </div>
                  <div class="dropdown-user-info">
                    <span class="dropdown-name">{{ estadoAutenticacion.usuario.name }} {{
                      estadoAutenticacion.usuario.last_name }}</span>
                    <span class="dropdown-email">{{ estadoAutenticacion.usuario.email }}</span>
                  </div>
                </div>

                <div class="dropdown-divider"></div>

                <p class="dropdown-section-label">Explore</p>

                <router-link to="/" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-home"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Home</span>
                    <span class="dropdown-item-desc">Back to the main page</span>
                  </div>
                </router-link>

                <router-link to="/content/overview" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-th-large"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Catalog</span>
                    <span class="dropdown-item-desc">Explore all games</span>
                  </div>
                </router-link>

                <router-link to="/tendencias" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-chart-line"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Trends</span>
                    <span class="dropdown-item-desc">Most popular in the community</span>
                  </div>
                </router-link>

                <div class="dropdown-divider"></div>

                <p class="dropdown-section-label">MY ACCOUNT</p>

                <router-link to="/user/profile" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-id-card"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Profile</span>
                    <span class="dropdown-item-desc">View and edit your information</span>
                  </div>
                </router-link>

                <div v-if="isAdmin" class="dropdown-divider"></div>

                <p v-if="isAdmin" class="dropdown-section-label">ADMINISTRATION</p>

                <router-link v-if="isAdmin" to="/admin/users" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-users"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Manage Users</span>
                    <span class="dropdown-item-desc">View and edit users</span>
                  </div>
                </router-link>

                <button v-if="isAdmin" class="dropdown-item" @click="irAModeracion">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-comments"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Moderation</span>
                    <span class="dropdown-item-desc">Manage comments</span>
                  </div>
                </button>

                <div class="dropdown-divider"></div>

                <p class="dropdown-section-label">OPTIONS</p>

                <button class="dropdown-item dropdown-danger" @click="abrirConfirmEliminar">
                  <div class="dropdown-item-icon dropdown-danger-icon">
                    <i class="pi pi-trash"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Delete account</span>
                    <span class="dropdown-item-desc">Permanently delete your account</span>
                  </div>
                </button>

                <div class="dropdown-divider"></div>

                <button class="dropdown-item dropdown-logout" @click="manejarCierreSesion">
                  <div class="dropdown-item-icon dropdown-logout-icon">
                    <i class="pi pi-sign-out"></i>
                  </div>
                  <span class="dropdown-item-title">Sign out</span>
                </button>
              </div>
            </Transition>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link">
            <i class="pi pi-sign-in"></i>
            <span class="btn-text">Sign in</span>
          </router-link>
          <router-link to="/register" class="nav-link nav-link-primary">
            <i class="pi pi-user-plus"></i>
            <span class="btn-text">Sign up</span>
          </router-link>
        </template>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <RouterView />
  </main>

  <NotificationToast />

  <Transition name="modal-fade">
    <div v-if="confirmEliminarAbierto" class="confirm-overlay" @click.self="cerrarConfirmEliminar">
      <div class="confirm-modal">
        <div class="confirm-icon-wrap">
          <i class="pi pi-exclamation-triangle"></i>
        </div>
        <h2>Delete your account?</h2>
        <p>This action is <strong>permanent</strong>. All your comments, ratings and favorites will be deleted. You will
          not be able to recover your account.</p>

        <div class="confirm-input-group">
          <label>Type <strong>DELETE</strong> to confirm:</label>
          <input type="text" v-model="confirmTexto" class="confirm-input" placeholder="DELETE"
            :disabled="eliminandoCuenta" />
        </div>

        <div class="confirm-actions">
          <button class="confirm-btn confirm-btn-cancel" @click="cerrarConfirmEliminar" :disabled="eliminandoCuenta">
            Cancel
          </button>
          <button class="confirm-btn confirm-btn-delete" @click="confirmarEliminarCuenta"
            :disabled="confirmTexto !== 'DELETE' || eliminandoCuenta">
            <i v-if="eliminandoCuenta" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-trash"></i>
            {{ eliminandoCuenta ? 'Deleting...' : 'Delete account' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <footer class="main-footer">
    <div class="footer-container">
      <div class="footer-brand">
        <h3>Game Rank</h3>
        <p>Your platform to discover, rank and collect video games.</p>
      </div>

      <div class="footer-section">
        <h4 class="footer-section-title">Explore</h4>
        <nav class="footer-nav">
          <RouterLink to="/" class="footer-nav-link">Home</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/content/overview" class="footer-nav-link">Catalog</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/tendencias" class="footer-nav-link">Trends</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/user/profile" class="footer-nav-link">My Profile</RouterLink>
          <RouterLink v-if="isAdmin" to="/admin/users" class="footer-nav-link">User Management</RouterLink>
        </nav>
      </div>

      <div class="footer-section">
        <h4 class="footer-section-title">Legal</h4>
        <nav class="footer-nav">
          <RouterLink to="/terminos" class="footer-nav-link">Terms and Conditions</RouterLink>
        </nav>
      </div>

      <div class="footer-section footer-section--right">
        <div class="footer-author">
          <span class="footer-label">Created by</span>
          <a href="https://github.com/Alan3420" target="_blank" class="footer-author-link">
            <i class="pi pi-github"></i>
            Alan Novas Mateo
          </a>
        </div>
        <div class="footer-powered">
          <span class="footer-label">Powered by</span>
          <a href="https://rawg.io" target="_blank" class="footer-link">
            <i class="pi pi-external-link"></i>
            RAWG
          </a>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 Game Rank. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
import jsApp from "./script_app.js";
import NotificationToast from '../components/Notifications/NotificationToast.vue';

export default {
  name: 'App',
  components: { NotificationToast },
  mixins: [jsApp]
};
</script>

<style scoped src="./style_app.css"></style>