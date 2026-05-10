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
  computed: {
    isFormValid() {
      return (
        this.name.length >= 1 && this.name.length <= 50 &&
        this.last_name.length >= 1 && this.last_name.length <= 50 &&
        this.email.length > 0 && this.email.length <= 100 &&
        this.password.length >= 8 && this.password.length <= 50
      );
    }
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

