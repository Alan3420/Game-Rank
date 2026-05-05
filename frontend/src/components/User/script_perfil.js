import { estadoAutenticacion } from '../../store/autenticacion'; 
import { list_favorites} from "../../services/favorites_area";

export default {
  name: "perfil",
  data() {
    return {
      estadoAutenticacion,
      favoritos: []
    };
  },
  async mounted() {
    await this.cargarFavoritos();
  },
  methods: {
    async cargarFavoritos() {
      try {
        const data = await list_favorites();
        this.favoritos = data.favorites;
      } catch (error) {
        console.error(error.listfavoritos.message);
      }
    }
  }
}