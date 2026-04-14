<template>
    <header class="main-header">
        <nav class="nav-container">
            <div class="logo-container">
                <router-link to="/">
                    <img id="logo" src="/src/assets/game_rank_logo.png" alt="Game Rank Logo">
                </router-link>
            </div>

            <ul class="nav-links">
                <li class="user_container">
                    <template v-if="estadoAutenticacion.usuario">
                        <div class="user-info">
                            <i class="pi pi-user"></i>
                            <span>{{ estadoAutenticacion.usuario.name }}</span>
                        </div>

                        <a href="#" @click.prevent="manejarCierreSesion" class="logout-link">
                            <i class="pi pi-sign-out"></i>
                            Cerrar sesión
                        </a>
                    </template>

                    <template v-else>
                        <router-link to="/login">Iniciar Sesión</router-link>
                        <router-link to="/register">Registrarse</router-link>
                    </template>
                </li>
            </ul>
        </nav>
    </header>

    <main>
        <RouterView />
    </main>

    <footer>

        <div class="footer-info">
            <p>&copy; 2026 Game Rank | Game data powered by <a href="https://rawg.io" target="_blank">RAWG</a></p>
        </div>

        <div class="footer-links">
            <a href="">Terminos</a>
            <a href="">Privacidad</a>
            <a href="https://github.com/Alan3420" target="_blank">Contacto</a>
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
/* Estilos base del Header */
.main-header {
    background-color: #ffffff;
    /* Fondo blanco */
    border-bottom: 1px solid #eaeaea;
    padding: 0 20px;
    height: 80px;
    display: flex;
    align-items: center;
}

.nav-container {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}







</style>
