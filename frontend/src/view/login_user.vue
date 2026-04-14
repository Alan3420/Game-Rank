<template>

  <body>
    <fieldset>
      <legend>Iniciar Sesion</legend>

      <form @submit.prevent="handleLogin">
        <label for="email">Correo Electrónico:</label>
        <input type="email" id="email" v-model="email" placeholder="email">

        <label for="passwd">Contraseña:</label>
        <input type="password" id="passwd" v-model="password" placeholder="password">

        <button type="submit" :disabled="loading">
          <span v-if="!loading">Login</span>
          <span v-else class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
        <a href="/register">¿no tienes cuenta? Registrate</a>
        <p class="informacion"></p>
      </form>
    </fieldset>
  </body>
</template>

<script>
import { login } from "../services/user_service";

export default {
  data() {
    return {
      email: "",
      password: "",
      loading: false

    }
  },
  methods: {
    async handleLogin() {
      try {
        this.loading = true
        const response = await login(this.email, this.password)
        

        await new Promise(resolve => setTimeout(resolve, 2000))

        console.log("Inicio de Sesion correcto");
        
        localStorage.setItem("token", response.token)
        localStorage.setItem("user", JSON.stringify(response.user))
        this.$router.push('/content/overview');

      } catch (error) {
        if(error.response && error.response.status === 401){
          
          await new Promise(resolve => setTimeout(resolve, 2000))
          let classInfo = document.querySelector(".informacion")
          classInfo.id = "info";
          
          let info = document.getElementById("info")

          info.textContent = error.response.data.message
          console.log(error.response.data.message);
          
        }
        else{
          console.log("Error:", error.message);
        }
      }
      finally {
        this.loading = false
      }

    }
  }
}
</script>


<style scoped>
body {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

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
