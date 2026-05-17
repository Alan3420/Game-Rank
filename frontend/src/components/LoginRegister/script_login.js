import { login } from "../../services/user_service";
import { estadoAutenticacion } from '../../store/autenticacion';
import { notificaciones } from '../../store/notificaciones';

export default {
    name: "login",
  data() {
    return {
      email: "",
      password: "",
      mostrarPassword: false,
      loading: false,
      errorMessage: ""
    }
  },
  computed: {
    isFormValid() {
      return (
        this.email.length > 0 && this.email.length <= 100 &&
        this.password.length >= 8 && this.password.length <= 50
      );
    }
  },
  methods: {
    async handleLogin() {
      try {
        this.loading = true;
        this.errorMessage = "";
        const response = await login(this.email, this.password);

        estadoAutenticacion.iniciarSesion(response.user, response.token);

        notificaciones.success(`Welcome ${response.user.name}, you've signed in successfully.`, {
          title: "Welcome back!"
        });

        this.$router.push('/');

      } catch (error) {
        if (error.response && error.response.status === 401) {
          await new Promise(resolve => setTimeout(resolve, 2000));
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
}


