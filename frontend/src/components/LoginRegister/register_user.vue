<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1 class="register-title">Join Game Rank</h1>
        <p class="register-subtitle">Create your account to access reviews, favorites and much more</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="name" class="form-label">First Name</label>
            <input
              id="name"
              v-model="name"
              type="text"
              placeholder="Your first name"
              class="form-input"
              maxlength="50"
              required
            >
          </div>

          <div class="form-group">
            <label for="last_name" class="form-label">Last Name</label>
            <input
              id="last_name"
              v-model="last_name"
              type="text"
              placeholder="Your last name"
              class="form-input"
              maxlength="50"
              required
            >
          </div>
        </div>

        <div class="form-group">
          <label for="nickname" class="form-label">Nickname</label>
          <div class="input-wrap">
            <span class="input-prefix">@</span>
            <input
              id="nickname"
              v-model="nickname"
              type="text"
              placeholder="your_nickname"
              class="form-input input-with-prefix"
              :class="{ 'input-error': nickname && !nicknameValido }"
              maxlength="30"
              required
            >
          </div>
          <span v-if="nickname && !nicknameValido" class="error-text">
            3-30 characters: letters, numbers and underscores (_) only
          </span>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="tu@gmail.com"
            class="form-input"
            :class="{ 'input-error': email && !emailDominioValido }"
            maxlength="100"
            required
          >
          <span v-if="email && !emailDominioValido" class="error-text">
            Invalid email domain
          </span>
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <div class="input-wrap">
            <input
              id="password"
              v-model="password"
              :type="mostrarPassword ? 'text' : 'password'"
              placeholder="Minimum 8 characters"
              class="form-input"
              maxlength="50"
              required
            >
            <button type="button" class="eye-btn" @click="mostrarPassword = !mostrarPassword" tabindex="-1">
              <i class="pi" :class="mostrarPassword ? 'pi-eye-slash' : 'pi-eye'"></i>
            </button>
          </div>
        </div>

        <div class="form-group">
          <label for="confirmPassword" class="form-label">Confirm password</label>
          <div class="input-wrap">
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              :type="mostrarConfirmPassword ? 'text' : 'password'"
              placeholder="Repeat your password"
              class="form-input"
              :class="{ 'input-error': confirmPassword && password !== confirmPassword }"
              maxlength="50"
              required
            >
            <button type="button" class="eye-btn" @click="mostrarConfirmPassword = !mostrarConfirmPassword" tabindex="-1">
              <i class="pi" :class="mostrarConfirmPassword ? 'pi-eye-slash' : 'pi-eye'"></i>
            </button>
          </div>
          <span v-if="confirmPassword && password !== confirmPassword" class="error-text">
            Passwords do not match
          </span>
        </div>

        <label class="form-checkbox-label">
          <input type="checkbox" v-model="aceptaTerminos" class="form-checkbox" />
          <span>
            I have read and accept the
            <router-link to="/terminos" target="_blank" class="link">Terms and Conditions</router-link>
          </span>
        </label>

        <button type="submit" :disabled="loading || !isFormValid" class="btn btn-primary">
          <span :style="{ visibility: loading ? 'hidden' : 'visible' }">Create Account</span>
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
          <p>Already have an account? <router-link to="/login" class="link">Sign in</router-link></p>
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