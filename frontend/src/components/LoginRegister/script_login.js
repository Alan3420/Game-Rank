import { autenticarUsuario } from "../../services/user_service";
import { estadoAutenticacion } from '../../store/autenticacion';
import { notificaciones } from '../../store/notificaciones';

// Componente del formulario de inicio de sesion.
// Maneja los dos inputs (email y password), el toggle de "ver contrasena"
// y la llamada al backend cuando se envia el formulario.
export default {
  name: "login",

  data() {
    return {
      email: "",
      password: "",
      mostrarPassword: false,
      loading: false,
      errorMessage: ""
    };
  },

  computed: {

    // Devuelve true solo cuando los campos cumplen las reglas minimas.
    // El boton de submit usa esto para activarse o quedar deshabilitado.
    formularioValido() {

      var emailValido = false;
      if (this.email.length > 0 && this.email.length <= 100) {
        emailValido = true;
      }

      var passwordValida = false;
      if (this.password.length >= 8 && this.password.length <= 50) {
        passwordValida = true;
      }

      if (emailValido && passwordValida) {
        return true;
      }
      return false;
    }
  },

  methods: {

    // Maneja el submit del formulario. Pide al backend autenticar las
    // credenciales y, si todo va bien, guarda el usuario y token en el
    // store global y redirige al home.
    async manejarInicioSesion() {

      try {
        this.loading = true;
        this.errorMessage = "";

        const response = await autenticarUsuario(this.email, this.password);

        estadoAutenticacion.iniciarSesion(response.user, response.token);

        notificaciones.success(
          'Welcome ' + response.user.name + ", you've signed in successfully.",
          { title: "Welcome back!" }
        );

        this.$router.push('/');

      } catch (error) {

        // 401 = credenciales incorrectas. Esperamos 2s antes de mostrar el
        // mensaje para frenar intentos masivos (ataque de fuerza bruta basico).
        if (error.response && error.response.status === 401) {

          await new Promise(function (resolve) {
            setTimeout(resolve, 2000);
          });

          this.errorMessage = error.response.data.message;
          notificaciones.error(error.response.data.message, {
            title: "Incorrect credentials"
          });

        } else {
          notificaciones.error("We couldn't connect to the server. Please try again later.", {
            title: "Connection error"
          });
        }

      } finally {
        this.loading = false;
      }
    }
  }
};
