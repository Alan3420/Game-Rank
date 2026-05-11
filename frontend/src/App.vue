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
        <template v-if="estadoAutenticacion.usuario">
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
      </div>

      <div class="footer-links">
        <a href="https://github.com/Alan3420" target="_blank" class="footer-link">
          <i class="pi pi-github"></i>
          GitHub
        </a>
        <a href="https://rawg.io" target="_blank" class="footer-link">
          <i class="pi pi-external-link"></i>
          RAWG API
        </a>
      </div>

      <div class="footer-copyright">
        <p>&copy; 2026 Game Rank. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { estadoAutenticacion } from './store/autenticacion';
import { useRouter, useRoute } from 'vue-router';
import { ref, watch, onMounted, onUnmounted, computed } from "vue";
import NotificationToast from './components/Notifications/NotificationToast.vue';
import { notificaciones } from './store/notificaciones';
import { deleteOwnAccount } from './services/user_service';

const router = useRouter();
const route = useRoute();

const headerSearch = ref('');
const menuAbierto = ref(false);
const userMenuRef = ref(null);

const confirmEliminarAbierto = ref(false);
const confirmTexto = ref('');
const eliminandoCuenta = ref(false);

const isAdmin = computed(() => estadoAutenticacion.usuario?.role === 'admin');

watch(() => route.query.q, (val) => {
  headerSearch.value = val || '';
}, { immediate: true });

watch(route, () => {
  menuAbierto.value = false;
});

const submitHeaderSearch = () => {
  const term = headerSearch.value.trim();
  router.push({ path: '/content/overview', query: term ? { q: term } : {} });
};

const manejarCierreSesion = () => {
  menuAbierto.value = false;
  estadoAutenticacion.cerrarSesion();
  router.push("/login");
  notificaciones.success("Has cerrado sesión correctamente.", { title: "Hasta luego" });
};

const irAConfigAdmin = () => {
  menuAbierto.value = false;
  notificaciones.info("Panel de configuración en desarrollo.", { title: "Próximamente" });
};

const abrirConfirmEliminar = () => {
  menuAbierto.value = false;
  confirmTexto.value = '';
  confirmEliminarAbierto.value = true;
};

const cerrarConfirmEliminar = () => {
  if (eliminandoCuenta.value) return;
  confirmEliminarAbierto.value = false;
  confirmTexto.value = '';
};

const confirmarEliminarCuenta = async () => {

  if (confirmTexto.value !== 'ELIMINAR' || eliminandoCuenta.value) return;
  eliminandoCuenta.value = true;

  try {

    await deleteOwnAccount();
    confirmEliminarAbierto.value = false;
    estadoAutenticacion.cerrarSesion();
    router.push("/login");
    notificaciones.success("Tu cuenta ha sido eliminada permanentemente.", { title: "Cuenta eliminada" });

  } catch (error) {

    console.error('Error al eliminar la cuenta:', error);
    notificaciones.error(
      error.response?.data?.message || "No pudimos eliminar tu cuenta. Inténtalo de nuevo.",
      { title: "Error" }
    );
    
  } finally {
    eliminandoCuenta.value = false;
  }
};

const handleClickOutside = (e) => {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    menuAbierto.value = false;
  }
};

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside);

  const flash = localStorage.getItem('flashNotificacion');
  if (flash) {
    localStorage.removeItem('flashNotificacion');
    try {
      const { type, title, message } = JSON.parse(flash);
      const fn = type === 'success' ? notificaciones.success : notificaciones.error;
      fn(message, { title });
    } catch { }
  }
});
onUnmounted(() => document.removeEventListener('mousedown', handleClickOutside));
</script>

<style scoped>
/* Header Styles */
* {
  font-family: 'Sora', sans-serif;
}

.main-header {
  background: var(--color-surface-translucent);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-container {
  max-width: 1400px;
  padding: 0 24px;
  display: flex;
  position: relative;

  align-items: center;
  justify-content: space-between;
  min-height: 72px;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--color-text);
  font-weight: 800;
  font-size: 1.25rem;
  transition: opacity 0.2s ease;
}


#logo {
  height: 40px;
  width: auto;
}


.header-search {
  flex: 1;
  max-width: 480px;
  margin: 0 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--color-bg-gradient-end);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 0 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.header-search:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: var(--color-surface);
}

.header-search-icon {
  color: var(--color-text-placeholder);
  font-size: 0.85rem;
  flex-shrink: 0;
}

.header-search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-family: 'Sora', sans-serif;
  font-size: 0.9rem;
  color: var(--color-text);
  padding: 10px 0;
}

.header-search-input::placeholder {
  color: var(--color-text-placeholder);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 101;
}

/* ── USER MENU ── */
.user-menu {
  position: relative;
}

.options-user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px 6px 6px;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  font-family: 'Sora', sans-serif;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--color-text);
}

.options-user:hover,
.options-user.is-active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.user-avatar-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.options-user .pi-chevron-up,
.options-user .pi-chevron-down {
  font-size: 0.7rem;
  color: var(--color-text-placeholder);
}

/* ── DROPDOWN ── */
.user-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 280px;
  background: white;
  border: 1px solid var(--color-border-light);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(20, 21, 63, 0.12), 0 2px 8px rgba(20, 21, 63, 0.06);
  overflow: hidden;
  z-index: 200;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.dropdown-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  font-size: 0.95rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: -0.02em;
}

