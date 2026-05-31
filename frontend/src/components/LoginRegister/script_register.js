import { registrarUsuario } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';


export default {
  name: "register",

  data() {
    return {
      name: "",
      last_name: "",
      nickname: "",
      email: "",
      password: "",
      confirmPassword: "",
      mostrarPassword: false,
      mostrarConfirmPassword: false,
      aceptaTerminos: false,
      loading: false,
      errorMessage: ""
    };
  },

  computed: {

    nicknameValido() {
      var patron = /^[a-zA-Z0-9_]{3,30}$/;
      if (patron.test(this.nickname)) {
        return true;
      }
      return false;
    },

    // Filtramos dominios para que no se registre cualquier email tonto
    // de un solo uso, pegamos los mas comunes y ya
    emailDominioValido() {

      var dominiosPermitidos = [
        'gmail.com',
        'hotmail.com',
        'hotmail.es',
        'outlook.com',
        'outlook.es',
        'yahoo.com',
        'yahoo.es',
        'icloud.com',
        'live.com'
      ];

      var partes = this.email.split('@');

      if (partes.length !== 2) {
        return false;
      }

      var dominio = partes[1].toLowerCase();

      if (dominiosPermitidos.indexOf(dominio) !== -1) {
        return true;
      }
      return false;
    },

    formularioValido() {

      if (this.name.length < 1 || this.name.length > 50) {
        return false;
      }

      if (this.last_name.length < 1 || this.last_name.length > 50) {
        return false;
      }

      if (!this.nicknameValido) {
        return false;
      }

      if (this.email.length < 1 || this.email.length > 100) {
        return false;
      }

      if (!this.emailDominioValido) {
        return false;
      }

      if (this.password.length < 8 || this.password.length > 50) {
        return false;
      }

      if (this.password !== this.confirmPassword) {
        return false;
      }

      if (!this.aceptaTerminos) {
        return false;
      }

      return true;
    }
  },

  methods: {

    async manejarRegistro() {

      try {
        this.loading = true;
        this.errorMessage = "";

        await registrarUsuario(
          this.name,
          this.last_name,
          this.nickname,
          this.email,
          this.password
        );

        notificaciones.success("Your account was created successfully. You can now sign in.", {
          title: "Account created"
        });

        this.$router.push('/login');

      } catch (error) {

        if (error.response && error.response.status === 409) {

          // Espera de 2s para que cueste mas probar nicknames/emails
          // a base de spamear el endpoint
          await new Promise(function (resolve) {
            setTimeout(resolve, 2000);
          });

          this.errorMessage = error.response.data.message;
          notificaciones.error(error.response.data.message, {
            title: "Registration failed"
          });

        } else {
          notificaciones.error("There was a problem creating your account. Please try again later.", {
            title: "Registration error"
          });
        }

      } finally {
        this.loading = false;
      }
    }
  }
};
