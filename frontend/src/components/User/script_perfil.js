import { estadoAutenticacion } from '../../store/autenticacion';
import { list_favorites, removeTOFavorite } from "../../services/favorites_area";
import { changePassword } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted, ref } from 'vue';

export default {
  name: "perfil",
  data() {
    return {
      estadoAutenticacion,
      favoritos: [],
      favoritosLoading: true,
      remover: null,
      mostrarModalEditar: false,
      mostrarModalCambiarContraseña: false,
      mostrarMenuEditar: false,
      formularioCambiarContraseña: {
        actual: '',
        nueva: '',
        confirmar: ''
      },
      errorCambiarContraseña: '',
      cambiandoContraseña: false,
      router: null
    };
  },
  computed: {
    isAdmin() {
      return estadoAutenticacion.usuario?.role === 'admin';
    }
  },
  async mounted() {
    this.router = useRouter();
    await this.cargarFavoritos();
    document.addEventListener('mousedown', this.handleClickOutsideMenu);
  },
  beforeUnmount() {
    document.removeEventListener('mousedown', this.handleClickOutsideMenu);
  },
  methods: {
    abrirModalEditar() {
      this.mostrarModalEditar = true;
    },
    cerrarModalEditar() {
      this.mostrarModalEditar = false;
    },
    async cargarFavoritos() {
      this.favoritosLoading = true;
      try {
        const data = await list_favorites();
        this.favoritos = data.favorites;
      } catch (error) {
        console.error(error.listfavoritos.message);
      } finally {
        this.favoritosLoading = false;
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
    },
    goToDetail(gameId) {
      this.router.push(`/game/${gameId}`);
    },
    irAPanelAdmin() {
      this.router.push('/admin/users');
    },
    irAConfigAdmin() {
      notificaciones.info("Panel de configuración en desarrollo.", { title: "Próximamente" });
    },
    abrirModalCambiarContraseña() {
      this.mostrarMenuEditar = false;
      this.mostrarModalCambiarContraseña = true;
      this.errorCambiarContraseña = '';
      this.formularioCambiarContraseña = { actual: '', nueva: '', confirmar: '' };
    },
    cerrarModalCambiarContraseña() {
      this.mostrarModalCambiarContraseña = false;
      this.formularioCambiarContraseña = { actual: '', nueva: '', confirmar: '' };
      this.errorCambiarContraseña = '';
    },
    handleClickOutsideMenu(e) {
      const menuRef = this.$refs.menuEditarRef;
      if (menuRef && !menuRef.contains(e.target)) {
        this.mostrarMenuEditar = false;
      }
    },
    async guardarCambioContraseña() {
      const { actual, nueva, confirmar } = this.formularioCambiarContraseña;

      if (!actual || !nueva || !confirmar) {
        this.errorCambiarContraseña = 'Todos los campos son obligatorios.';
        return;
      }

      if (nueva.length < 8) {
        this.errorCambiarContraseña = 'La nueva contraseña debe tener al menos 8 caracteres.';
        return;
      }

      if (nueva !== confirmar) {
        this.errorCambiarContraseña = 'Las contraseñas no coinciden.';
        return;
      }

      this.cambiandoContraseña = true;
      this.errorCambiarContraseña = '';

      try {
        await changePassword(actual, nueva);
        this.cerrarModalCambiarContraseña();
        notificaciones.success("Tu contraseña ha sido actualizada correctamente.", {
          title: "Contraseña cambio exitoso"
        });
      } catch (error) {
        console.error('Error al cambiar contraseña:', error);
        let mensaje = "No pudimos cambiar tu contraseña.";
        if (error.response?.data?.message) {
          mensaje = error.response.data.message;
        }
        this.errorCambiarContraseña = mensaje;
      } finally {
        this.cambiandoContraseña = false;
      }
    }
  }
}