.dropdown-user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.dropdown-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-email {
  font-size: 0.78rem;
  color: var(--color-text-placeholder);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-divider {
  height: 1px;
  background: var(--color-border-lightest);
  margin: 0;
}

.dropdown-section-label {
  margin: 0;
  padding: 10px 16px 6px;
  font-size: 0.68rem;
  font-weight: 700;
  color: #b0b0c8;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  text-decoration: none;
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Sora', sans-serif;
  transition: background 0.15s ease;
  text-align: left;
}

.dropdown-item:hover {
  background: #f8f8fe;
}

.dropdown-item-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.dropdown-logout-icon {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.dropdown-danger-icon {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.dropdown-danger .dropdown-item-title {
  color: var(--color-danger);
}

/* ── MODAL CONFIRMACIÓN ── */
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 15, 30, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.confirm-modal {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 440px;
  width: 100%;
  text-align: center;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--color-border-light);
}

.confirm-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-danger-light);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
}

.confirm-icon-wrap i {
  font-size: 1.8rem;
  color: var(--color-danger);
}

.confirm-modal h2 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--color-text);
  margin: 0 0 0.75rem;
}

.confirm-modal p {
  font-size: 0.92rem;
  color: var(--color-text-medium);
  margin: 0 0 1.5rem;
  line-height: 1.5;
}

.confirm-modal p strong {
  color: var(--color-danger);
  font-weight: 700;
}

.confirm-input-group {
  text-align: left;
  margin-bottom: 1.5rem;
}

.confirm-input-group label {
  display: block;
  font-size: 0.82rem;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
  font-weight: 500;
}

.confirm-input-group label strong {
  color: var(--color-text);
  font-weight: 700;
}

.confirm-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  font-family: 'Sora', sans-serif;
  font-size: 0.92rem;
  color: var(--color-text);
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.confirm-input:focus {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 3px rgba(211, 57, 57, 0.1);
}

.confirm-input:disabled {
  background: var(--color-surface-hover);
  cursor: not-allowed;
}

.confirm-actions {
  display: flex;
  gap: 10px;
  justify-content: stretch;
}

.confirm-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 11px 18px;
  border-radius: 10px;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-btn-cancel {
  background: white;
  border-color: var(--color-border);
  color: var(--color-text-secondary);
}

.confirm-btn-cancel:hover:not(:disabled) {
  background: #f8f8fe;
  border-color: #d1d5db;
}

.confirm-btn-delete {
  background: var(--color-danger);
  color: white;
  box-shadow: 0 4px 14px rgba(211, 57, 57, 0.25);
}

.confirm-btn-delete:hover:not(:disabled) {
  background: var(--color-danger-hover);
  box-shadow: 0 8px 22px rgba(211, 57, 57, 0.35);
  transform: translateY(-1px);
}

.confirm-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-active .confirm-modal,
.modal-fade-leave-active .confirm-modal {
  transition: transform 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .confirm-modal,
.modal-fade-leave-to .confirm-modal {
  transform: scale(0.95);
}

.dropdown-item-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.dropdown-item-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--color-text);
}

.dropdown-logout .dropdown-item-title {
  color: var(--color-danger);
}

.dropdown-item-desc {
  font-size: 0.75rem;
  color: var(--color-text-placeholder);
}

/* Animación dropdown */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.user-btn-name {
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}


.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  color: var(--color-text-medium);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  border-radius: 20px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: rgba(0, 0, 0, 0.04);
}

.nav-link-primary {
  background: var(--color-primary);
  color: white;
  border: 1px solid var(--color-primary);
}

.nav-link-primary:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
}

/* Main Content */
.main-content {
  min-height: calc(100vh - 144px);
  /* Header + Footer height */
}

/* Footer Styles */
.main-footer {
  background: var(--color-bg-gradient-start);
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  margin-top: auto;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 24px 24px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 40px;
  align-items: center;
}

.footer-brand h3 {
  margin: 0 0 8px;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--color-text);
}

.footer-brand p {
  margin: 0;
  color: var(--color-text-medium);
  font-size: 0.9rem;
  line-height: 1.5;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-text-medium);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--color-primary);
}

.footer-copyright {
  text-align: right;
}

.footer-copyright p {
  margin: 0;
  color: var(--color-text-placeholder);
  font-size: 0.85rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
    min-height: 64px;
    flex-wrap: nowrap;
  }

  .logo-link {
    font-size: 1.1rem;
  }

  #logo {
    height: 32px;
  }

  .header-search {
    margin: 0 12px;
  }

  .nav-menu {
    gap: 12px;
  }

  .nav-link {
    padding: 6px 12px;
    font-size: 0.85rem;
  }


  .footer-container {
    grid-template-columns: 1fr;
    gap: 24px;
    text-align: center;
    padding: 32px 16px 20px;
  }

  .footer-links {
    justify-content: center;
  }

  .footer-copyright {
    text-align: center;
  }
}

@media (max-width: 640px) {
  .header-container {
    flex-wrap: wrap;
    padding-top: 12px;
    padding-bottom: 12px;
    min-height: 0;
    row-gap: 10px;
  }

  .logo-link {
    order: 1;
  }

  .nav-menu {
    order: 2;
  }

  .header-search {
    order: 3;
    flex-basis: 100%;
    max-width: 100%;
    margin: 0;
  }
}

@media (max-width: 480px) {
  .nav-menu {
    gap: 8px;
  }

  .nav-link {
    order: 3;
  }

  .nav-link-primary {
    order: 4;
  }

  .user-btn-name {
    display: none;
  }

  .footer-links {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
