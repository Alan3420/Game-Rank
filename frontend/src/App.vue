<template>
  <header class="main-header">
    <div class="header-container">
      <router-link to="/" class="logo-link">
        <img id="logo" src="/src/assets/game_rank_logo.png" alt="Game Rank Logo" />
        <span class="brand-name">Game Rank</span>
      </router-link>

      <nav class="nav-menu">
        <template v-if="estadoAutenticacion.usuario">
          <div class="user-info">
            <i class="pi pi-user"></i>
            <span class="user-name">{{ estadoAutenticacion.usuario.name }}</span>
          </div>
          <button class="logout-btn" @click="manejarCierreSesion">
            <i class="pi pi-sign-out"></i>
            Cerrar sesión
          </button>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link">
            <i class="pi pi-sign-in"></i>
            Iniciar sesión
          </router-link>
          <router-link to="/register" class="nav-link nav-link-primary">
            <i class="pi pi-user-plus"></i>
            Registrarse
          </router-link>
        </template>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <RouterView />
  </main>

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
import { useRouter } from 'vue-router';

const router = useRouter();

const manejarCierreSesion = () => {
  estadoAutenticacion.cerrarSesion();
  router.push("/login");
};
</script>

<style scoped>
/* Header Styles */
.main-header {
  background: #ffffff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
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

.logo-link:hover {
  opacity: 0.8;
}

#logo {
  height: 40px;
  width: auto;
}

.brand-name {
  display: none;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(99, 102, 241, 0.08);
  border-radius: 20px;
  color: #6366f1;
  font-weight: 600;
  font-size: 0.95rem;
}

.user-info i {
  font-size: 1rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(239, 68, 68, 0.08);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  transform: translateY(-1px);
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
  color: #1f1f35;
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
  min-height: calc(100vh - 144px); /* Header + Footer height */
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
  }

  .logo-link {
    font-size: 1.1rem;
  }

  #logo {
    height: 32px;
  }

  .nav-menu {
    gap: 12px;
  }

  .user-info {
    padding: 6px 12px;
    font-size: 0.85rem;
  }

  .logout-btn,
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

@media (max-width: 480px) {
  .nav-menu {
    flex-direction: column;
    gap: 8px;
  }

  .user-info {
    order: 1;
  }

  .logout-btn {
    order: 2;
  }

  .nav-link {
    order: 3;
  }

  .nav-link-primary {
    order: 4;
  }

  .footer-links {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
