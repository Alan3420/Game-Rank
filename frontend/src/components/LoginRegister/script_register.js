import { registrarUsuario } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';
import { mensajeDeError } from '../../utils/mensajeError.js';


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
      // Tras el primer envio fallido se muestran todos los errores
      intentado: false,
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

    // Mensaje por campo; vacio si el campo esta bien
    erroresCampos() {
      var e = {};
      e.name = this.name.trim().length < 1 ? 'Enter your first name.' : '';
      e.last_name = this.last_name.trim().length < 1 ? 'Enter your last name.' : '';
      e.nickname = this.nicknameValido ? '' : '3–30 characters: letters, numbers and underscores.';
      if (this.email.length < 1) {
        e.email = 'Enter your email.';
      } else if (!this.emailDominioValido) {
        e.email = 'Use a Gmail, Outlook, Hotmail, Yahoo, iCloud or Live address.';
      } else {
        e.email = '';
      }
      e.password = this.password.length < 8 ? 'Use at least 8 characters.' : '';
      e.confirm = this.password !== this.confirmPassword ? "Passwords don't match." : '';
      e.terminos = this.aceptaTerminos ? '' : 'Accept the Terms and Conditions to continue.';
      return e;
    },

    // Se muestra el error de un campo si ya se intento enviar o si el
    // campo tiene texto y es invalido
    errorVisible() {
      var e = this.erroresCampos;
      return {
        name: this.intentado ? e.name : '',
        last_name: this.intentado ? e.last_name : '',
        nickname: (this.intentado || this.nickname) ? e.nickname : '',
        email: (this.intentado || this.email) ? e.email : '',
        password: this.intentado ? e.password : '',
        confirm: (this.intentado || this.confirmPassword) ? e.confirm : '',
        terminos: this.intentado ? e.terminos : ''
      };
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

      if (!this.formularioValido) {
        this.intentado = true;
        // Foco en el primer campo con error
        var orden = [['name', 'name'], ['last_name', 'last_name'], ['nickname', 'nickname'], ['email', 'email'],
          ['password', 'password'], ['confirm', 'confirmPassword'], ['terminos', 'terms']];
        for (var i = 0; i < orden.length; i++) {
          if (this.erroresCampos[orden[i][0]]) {
            var el = document.getElementById(orden[i][1]);
            if (el) {
              el.focus();
            }
            break;
          }
        }
        return;
      }

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

          this.errorMessage = mensajeDeError(error, 'That email or nickname is already in use.');
          notificaciones.error(this.errorMessage, {
            title: "Registration failed"
          });

        } else {
          notificaciones.error("Account wasn't created. Check your details and try again in a few minutes.", {
            title: "Registration error"
          });
        }

      } finally {
        this.loading = false;
      }
    }
  }
};
