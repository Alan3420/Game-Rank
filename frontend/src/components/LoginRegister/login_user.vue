<template>
  <div class="auth card-world">
    <div class="auth-shell">

      <div class="auth-intro">
        <h1 class="auth-title">Welcome back</h1>
        <p class="auth-lede">Sign in to pick up your album where you left it.</p>
        <ul class="auth-perks">
          <li><i aria-hidden="true" class="pi pi-bookmark"></i><span>Your collection and its four statuses</span></li>
          <li><i aria-hidden="true" class="pi pi-heart"></i><span>Your favorites, saved across devices</span></li>
          <li><i aria-hidden="true" class="pi pi-star"></i><span>Your reviews and ratings</span></li>
        </ul>
      </div>

      <!-- carta de socio: marco uniforme y el formulario en la cara -->
      <section class="auth-card cw-frame" aria-labelledby="auth-card-title">
        <div class="auth-card__face">
          <div class="auth-card__band">
            <h2 id="auth-card-title" class="auth-card__title">Sign in</h2>
            <span class="auth-card__set">Returning</span>
          </div>

          <form class="auth-form" novalidate @submit.prevent="manejarInicioSesion">
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input
                id="email"
                v-model="email"
                type="email"
                name="email"
                autocomplete="email"
                spellcheck="false"
                placeholder="your@email.com"
                class="form-input"
                :class="{ 'input-error': errorVisible.email }"
                :aria-invalid="errorVisible.email ? 'true' : 'false'"
                aria-describedby="email-hint"
                maxlength="100"
                required
              >
              <span id="email-hint" class="form-hint form-hint--error">{{ errorVisible.email }}</span>
            </div>

            <div class="form-group">
              <label for="passwd" class="form-label">Password</label>
              <div class="input-wrap">
                <input
                  id="passwd"
                  v-model="password"
                  :type="mostrarPassword ? 'text' : 'password'"
                  name="password"
                  autocomplete="current-password"
                  placeholder="Your password"
                  class="form-input form-input--eye"
                  :class="{ 'input-error': errorVisible.password }"
                  :aria-invalid="errorVisible.password ? 'true' : 'false'"
                  aria-describedby="passwd-hint"
                  maxlength="50"
                  required
                >
                <button type="button" class="eye-btn" :aria-label="mostrarPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="mostrarPassword" @click="mostrarPassword = !mostrarPassword">
                  <i aria-hidden="true" class="pi" :class="mostrarPassword ? 'pi-eye-slash' : 'pi-eye'"></i>
                </button>
              </div>
              <span id="passwd-hint" class="form-hint form-hint--error">{{ errorVisible.password }}</span>
            </div>

            <div v-if="errorMessage" class="error-alert" role="alert">
              <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
              {{ errorMessage }}
            </div>

            <button type="submit" :disabled="loading" class="auth-btn">
              <i v-if="loading" aria-hidden="true" class="pi pi-spin pi-spinner"></i>
              {{ loading ? 'Signing in…' : 'Sign in' }}
            </button>

            <p class="auth-alt">New here? <router-link to="/register" class="auth-link">Create an account</router-link></p>
          </form>

          <div class="auth-card__foot" aria-hidden="true">
            <span class="auth-card__no">Game Rank</span>
            <span>Game data by RAWG</span>
          </div>
        </div>
      </section>
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

<style scoped src="./style_auth.css"></style>
