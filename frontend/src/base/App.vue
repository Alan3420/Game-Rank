<template>
  <a href="#contenido" class="skip-link">Skip to content</a>

  <header class="main-header cw-scope">
    <div class="header-container">
      <router-link to="/" class="logo-link" aria-label="Game Rank home">
        <!-- Logo "Card G": el marco de la carta forma la G. Fuente en assets/brand/ -->
        <svg class="logo-symbol" viewBox="42 0 172 256" width="172" height="256" aria-hidden="true" focusable="false">
          <path fill="currentColor" d="M74 10 H182 A32 32 0 0 1 214 42 V74 H178 V52 A8 8 0 0 0 170 44 H86 A8 8 0 0 0 78 52 V204 A8 8 0 0 0 86 212 H170 A8 8 0 0 0 178 204 V154 H126 V120 H214 V214 A32 32 0 0 1 182 246 H74 A32 32 0 0 1 42 214 V42 A32 32 0 0 1 74 10 Z" />
        </svg>
        <svg class="logo-wordmark" viewBox="0 0 665 256" width="665" height="256" aria-hidden="true" focusable="false">
          <path fill="currentColor" d="M4.2 152.8V103Q4.2 89.1 13 80.9Q21.8 72.8 36.4 72.8Q51.1 72.8 59.9 81.1Q68.8 89.4 68.8 103.3V109Q68.8 109.8 68.3 110.3Q67.7 110.9 67 110.9H45.1Q44.3 110.9 43.7 110.3Q43.2 109.8 43.2 109V103Q43.2 99.3 41.3 97Q39.5 94.7 36.4 94.7Q33.5 94.7 31.6 97Q29.8 99.3 29.8 103V153Q29.8 156.7 31.6 159Q33.5 161.3 36.4 161.3Q39.5 161.3 41.3 159Q43.2 156.7 43.2 153V143.1Q43.2 142.3 42.4 142.3H38.4Q37.6 142.3 37.1 141.8Q36.6 141.3 36.6 140.5V124.1Q36.6 123.4 37.1 122.8Q37.6 122.3 38.4 122.3H67Q67.7 122.3 68.3 122.8Q68.8 123.4 68.8 124.1V152.8Q68.8 166.7 59.9 175Q51.1 183.2 36.4 183.2Q21.8 183.2 13 175Q4.2 166.7 4.2 152.8Z M125.3 180.3 123.3 166.9Q123.3 166.1 122.3 166.1H105.7Q104.8 166.1 104.8 166.9L102.9 180.3Q102.8 182 100.9 182H79Q77 182 77.5 180L99.8 75.7Q100.1 74 101.8 74H127Q128.7 74 129 75.7L151.2 180L151.4 180.6Q151.4 182 149.7 182H127.3Q125.4 182 125.3 180.3ZM108.8 146.4H119.1Q119.7 146.4 119.7 145.6L114.2 110.4Q114 109.8 113.7 109.8Q113.4 109.8 113.2 110.4L108.2 145.6Q108.2 146.4 108.8 146.4Z M213.7 74H235.1Q235.9 74 236.4 74.5Q237 75.1 237 75.9V180.1Q237 180.9 236.4 181.5Q235.9 182 235.1 182H213.2Q212.5 182 211.9 181.5Q211.4 180.9 211.4 180.1V114Q211.4 113.3 211.1 113.3Q210.8 113.2 210.4 113.7L199.6 132.5Q199 133.7 198.7 133.7Q198.4 133.7 197.6 132.5L186.8 113.7Q186.5 113.2 186.2 113.2Q185.9 113.2 185.9 113.8V180.1Q185.9 180.9 185.4 181.5Q184.8 182 184.1 182H162.2Q161.4 182 160.8 181.5Q160.3 180.9 160.3 180.1V75.9Q160.3 75.1 160.8 74.5Q161.4 74 162.2 74H183.8Q185.3 74 186.1 75.2L198.4 97.6Q198.9 98.2 199.3 97.6L211.4 75.2Q212 74 213.7 74Z M306.7 95.9H275.7Q274.9 95.9 274.9 96.7V116.1Q274.9 116.9 275.7 116.9H292.7Q293.5 116.9 294 117.4Q294.5 118 294.5 118.7V137.1Q294.5 137.9 294 138.4Q293.5 139 292.7 139H275.7Q274.9 139 274.9 139.7V159.3Q274.9 160.1 275.7 160.1H306.7Q307.5 160.1 308 160.6Q308.6 161.2 308.6 161.9V180.1Q308.6 180.9 308 181.5Q307.5 182 306.7 182H251.2Q250.4 182 249.9 181.5Q249.3 180.9 249.3 180.1V75.9Q249.3 75.1 249.9 74.5Q250.4 74 251.2 74H306.7Q307.5 74 308 74.5Q308.6 75.1 308.6 75.9V94.1Q308.6 94.8 308 95.4Q307.5 95.9 306.7 95.9Z M392.5 180.5 382 139.6Q381.9 139 381.2 139H378.9Q378.2 139 378.2 139.7V180.1Q378.2 180.9 377.6 181.5Q377.1 182 376.3 182H354.4Q353.6 182 353.1 181.5Q352.5 180.9 352.5 180.1V75.9Q352.5 75.1 353.1 74.5Q353.6 74 354.4 74H387.6Q396.5 74 403.5 78.2Q410.4 82.5 414.2 90.1Q418 97.8 418 107.5Q418 116.1 414.8 123Q411.6 129.9 405.9 134Q405.6 134.2 405.5 134.4Q405.3 134.6 405.5 134.9L418.7 179.8L418.9 180.5Q418.9 182 417.2 182H394.7Q393 182 392.5 180.5ZM378.2 96.7V118.6Q378.2 119.4 378.9 119.4H383.2Q387.4 119.4 389.9 116.3Q392.3 113.2 392.3 107.8Q392.3 102.1 389.9 99Q387.4 95.9 383.2 95.9H378.9Q378.2 95.9 378.2 96.7Z M473.7 180.3 471.7 166.9Q471.7 166.1 470.7 166.1H454.1Q453.1 166.1 453.1 166.9L451.3 180.3Q451.1 182 449.3 182H427.4Q425.4 182 425.8 180L448.2 75.7Q448.5 74 450.2 74H475.4Q477.1 74 477.4 75.7L499.6 180L499.7 180.6Q499.7 182 498 182H475.7Q473.8 182 473.7 180.3ZM457.1 146.4H467.5Q468.1 146.4 468.1 145.6L462.5 110.4Q462.4 109.8 462.1 109.8Q461.8 109.8 461.6 110.4L456.5 145.6Q456.5 146.4 457.1 146.4Z M555.7 74H577.3Q578.1 74 578.6 74.5Q579.2 75.1 579.2 75.9V180.1Q579.2 180.9 578.6 181.5Q578.1 182 577.3 182H552.8Q551.1 182 550.6 180.5L535.4 126.8Q535.2 126.3 534.8 126.2Q534.4 126.1 534.4 126.8L534.8 180.1Q534.8 180.9 534.2 181.5Q533.7 182 532.9 182H511.3Q510.5 182 510 181.5Q509.5 180.9 509.5 180.1V75.9Q509.5 75.1 510 74.5Q510.5 74 511.3 74H535.5Q537.2 74 537.7 75.5L553.1 129.5Q553.3 130 553.7 130Q554 130 554 129.4L553.9 75.9Q553.9 75.1 554.4 74.5Q555 74 555.7 74Z M592.1 180.1V75.9Q592.1 75.1 592.7 74.5Q593.2 74 594 74H615.9Q616.7 74 617.2 74.5Q617.8 75.1 617.8 75.9V110.7Q617.8 111.3 618.1 111.3Q618.4 111.3 618.7 110.9L634.9 75.4Q635.5 74 637 74H660.2Q661.3 74 661.7 74.5Q662 75.1 661.6 76.2L639.2 121.5Q639.1 122.1 639.1 122.4L662.5 179.8Q662.7 180.1 662.7 180.8Q662.7 182 661.1 182H637.8Q636.1 182 635.7 180.6L621.8 144.5Q621.6 144 621.3 144Q621 144 620.7 144.5L617.9 150.1Q617.8 150.4 617.8 151V180.1Q617.8 180.9 617.2 181.5Q616.7 182 615.9 182H594Q593.2 182 592.7 181.5Q592.1 180.9 592.1 180.1Z" />
        </svg>
      </router-link>

      <div v-if="estadoAutenticacion.usuario" class="header-search">
        <i aria-hidden="true" class="pi pi-search header-search-icon"></i>
        <input type="search" name="q" autocomplete="off" aria-label="Search games" v-model="headerSearch"
          placeholder="Search a game…" class="header-search-input"
          @keyup.enter="enviarBusquedaCabecera" />
      </div>

      <nav class="nav-menu">
        <button type="button" class="theme-toggle" @click="cambiarTema" :title="tema === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
          :aria-label="tema === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'">
          <i aria-hidden="true" class="pi" :class="tema === 'dark' ? 'pi-sun' : 'pi-moon'"></i>
        </button>

        <template v-if="estadoAutenticacion.cargando">
          <Skeleton class="header-skel-link" width="92px" height="36px" radius="10px" />
          <Skeleton class="header-skel-link" width="84px" height="36px" radius="10px" />
          <Skeleton width="130px" height="42px" radius="10px" />
        </template>

        <template v-else-if="estadoAutenticacion.usuario">
          <router-link to="/content/overview" class="header-catalog-link">
            <i aria-hidden="true" class="pi pi-th-large"></i>
            <span>Catalog</span>
          </router-link>

          <router-link to="/tendencias" class="header-catalog-link header-trends-link">
            <i aria-hidden="true" class="pi pi-chart-line"></i>
            <span>Trends</span>
          </router-link>

          <div class="user-menu" ref="userMenuRef">
            <button type="button" @click="menuAbierto = !menuAbierto" class="options-user" :class="{ 'is-active': menuAbierto }"
              aria-haspopup="menu" :aria-expanded="menuAbierto"
              :aria-label="estadoAutenticacion.usuario.name + ', account menu'">
              <div class="user-avatar-btn">
                {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}
              </div>
              <span class="user-btn-name">{{ estadoAutenticacion.usuario.name }}</span>
              <i aria-hidden="true" class="pi" :class="menuAbierto ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
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

                <div class="dropdown-group">
                  <router-link to="/user/profile" class="dropdown-item" @click="menuAbierto = false">
                    <i aria-hidden="true" class="pi pi-id-card dropdown-item-icon"></i>
                    <span class="dropdown-item-title">Profile</span>
                  </router-link>
                </div>

                <div v-if="esAdministrador" class="dropdown-group">
                  <p class="dropdown-section-label">Administration</p>
                  <router-link to="/admin/users" class="dropdown-item" @click="menuAbierto = false">
                    <i aria-hidden="true" class="pi pi-users dropdown-item-icon"></i>
                    <span class="dropdown-item-title">Manage users</span>
                  </router-link>
                  <button type="button" class="dropdown-item" @click="irAModeracion">
                    <i aria-hidden="true" class="pi pi-comments dropdown-item-icon"></i>
                    <span class="dropdown-item-title">Moderate comments</span>
                  </button>
                </div>

                <div class="dropdown-group">
                  <button type="button" class="dropdown-item dropdown-danger" @click="abrirConfirmEliminar">
                    <i aria-hidden="true" class="pi pi-trash dropdown-item-icon"></i>
                    <span class="dropdown-item-title">Delete account</span>
                  </button>
                  <button type="button" class="dropdown-item" @click="manejarCierreSesion">
                    <i aria-hidden="true" class="pi pi-sign-out dropdown-item-icon"></i>
                    <span class="dropdown-item-title">Sign out</span>
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link">
            <i aria-hidden="true" class="pi pi-sign-in"></i>
            <span class="btn-text">Sign in</span>
          </router-link>
          <router-link to="/register" class="nav-link nav-link-primary">
            <i aria-hidden="true" class="pi pi-user-plus"></i>
            <span class="btn-text">Sign up</span>
          </router-link>
        </template>
      </nav>
    </div>
  </header>

  <main id="contenido" class="main-content" tabindex="-1">
    <RouterView />
  </main>

  <NotificationToast />
  <ConfirmDialog />

  <Transition name="modal-fade">
    <div v-if="confirmEliminarAbierto" class="confirm-overlay cw-scope" @click.self="cerrarConfirmEliminar">
      <div class="confirm-modal" role="alertdialog" aria-modal="true" aria-labelledby="delete-account-title">
        <div class="confirm-icon-wrap">
          <i aria-hidden="true" class="pi pi-exclamation-triangle"></i>
        </div>
        <h2 id="delete-account-title">Delete your account?</h2>
        <p>This action is <strong>permanent</strong>. All your comments, ratings and favorites will be deleted. You will
          not be able to recover your account.</p>

        <div class="confirm-input-group">
          <label for="confirm-delete">Type <strong>DELETE</strong> to confirm:</label>
          <input id="confirm-delete" name="confirm_delete" type="text" autocomplete="off" spellcheck="false"
            v-model="confirmTexto" class="confirm-input" placeholder="DELETE"
            :disabled="eliminandoCuenta" />
        </div>

        <div class="confirm-actions">
          <button class="confirm-btn confirm-btn-cancel" @click="cerrarConfirmEliminar" :disabled="eliminandoCuenta">
            Cancel
          </button>
          <button class="confirm-btn confirm-btn-delete" @click="confirmarEliminarCuenta"
            :disabled="confirmTexto !== 'DELETE' || eliminandoCuenta">
            <i aria-hidden="true" v-if="eliminandoCuenta" class="pi pi-spin pi-spinner"></i>
            <i aria-hidden="true" v-else class="pi pi-trash"></i>
            {{ eliminandoCuenta ? 'Deleting…' : 'Delete account' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <footer class="main-footer cw-scope">
    <div class="footer-container">
      <div class="footer-brand">
        <h3>Game Rank</h3>
        <p>Your platform to discover, rank and collect video games.</p>
      </div>

      <div class="footer-section">
        <h4 class="footer-section-title">Explore</h4>
        <nav class="footer-nav footer-nav--grid">
          <RouterLink to="/" class="footer-nav-link">Home</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/content/overview" class="footer-nav-link">Catalog</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/tendencias" class="footer-nav-link">Trends</RouterLink>
          <RouterLink v-if="estadoAutenticacion.usuario" to="/user/profile" class="footer-nav-link">My Profile</RouterLink>
          <RouterLink v-if="esAdministrador" to="/admin/users" class="footer-nav-link">User Management</RouterLink>
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
            <i aria-hidden="true" class="pi pi-github"></i>
            Alan Novas Mateo
          </a>
        </div>
        <div class="footer-powered">
          <span class="footer-label">Powered by</span>
          <a href="https://rawg.io" target="_blank" class="footer-link">
            <i aria-hidden="true" class="pi pi-external-link"></i>
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
import Skeleton from '../components/Skeleton/Skeleton.vue';
import ConfirmDialog from '../components/Confirm/ConfirmDialog.vue';

export default {
  name: 'App',
  components: { NotificationToast, Skeleton, ConfirmDialog },
  mixins: [jsApp]
};
</script>

<style scoped src="./style_app.css"></style>