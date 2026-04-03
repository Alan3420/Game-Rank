<template>
  <div class="register-container">
    <fieldset>
      <legend>Registrarse</legend>

      <form @submit.prevent="handleRegister">

        <label for="name">Nombre:</label>
        <input id="name" v-model="name" type="text" required>

        <label for="last_name">Apellidos:</label>
        <input id="last_name" v-model="last_name" type="text" required>

        <label for="email">Correo Electrónico:</label>
        <input id="email" v-model="email" type="email" required>

        <label for="password">Contraseña:</label>
        <input id="password" v-model="password" type="password" required>

        <button type="submit" :disabled="loading">
          <span v-if="!loading">Crear cuenta</span>
          <span v-else class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
        <p class="informacion"></p>

        <a href="/login" @click.prevent="$router.push('/login')">
          Volver al login
        </a>

      </form>
    </fieldset>
  </div>
</template>

<script>
import { register } from "../services/user_service";

export default {
  data() {
    return {
      name: "",
      last_name: "",
      email: "",
      password: "",
      loading: false
    };
  },
  methods: {
    async handleRegister() {

      try {
        this.loading = true;
        const response = await register(this.name, this.last_name, this.email, this.password);
        console.log("Usuario creado:", response);
        await new Promise(resolve => setTimeout(resolve, 2000))

        this.$router.push('/login');
      } catch (error) {
        if (error.response && error.response.status === 400) {
          await new Promise(resolve => setTimeout(resolve, 2000))
          let classInfo = document.querySelector(".informacion")
          classInfo.id = "info";

          let info = document.getElementById("info")
          info.textContent = error.response.data.message
        }
         else {
          console.log("Error:", error.message);
        }
      }
      finally {
        this.loading = false;

      }
    }
  }
};
</script>

<style scoped>

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f1f5f9;
}

fieldset {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  background: white;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #6366f1;
  color: #ffffff;
  padding: 10px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.25s;
}

button:hover {
  background-color: #4f46e5;
  transform: translateY(-2px);
}

a {
  margin-top: 10px;
  text-align: center;
  text-decoration: none;
  color: #6366f1;
  transition: 0.2s;
}

a:hover {
  transform: scale(1.05);
}

</style>