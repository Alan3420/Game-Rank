<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1 class="login-title">Welcome back</h1>
        <p class="login-subtitle">Sign in to access your account and explore the best games</p>
      </div>

      <form @submit.prevent="manejarInicioSesion" class="login-form">
        <div class="form-group">
          <label for="email" class="form-label">
            Email Address
          </label>
          <input
            type="email"
            id="email"
            name="email"
            autocomplete="email"
            spellcheck="false"
            v-model="email"
            placeholder="your@email.com"
            class="form-input"
            maxlength="100"
            required
          >
        </div>

        <div class="form-group">
          <label for="passwd" class="form-label">
            Password
          </label>
          <div class="input-wrap">
            <input
              :type="mostrarPassword ? 'text' : 'password'"
              id="passwd"
              name="password"
              autocomplete="current-password"
              v-model="password"
              placeholder="Your password"
              class="form-input"
              maxlength="50"
              required
            >
            <button type="button" class="eye-btn" @click="mostrarPassword = !mostrarPassword"
              :aria-label="mostrarPassword ? 'Hide password' : 'Show password'" :aria-pressed="mostrarPassword">
              <i aria-hidden="true" class="pi" :class="mostrarPassword ? 'pi-eye-slash' : 'pi-eye'"></i>
            </button>
          </div>
        </div>

        <button type="submit" :disabled="loading || !formularioValido" class="btn btn-primary">
          <span :style="{ visibility: loading ? 'hidden' : 'visible' }">Sign In</span>
          <span v-if="loading" class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        <div v-if="errorMessage" class="error-message">
          <i aria-hidden="true" class="pi pi-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div class="login-footer">
          <p>Don't have an account? <router-link to="/register" class="link">Register here</router-link></p>
          <p><router-link to="/terminos" class="link">Terms and Conditions</router-link></p>
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