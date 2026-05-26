import { registrarUsuario } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';

// Componente del formulario de registro de nuevos usuarios.
// Tiene mas validaciones que el de login porque aqui hay que comprobar
// nickname, dominio de email, longitud y confirmacion de contrasena, etc.
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

    // El nickname acepta letras, numeros y guion bajo, entre 3 y 30 caracteres.
    // Lo validamos con una expresion regular sencilla.
    nicknameValido() {
      var patron = /^[a-zA-Z0-9_]{3,30}$/;
      if (patron.test(this.nickname)) {
        return true;
      }
      return false;
    },

    // Limitamos los dominios de correo aceptados a los mas comunes para
    // evitar registros con emails de un solo uso.
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

    // El boton de submit solo se activa cuando TODAS las reglas se cumplen.
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

    // Maneja el submit del formulario. Si el backend responde 409 quiere
    // decir que el email o nickname ya estaba registrado.
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

          // Pequena espera para que no se pueda spamear el endpoint
          // probando combinaciones de email/nickname.
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
