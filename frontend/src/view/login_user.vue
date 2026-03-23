<template>
    <div class="container-login">
        <div class="welcome-section">
            <h1>Bienvenido de vuelta</h1>
            <p>Por favor, inicia sesión para continuar.</p>
            <a href="https://github.com/Alan3420/Proyecto-Game-Rank.git" target="_blank" class="github-link">
                <i class="fab fa-github"></i>Repo Github
            </a>
        </div>

        <fieldset>
            <legend>Iniciar Sesión</legend>
            <form @submit.prevent="handleLogin">
                <label for="email">Correo Electrónico:</label>
                <input id="email" v-model="email" type="email" required>

                <label for="password">Contraseña:</label>
                <input id="password" v-model="password" type="password" required>

                <button type="submit" v-on:click=>Iniciar Sesión</button>
            </form>
        </fieldset>
    </div>
</template>

<script>
import { login } from "../services/user_service";

export default {
    data(){
        return {
            email: "",
            password: ""
        }
    },
    methods:{
        async handleLogin() {
            try {
                const response = await login(this.email, this.password)
                console.log("Respuesta:", response)
                this.$router.push('/content');
            } catch (error) {
                console.log("Error:", error)
            }
}
    }
}
</script>

<style scoped>
.container-login {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  min-height: 80vh;
  padding: 2rem;
}
.welcome-section ,fieldset{
  flex: 1;
  max-width: 400px;
}
.welcome-section{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 1rem;
}

fieldset{
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 2rem;
}

form{
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
.github-link:hover, .github-link:hover i {
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