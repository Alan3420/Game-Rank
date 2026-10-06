<template>
  <div class="auth auth--register card-world">
    <div class="auth-shell">

      <div class="auth-intro">
        <h1 class="auth-title">Join Game Rank</h1>
        <p class="auth-lede">Create your account and start your album.</p>
        <ul class="auth-perks">
          <li><i aria-hidden="true" class="pi pi-bookmark"></i><span>Collect games as Pending, Playing, Paused or Completed</span></li>
          <li><i aria-hidden="true" class="pi pi-heart"></i><span>Keep your favorites in one place</span></li>
          <li><i aria-hidden="true" class="pi pi-star"></i><span>Rate and review, and shape the community trends</span></li>
        </ul>
      </div>

      <!-- carta de socio: el pie muestra el apodo segun se escribe -->
      <section class="auth-card cw-frame" aria-labelledby="auth-card-title">
        <div class="auth-card__face">
          <div class="auth-card__band">
            <h2 id="auth-card-title" class="auth-card__title">Create account</h2>
            <span class="auth-card__set">New member</span>
          </div>

          <form class="auth-form" novalidate @submit.prevent="manejarRegistro">
            <div class="form-row">
              <div class="form-group">
                <label for="name" class="form-label">First name</label>
                <input id="name" v-model="name" name="name" autocomplete="given-name" type="text"
                  placeholder="Your first name" class="form-input" :class="{ 'input-error': errorVisible.name }"
                  :aria-invalid="errorVisible.name ? 'true' : 'false'" aria-describedby="name-hint" maxlength="50" required>
                <span id="name-hint" class="form-hint form-hint--error">{{ errorVisible.name }}</span>
              </div>

              <div class="form-group">
                <label for="last_name" class="form-label">Last name</label>
                <input id="last_name" v-model="last_name" name="last_name" autocomplete="family-name" type="text"
                  placeholder="Your last name" class="form-input" :class="{ 'input-error': errorVisible.last_name }"
                  :aria-invalid="errorVisible.last_name ? 'true' : 'false'" aria-describedby="last-name-hint" maxlength="50" required>
                <span id="last-name-hint" class="form-hint form-hint--error">{{ errorVisible.last_name }}</span>
              </div>
            </div>

            <div class="form-group">
              <label for="nickname" class="form-label">Nickname</label>
              <div class="input-wrap">
                <span class="input-prefix" aria-hidden="true">@</span>
                <input id="nickname" v-model="nickname" name="nickname" autocomplete="username" spellcheck="false"
                  type="text" placeholder="your_nickname" class="form-input form-input--prefix"
                  :class="{ 'input-error': errorVisible.nickname }" :aria-invalid="errorVisible.nickname ? 'true' : 'false'"
                  aria-describedby="nickname-hint" maxlength="30" required>
              </div>
              <span id="nickname-hint" class="form-hint" :class="{ 'form-hint--error': errorVisible.nickname }">
                3–30 characters: letters, numbers and underscores.
              </span>
            </div>

            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input id="email" v-model="email" name="email" autocomplete="email" spellcheck="false" type="email"
                placeholder="your@gmail.com" class="form-input" :class="{ 'input-error': errorVisible.email }"
                :aria-invalid="errorVisible.email ? 'true' : 'false'" aria-describedby="email-hint"
                maxlength="100" required>
              <span id="email-hint" class="form-hint" :class="{ 'form-hint--error': errorVisible.email }">
                {{ errorVisible.email || 'We only use it to sign you in.' }}
              </span>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="password" class="form-label">Password</label>
                <div class="input-wrap">
                  <input id="password" v-model="password" name="password" autocomplete="new-password"
                    :type="mostrarPassword ? 'text' : 'password'" placeholder="At least 8 characters"
                    class="form-input form-input--eye" :class="{ 'input-error': errorVisible.password }"
                    :aria-invalid="errorVisible.password ? 'true' : 'false'" aria-describedby="password-hint"
                    maxlength="50" required>
                  <button type="button" class="eye-btn" :aria-label="mostrarPassword ? 'Hide password' : 'Show password'"
                    :aria-pressed="mostrarPassword" @click="mostrarPassword = !mostrarPassword">
                    <i aria-hidden="true" class="pi" :class="mostrarPassword ? 'pi-eye-slash' : 'pi-eye'"></i>
                  </button>
                </div>
                <span id="password-hint" class="form-hint form-hint--error">{{ errorVisible.password }}</span>
              </div>

              <div class="form-group">
                <label for="confirmPassword" class="form-label">Confirm password</label>
                <div class="input-wrap">
                  <input id="confirmPassword" v-model="confirmPassword" name="confirm_password" autocomplete="new-password"
                    :type="mostrarConfirmPassword ? 'text' : 'password'" placeholder="Repeat it"
                    class="form-input form-input--eye" :class="{ 'input-error': errorVisible.confirm }"
                    :aria-invalid="errorVisible.confirm ? 'true' : 'false'" aria-describedby="confirm-hint"
                    maxlength="50" required>
                  <button type="button" class="eye-btn" :aria-label="mostrarConfirmPassword ? 'Hide password' : 'Show password'"
                    :aria-pressed="mostrarConfirmPassword" @click="mostrarConfirmPassword = !mostrarConfirmPassword">
                    <i aria-hidden="true" class="pi" :class="mostrarConfirmPassword ? 'pi-eye-slash' : 'pi-eye'"></i>
                  </button>
                </div>
                <span id="confirm-hint" class="form-hint form-hint--error">{{ errorVisible.confirm }}</span>
              </div>
            </div>

            <div class="form-group">
              <label class="auth-check">
                <input id="terms" v-model="aceptaTerminos" type="checkbox" class="auth-check__box"
                  :aria-invalid="errorVisible.terminos ? 'true' : 'false'" aria-describedby="terms-hint">
                <span>
                  I have read and accept the
                  <router-link to="/terminos" target="_blank" class="auth-link">Terms and Conditions</router-link>
                </span>
              </label>
              <span id="terms-hint" class="form-hint form-hint--error">{{ errorVisible.terminos }}</span>
            </div>

            <div v-if="errorMessage" class="error-alert" role="alert">
              <i aria-hidden="true" class="pi pi-exclamation-circle"></i>
              {{ errorMessage }}
            </div>

            <button type="submit" :disabled="loading" class="auth-btn">
              <i v-if="loading" aria-hidden="true" class="pi pi-spin pi-spinner"></i>
              {{ loading ? 'Creating account…' : 'Create account' }}
            </button>

            <p class="auth-alt">Already a member? <router-link to="/login" class="auth-link">Sign in</router-link></p>
          </form>

          <div class="auth-card__foot" aria-hidden="true">
            <span class="auth-card__no">@{{ nickname || 'your_nickname' }}</span>
            <span>Member since {{ anioActual }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>


<script>
    import jsRegister from "./script_register.js";

    export default {
        name: 'register',
        mixins: [jsRegister],
        computed: {
            anioActual() {
                return new Date().getFullYear();
            }
        }
    };
</script>

<style scoped src="./style_auth.css"></style>
