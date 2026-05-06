import { register } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';

export default {
    name: "register",
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
        await register(this.name, this.last_name, this.email, this.password);

        notificaciones.success("Tu cuenta fue creada correctamente. Ya puedes iniciar sesión.", {
          title: "Cuenta creada"
        });

        this.$router.push('/login');

      } catch (error) {

        if (error.response && error.response.status === 409) {

          await new Promise(resolve => setTimeout(resolve, 2000));

          this.errorMessage = error.response.data.message;
          notificaciones.error(error.response.data.message, {
            title: "No pudimos registrarte"
          });

        } else {
          notificaciones.error("Ocurrió un problema al crear la cuenta. Inténtalo de nuevo más tarde.", {
            title: "Error en el registro"
          });
        }
      } finally {
        this.loading = false;
      }
    }
  }
};

