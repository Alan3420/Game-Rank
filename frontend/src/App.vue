<template>
  <header class="main-header">
    <div class="header-container">
      <router-link to="/" class="logo-link">
        <img id="logo" src="/src/assets/game_rank_logo.png" alt="Game Rank Logo" />
      </router-link>

      <div v-if="estadoAutenticacion.usuario" class="header-search">
        <i class="pi pi-search header-search-icon"></i>
        <input
          type="text"
          v-model="headerSearch"
          placeholder="Buscar un juego..."
          class="header-search-input"
          @keyup.enter="submitHeaderSearch"
        />
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
                    {{ estadoAutenticacion.usuario.name?.charAt(0)?.toUpperCase() }}{{ estadoAutenticacion.usuario.last_name?.charAt(0)?.toUpperCase() }}
                  </div>
                  <div class="dropdown-user-info">
                    <span class="dropdown-name">{{ estadoAutenticacion.usuario.name }} {{ estadoAutenticacion.usuario.last_name }}</span>
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
import { ref, watch, onMounted, onUnmounted } from "vue";
import NotificationToast from './components/Notifications/NotificationToast.vue';
import { notificaciones } from './store/notificaciones';

const router = useRouter();
const route = useRoute();

const headerSearch = ref('');
const menuAbierto = ref(false);
const userMenuRef = ref(null);

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
    } catch {}
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
  background: #ffffffe5;
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
  color: #1f1f35;
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
  background: #f3f4fa;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 0 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.header-search:focus-within {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: #fff;
}

.header-search-icon {
  color: #9ca3af;
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
  color: #1f1f35;
  padding: 10px 0;
}

.header-search-input::placeholder {
  color: #9ca3af;
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
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  font-family: 'Sora', sans-serif;
  font-size: 0.88rem;
  font-weight: 600;
  color: #1f1f35;
}

.options-user:hover,
.options-user.is-active {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.user-avatar-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  color: #1f1f35;
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
  color: #9ca3af;
}

/* ── DROPDOWN ── */
.user-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 280px;
  background: white;
  border: 1px solid #edeef8;
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
  background: #6366f1;
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
  color: #1f1f35;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-email {
  font-size: 0.78rem;
  color: #9ca3af;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-divider {
  height: 1px;
  background: #f0f0f8;
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
  background: #eef2ff;
  color: #6366f1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.dropdown-logout-icon {
  background: #fff0f0;
  color: #d33939;
}

.dropdown-item-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.dropdown-item-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1f1f35;
}

.dropdown-logout .dropdown-item-title {
  color: #d33939;
}

.dropdown-item-desc {
  font-size: 0.75rem;
  color: #9ca3af;
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
  color: #6b7280;
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
  background: #6366f1;
  color: white;
  border: 1px solid #6366f1;
}

.nav-link-primary:hover {
  background: #4f46e5;
  border-color: #4f46e5;
  transform: translateY(-1px);
}

/* Main Content */
.main-content {
  min-height: calc(100vh - 144px);
  /* Header + Footer height */
}

/* Footer Styles */
.main-footer {
  background: #f8f9fb;
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
  color: #1f1f35;
}

.footer-brand p {
  margin: 0;
  color: #6b7280;
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
  color: #6b7280;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: #6366f1;
}

.footer-copyright {
  text-align: right;
}

.footer-copyright p {
  margin: 0;
  color: #9ca3af;
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
