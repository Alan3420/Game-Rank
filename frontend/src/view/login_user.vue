<template>

    <body>
        <div class="container-login">

            <!-- Panel izquierdo -->
            <div class="panel">
                <div :class="{ 'slide-out-left': isRegistering }">
                    <div class="welcome-section">
                        <h1>Bienvenido de vuelta</h1>
                        <p>Por favor, inicia sesión para continuar.</p>
                        <a href="https://github.com/Alan3420/Proyecto-Game-Rank.git" target="_blank"
                            class="github-link">
                            <i class="fab fa-github"></i>Repo Github
                        </a>
                    </div>
                </div>

                <div :class="{ 'slide-out-left': !isRegistering }">
                    <fieldset>
                        <legend>Crear Cuenta</legend>
                        <form @submit.prevent="handleRegister">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="nombre">Nombre:</label>
                                    <input id="nombre" v-model="register.nombre" type="text" required />
                                </div>
                                <div class="form-group">
                                    <label for="apellido">Apellido:</label>
                                    <input id="apellido" v-model="register.apellido" type="text" required />
                                </div>
                            </div>
                            <label for="reg-email">Correo Electrónico:</label>
                            <input id="reg-email" v-model="register.email" type="email" required />
                            <label for="reg-password">Contraseña:</label>
                            <input id="reg-password" v-model="register.password" type="password" required />
                            <button type="submit">Registrarse</button>
                            <a href="#" @click.prevent="toggleView">¿Ya tienes cuenta? Inicia sesión</a>
                        </form>
                    </fieldset>
                </div>
            </div>

            <!-- Panel derecho -->
            <div class="panel">
                <div :class="{ 'slide-out-right': isRegistering }">
                    <fieldset>
                        <legend>Iniciar Sesión</legend>
                        <form @submit.prevent="handleLogin">
                            <label for="email">Correo Electrónico:</label>
                            <input id="email" v-model="email" type="email" required />
                            <label for="password">Contraseña:</label>
                            <input id="password" v-model="password" type="password" required />
                            <button type="submit">Iniciar Sesión</button>
                            <a href="#" @click.prevent="toggleView">Crear una cuenta</a>
                        </form>
                    </fieldset>
                </div>

                <div :class="{ 'slide-out-right': !isRegistering }">
                    <div class="welcome-section">
                        <h1>¡Únete a Game Rank!</h1>
                        <p>Registra tu progreso, compite con otros jugadores y sube en el ranking.</p>
                    </div>
                </div>
            </div>

        </div>
    </body>
</template>

<script>
import { login } from "../services/user_service";

export default {
    data() {
        return {
            email: "",
            password: "",
            isRegistering: false,
            register: {
                nombre: "",
                apellido: "",
                email: "",
                password: "",
            }
        }
    },
    methods: {
        async handleLogin() {
            try {
                const response = await login(this.email, this.password)
                localStorage.setItem("token", response.token)
                localStorage.setItem("user", JSON.stringify(response.user))
                this.$router.push('/content');
            } catch (error) {
                console.log("Error:", error)
            }
        },

        async handleRegister() {
            console.log("Registrando:", this.register);
            // conecta aquí tu servicio
        },

        toggleView() {
            this.isRegistering = !this.isRegistering;
            const container = document.querySelector(".container-login");
            container.classList.toggle("active");
        },

    }
}
</script>

<style scoped>
@property --angle {
    syntax: '<angle>';
    initial-value: 125deg;
    inherits: false;
}

.panel {
    flex: 1;
    max-width: 400px;
    position: relative;
    min-height: 350px;
}

.panel>div {
    position: absolute;
    width: 100%;
    transition: opacity 0.4s ease, transform 0.4s ease;
}

.slide-out-left {
    opacity: 0;
    transform: translateX(-60px);
    pointer-events: none;
    position: absolute;
}

.slide-out-right {
    opacity: 0;
    transform: translateX(60px);
    pointer-events: none;
    position: absolute;
}

body {
    margin: 0;
    padding: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #f1f5f9;

}

.container-login {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    padding: 2rem;
    max-width: 900px;
    width: 90%;
    /* responsive */
    min-height: 80vh;
    height: auto;
    color: white;

    background: linear-gradient(var(--angle), #9ca3af 50%, #6366f1 50%);
    transition: --angle 0.4s cubic-bezier(0.1, 0, 0.1, 1);
    background-size: 200% 200%;
    background-position: 78% 0%;
    border-radius: 10px;
    box-shadow: 0 0 6px 0 rgba(0, 0, 0, 0.5);

}

.container-login.active {
    --angle: 305deg;
}

.welcome-section,
fieldset {
    flex: 1;
    max-width: 400px;
}

.welcome-section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 1rem;
}

fieldset {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 2rem;
}

form {
    display: flex;
    flex-direction: column;

}

form label {
    margin-bottom: 5px;
    font-weight: bold;
}

form input {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

form button {
    background-color: #6366f1;
    color: #ffffff;
    padding: 10px;
    font-size: 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.25s ease, transform 0.2s ease;
}

form button:hover {
    background-color: #4f46e5;
    transform: translateY(-2px);
}

form a {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-decoration: none;
    color: black;
    transition: transform 0.2s;
    color: white;
}

form a:hover {
    transform: scale(1.1);
}

a i {
    font-size: 1.5rem;
    color: #111827;
    transition: color 0.2s ease;
}


.github-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;

    color: #111827;
    padding: 1rem 5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.github-link:hover,
.github-link:hover i {
    background-color: #6366f1;
    color: white;

}

@media (max-width: 768px) {
    .container-login {
        flex-direction: column;
        padding: 1rem;
    }
}
</style>