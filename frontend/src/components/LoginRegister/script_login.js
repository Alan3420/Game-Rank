import { login } from "../../services/user_service";
import { estadoAutenticacion } from '../../store/autenticacion';

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

        console.log("Inicio de Sesion correcto");

        estadoAutenticacion.iniciarSesion(response.user, response.token);

        this.$router.push('/content/overview');

      } catch (error) {
        if(error.response && error.response.status === 401){
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
}


