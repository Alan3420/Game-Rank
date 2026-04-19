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
            <input id="name" v-model="name" type="text" placeholder="Tu nombre" class="form-input" required>
          </div>

          <div class="form-group">
            <label for="last_name" class="form-label">Apellidos</label>
            <input id="last_name" v-model="last_name" type="text" placeholder="Tus apellidos" class="form-input" required>
          </div>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Correo Electrónico</label>
          <input id="email" v-model="email" type="email" placeholder="tu@email.com" class="form-input" required>
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <input id="password" v-model="password" type="password" placeholder="Mínimo 6 caracteres" class="form-input" required>
        </div>

        <button type="submit" :disabled="loading" class="btn btn-primary">
          <span v-if="!loading">Crear Cuenta</span>
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

        <div class="register-footer">
          <p>¿Ya tienes cuenta? <router-link to="/login" class="link">Inicia sesión</router-link></p>
        </div>
      </form>
    </div>
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
      loading: false,
      errorMessage: ""
    };
  },
  methods: {
    async handleRegister() {
      try {
        this.loading = true;
        this.errorMessage = "";
        const response = await register(this.name, this.last_name, this.email, this.password);
        console.log("Usuario creado:", response);

        this.$router.push('/login');

      } catch (error) {

        if (error.response && error.response.status === 409) {

          await new Promise(resolve => setTimeout(resolve, 2000));

          this.errorMessage = error.response.data.message;
          console.log(error.response.data.message);
          
        } else {
          console.log("Error:", error.message);
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fb 0%, #f3f4fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-container {
  background: white;
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(20, 21, 63, 0.08);
  width: 100%;
  max-width: 480px;
  position: relative;
  overflow: hidden;
}

.register-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
}

.register-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.register-title {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 900;
  color: #1f1f35;
  letter-spacing: -0.02em;
}

.register-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 1rem;
  line-height: 1.6;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fafafa;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
  background: white;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary {
  background: #6366f1;
  color: white;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(99, 102, 241, 0.4);
}

.dots-loader {
  display: flex;
  gap: 4px;
  align-items: center;
}

.dots-loader span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: dots 1.4s infinite ease-in-out both;
}

.dots-loader span:nth-child(1) { animation-delay: -0.32s; }
.dots-loader span:nth-child(2) { animation-delay: -0.16s; }

@keyframes dots {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 0.9rem;
  border: 1px solid #fecaca;
}

.register-footer {
  text-align: center;
  margin-top: 1rem;
}

.register-footer p {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.link {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link:hover {
  color: #4f46e5;
  text-decoration: underline;
}

@media (max-width: 640px) {
  .form-row{
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  .register-container {
    padding: 2rem;
    margin: 0;
  }

  .register-page{
    margin: 0;
    padding: 10px;
  }

  .register-title {
    font-size: 1.75rem;
  }
}
</style>