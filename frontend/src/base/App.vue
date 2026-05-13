<template>
  <header class="main-header">
    <div class="header-container">
      <router-link to="/" class="logo-link">
        <img id="logo" src="/src/assets/game_rank_logo.png" alt="Game Rank Logo" />
      </router-link>

      <div v-if="estadoAutenticacion.usuario" class="header-search">
        <i class="pi pi-search header-search-icon"></i>
        <input type="text" v-model="headerSearch" placeholder="Buscar un juego..." class="header-search-input"
          @keyup.enter="submitHeaderSearch" />
      </div>

      <nav class="nav-menu">
        <button class="theme-toggle" @click="toggleTema" :title="tema === 'dark' ? 'Modo claro' : 'Modo oscuro'">
          <i class="pi" :class="tema === 'dark' ? 'pi-sun' : 'pi-moon'"></i>
        </button>

        <template v-if="estadoAutenticacion.usuario">
          <router-link to="/content/overview" class="header-catalog-link">
            <i class="pi pi-th-large"></i>
            <span>Catálogo</span>
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

                <p class="dropdown-section-label">Explorar</p>

                <router-link to="/" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-home"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Inicio</span>
                    <span class="dropdown-item-desc">Volver a la página principal</span>
                  </div>
                </router-link>

                <router-link to="/content/overview" class="dropdown-item dropdown-catalog-mobile" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-th-large"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Catálogo</span>
                    <span class="dropdown-item-desc">Explorar todos los juegos</span>
                  </div>
                </router-link>

                <div class="dropdown-divider"></div>

                <p class="dropdown-section-label">MI CUENTA</p>

                <router-link to="/user/profile" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-id-card"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Perfil</span>
                    <span class="dropdown-item-desc">Ver y editar tu información</span>
                  </div>
                </router-link>

                <div v-if="isAdmin" class="dropdown-divider"></div>

                <p v-if="isAdmin" class="dropdown-section-label">ADMINISTRACIÓN</p>

                <router-link v-if="isAdmin" to="/admin/users" class="dropdown-item" @click="menuAbierto = false">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-users"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Gestionar Usuarios</span>
                    <span class="dropdown-item-desc">Ver y editar usuarios</span>
                  </div>
                </router-link>

                <button v-if="isAdmin" class="dropdown-item" @click="irAConfigAdmin">
                  <div class="dropdown-item-icon">
                    <i class="pi pi-cog"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Configuración</span>
                    <span class="dropdown-item-desc">Ajustes del sistema</span>
                  </div>
                </button>

                <div class="dropdown-divider"></div>

                <p class="dropdown-section-label">OPCIONES</p>

                <button class="dropdown-item dropdown-danger" @click="abrirConfirmEliminar">
                  <div class="dropdown-item-icon dropdown-danger-icon">
                    <i class="pi pi-trash"></i>
                  </div>
                  <div class="dropdown-item-text">
                    <span class="dropdown-item-title">Eliminar cuenta</span>
                    <span class="dropdown-item-desc">Borrar permanentemente tu cuenta</span>
                  </div>
                </button>

                <div class="dropdown-divider"></div>

                <button class="dropdown-item dropdown-logout" @click="manejarCierreSesion">
                  <div class="dropdown-item-icon dropdown-logout-icon">
                    <i class="pi pi-sign-out"></i>
                  </div>
                  <span class="dropdown-item-title">Cerrar sesión</span>
                </button>
              </div>
            </Transition>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link">
            <i class="pi pi-sign-in"></i>
            <span class="btn-text">Iniciar sesión</span>
          </router-link>
          <router-link to="/register" class="nav-link nav-link-primary">
            <i class="pi pi-user-plus"></i>
            <span class="btn-text">Registrarse</span>
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
        <h2>¿Eliminar tu cuenta?</h2>
        <p>Esta acción es <strong>permanente</strong>. Se borrarán todos tus comentarios, valoraciones y favoritos. No
          podrás recuperar tu cuenta.</p>

        <div class="confirm-input-group">
          <label>Escribe <strong>ELIMINAR</strong> para confirmar:</label>
          <input type="text" v-model="confirmTexto" class="confirm-input" placeholder="ELIMINAR"
            :disabled="eliminandoCuenta" />
        </div>

        <div class="confirm-actions">
          <button class="confirm-btn confirm-btn-cancel" @click="cerrarConfirmEliminar" :disabled="eliminandoCuenta">
            Cancelar
          </button>
          <button class="confirm-btn confirm-btn-delete" @click="confirmarEliminarCuenta"
            :disabled="confirmTexto !== 'ELIMINAR' || eliminandoCuenta">
            <i v-if="eliminandoCuenta" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-trash"></i>
            {{ eliminandoCuenta ? 'Eliminando...' : 'Eliminar cuenta' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <footer class="main-footer">
    <div class="footer-container">
      <div class="footer-brand">
        <h3>Game Rank</h3>
        <p>Tu plataforma para descubrir, rankear y coleccionar videojuegos.</p>
      </div>

      <div class="footer-section">
        <h4 class="footer-section-title">Explorar</h4>
        <nav class="footer-nav">
          <RouterLink to="/" class="footer-nav-link">Inicio</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/content/overview" class="footer-nav-link">Catálogo</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/user/profile" class="footer-nav-link">Mi Perfil</RouterLink>
          <RouterLink v-if="isAdmin" to="/admin/users" class="footer-nav-link">Gestión de Usuarios</RouterLink>
        </nav>
      </div>

      <div class="footer-section footer-section--right">
        <div class="footer-author">
          <span class="footer-label">Creado por</span>
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
      <p>&copy; 2026 Game Rank. Todos los derechos reservados.</p>
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