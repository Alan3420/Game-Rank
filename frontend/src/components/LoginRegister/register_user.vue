<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1 class="register-title">Únete a Game Rank</h1>
        <p class="register-subtitle">Crea tu cuenta para acceder a reseñas, favoritos y mucho más</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="name" class="form-label">Nombre</label>
            <input
              id="name"
              v-model="name"
              type="text"
              placeholder="Tu nombre"
              class="form-input"
              maxlength="50"
              required
            >
          </div>

          <div class="form-group">
            <label for="last_name" class="form-label">Apellidos</label>
            <input
              id="last_name"
              v-model="last_name"
              type="text"
              placeholder="Tus apellidos"
              class="form-input"
              maxlength="50"
              required
            >
          </div>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Correo Electrónico</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="tu@email.com"
            class="form-input"
            maxlength="100"
            required
          >
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Mínimo 8 caracteres"
            class="form-input"
            maxlength="50"
            required
          >
        </div>

        <label class="form-checkbox-label">
          <input type="checkbox" v-model="aceptaTerminos" class="form-checkbox" />
          <span>
            He leído y acepto los
            <router-link to="/terminos" target="_blank" class="link">Términos y Condiciones</router-link>
          </span>
        </label>

        <button type="submit" :disabled="loading || !isFormValid" class="btn btn-primary">
          <span :style="{ visibility: loading ? 'hidden' : 'visible' }">Crear Cuenta</span>
          <span v-if="loading" class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        <div v-if="errorMessage" class="error-message">
          <i class="pi pi-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div class="register-footer">
          <p>¿Ya tienes cuenta? <router-link to="/login" class="link">Inicia sesión</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
    import jsRegister from "./script_register.js";

    export default {
        name: 'register',
        mixins: [jsRegister]
    };
</script>
<style scoped src="./style_register.css"></style>