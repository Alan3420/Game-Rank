import { register } from "../../services/user_service";

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

