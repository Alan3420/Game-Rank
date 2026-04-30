<template>
  <header class="main-header">
    <div class="header-container">
      <router-link to="/" class="logo-link">
        <img id="logo" src="/src/assets/game_rank_logo.png" alt="Game Rank Logo" />
      </router-link>

      <nav class="nav-menu">
        <template v-if="estadoAutenticacion.usuario">
          <button @click="abierto = !abierto" class="options-user">
            <i class="pi pi-user"></i>
            {{ estadoAutenticacion.usuario.name }}
            <i v-if="abierto == false" class="pi pi-bars"></i>
            <i v-if="abierto == true" class="pi pi-times"></i>
          </button>

          <div v-if="abierto" class="desplegable-menu">

            <div class="apartado-info-user">
              <div class="icon">
                <i class="pi pi-user"></i>
              </div>

              <div class="info">
                <span class="user-name section">{{ estadoAutenticacion.usuario.name }}</span>
                <span class="user-email action">{{ estadoAutenticacion.usuario.email }}</span>
              </div>

            </div>

            <hr>
            <p class="section-title-desplegable">MI CUENTA</p>
            <div class="apartado-info-user user-hover">
              <div class="icon">
                <i class="pi pi-id-card"></i>
              </div>

              <div class="info">
                <router-link to="/user/profile" class="user-info section">
                  Perfil
                </router-link>
                <p class="action">Ver editar tu informacion</p>
              </div>

            </div>

            <hr>
            <div class="sect-logout log-out-hover">
              <div class="icon separator">
                <i class="pi pi-sign-out"></i>
                <button class="logout-btn" @click="manejarCierreSesion">
                  <span class="btn-text">Cerrar sesión</span>
                </button>
              </div>

            </div>

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
import { ref } from "vue"

const abierto = ref(false);
const router = useRouter();

const manejarCierreSesion = () => {
  estadoAutenticacion.cerrarSesion();
  router.push("/login");
};
</script>

<style scoped>
/* Header Styles */
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
  margin: 0 auto;
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

.brand-name {
  display: none;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 101;
}

/* Opciones de usuarios */
.options-user {
  position: relative;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 10px;
  background-color: white;

  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.options-user:hover {
  background-color: whitesmoke;
  border: 1px solid #6365f1af;
}

.apartado-info-user .pi {
  background-color: #6365f12a;
  color: #4f46e5;
  border-radius: 10px;
  margin: 0;
  padding: 7px;
}

.desplegable-menu {

  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  margin-top: 3px;
  min-width: 300px;


  border-radius: 10px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;

  box-shadow: 0 0 10px 1px rgba(0, 0, 0, 0.7);
}

.apartado-info-user {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}
.user-hover:hover{
  background-color: #6365f12a;
  border-radius: 10px;
  cursor: pointer;
}

.info {
  display: flex;
  flex-direction: column;
}

.section {
  font-weight: bold;
}

.action {
  color: #7e7e7e;
  font-size: 12px;

}

hr {
  border: none;
  background-color: #7e7e7e31;
  height: 1px;
}

.section-title-desplegable {
  color: #7e7e7e7a;
  font-size: 12px;
  font-weight: bold;
}

.user-info {
  text-decoration: none;
  color: black;
}

.separator {
  display: flex;
  gap: 10px;
}

.pi-sign-out {
  background-color: #d3393935;
  color: #d33939;
  border-radius: 10px;
  margin: 0;
  padding: 7px;
}

.logout-btn {
  border: none;
  background-color: transparent;
  color: #d33939;
}
.log-out-hover:hover{
  background-color: #d3393935;
  border-radius: 10px;
  cursor: pointer;
}

/* .user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #1f1f35;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  text-decoration: none;
  border-radius: 10px;
} */

/* .user-info i {
  font-size: 1rem;
}

.user-info:hover {
  background: #1f1f35;
  color: #dbffc4;

  transform: translateY(1px);
} */

/* .logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #1f1f35;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.logout-btn:hover {
  color: #dc2626;
  background: #1f1f35;
  transform: translateY(1px);
} */

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

/* .logout-btn {
  padding: 6px 12px;
  font-size: 0.85rem;
  width: 100%;
  border-radius: 10px;
  border: none;
} */

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

  .nav-menu {
    gap: 12px;
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
    gap: 8px;
  }

  .user-name {
    display: none;
  }

  .btn-text {
    display: none;
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
