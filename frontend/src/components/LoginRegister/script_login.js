import { login } from "../../services/user_service";
import { estadoAutenticacion } from '../../store/autenticacion';
import { notificaciones } from '../../store/notificaciones';

export default {
    name: "login",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      errorMessage: ""
    }
  },
  methods: {
    async handleLogin() {
      try {
        this.loading = true;
        this.errorMessage = "";
        const response = await login(this.email, this.password);

        estadoAutenticacion.iniciarSesion(response.user, response.token);

        notificaciones.success(`Bienvenido ${response.user.name}, sesión iniciada correctamente.`, {
          title: "¡Hola de nuevo!"
        });

        this.$router.push('/content/overview');

      } catch (error) {
        if (error.response && error.response.status === 401) {
          await new Promise(resolve => setTimeout(resolve, 2000));
          this.errorMessage = error.response.data.message;
          notificaciones.error(error.response.data.message, {
            title: "Credenciales incorrectas"
          });
        } else {
          notificaciones.error("No pudimos conectar con el servidor. Inténtalo de nuevo más tarde.", {
            title: "Error de conexión"
          });
        }
      } finally {
        this.loading = false;
      }
    }
  }
}


