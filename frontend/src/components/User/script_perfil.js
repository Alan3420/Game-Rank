import { estadoAutenticacion } from '../../store/autenticacion';
import { list_favorites, removeTOFavorite } from "../../services/favorites_area";
import { notificaciones } from '../../store/notificaciones';

export default {
  name: "perfil",
  data() {
    return {
      estadoAutenticacion,
      favoritos: [],
      remover: null,
      mostrarModalEditar: false
    };
  },
  async mounted() {
    await this.cargarFavoritos();
  },
  methods: {
    abrirModalEditar() {
      this.mostrarModalEditar = true;
    },
    cerrarModalEditar() {
      this.mostrarModalEditar = false;
    },
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
        notificaciones.success("Juego eliminado de tus favoritos.", { title: "Favorito eliminado" });
      } catch (error) {
        console.error("Error al quitar favorito:", error);
        notificaciones.error("No pudimos eliminar el juego de favoritos.", {
          title: "Error en favoritos"
        });
      } finally {
        this.remover = null;
      }
    }
  }
}