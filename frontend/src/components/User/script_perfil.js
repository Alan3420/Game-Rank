import { estadoAutenticacion } from '../../store/autenticacion';
import { list_favorites, removeTOFavorite } from "../../services/favorites_area";

export default {
  name: "perfil",
  data() {
    return {
      estadoAutenticacion,
      favoritos: [],
      remover: null
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
    },
    async quitarFavorito(idGame) {
      this.remover = idGame;
      try {
        await removeTOFavorite(idGame);
        this.favoritos = this.favoritos.filter(f => f.id !== idGame);
      } catch (error) {
        console.error("Error al quitar favorito:", error);
      } finally {
        this.remover = null;
      }
    }
  }
}