<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1 class="login-title">Bienvenido de vuelta</h1>
        <p class="login-subtitle">Inicia sesión para acceder a tu cuenta y explorar los mejores juegos</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email" class="form-label">Correo Electrónico</label>
          <input type="email" id="email" v-model="email" placeholder="tu@email.com" class="form-input" required>
        </div>

        <div class="form-group">
          <label for="passwd" class="form-label">Contraseña</label>
          <input type="password" id="passwd" v-model="password" placeholder="Tu contraseña" class="form-input" required>
        </div>

        <button type="submit" :disabled="loading" class="btn btn-primary">
          <span v-if="!loading">Iniciar Sesión</span>
          <span v-else class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        <div v-if="errorMessage" class="error-message">
          <i class="pi pi-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div class="login-footer">
          <p>¿No tienes cuenta? <router-link to="/register" class="link">Regístrate aquí</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
    import jslogin from "./script_login.js";

    export default {
        name: 'login',
        mixins: [jslogin]
    };
</script>

<style scoped src="./style_login.css"></style>