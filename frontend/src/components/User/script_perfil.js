import { estadoAutenticacion } from '../../store/autenticacion';
import { list_favorites, removeTOFavorite } from "../../services/favorites_area";
import { changePassword, updateUser } from "../../services/user_service";
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
      formularioEditar: {
        name: '',
        last_name: ''
      },
      errorEditar: '',
      guardandoEditar: false,
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
      this.mostrarMenuEditar = false;
      this.formularioEditar = {
        name: estadoAutenticacion.usuario?.name || '',
        last_name: estadoAutenticacion.usuario?.last_name || ''
      };
      this.errorEditar = '';
      this.mostrarModalEditar = true;
    },
    cerrarModalEditar() {
      if (this.guardandoEditar) return;
      this.mostrarModalEditar = false;
      this.errorEditar = '';
    },
    async guardarCambiosPerfil() {
      const name = this.formularioEditar.name?.trim();
      const last_name = this.formularioEditar.last_name?.trim();

      if (!name || !last_name) {
        this.errorEditar = 'El nombre y el apellido son obligatorios.';
        return;
      }

      if (name.length > 50 || last_name.length > 50) {
        this.errorEditar = 'Cada campo debe tener máximo 50 caracteres.';
        return;
      }

      const sinCambios =
        name === estadoAutenticacion.usuario?.name &&
        last_name === estadoAutenticacion.usuario?.last_name;

      if (sinCambios) {
        this.errorEditar = 'No has hecho ningún cambio.';
        return;
      }

      this.guardandoEditar = true;
      this.errorEditar = '';

      try {
        const id_user = estadoAutenticacion.usuario.id_user;
        const response = await updateUser(id_user, { name, last_name });

        estadoAutenticacion.actualizarUsuario({ name, last_name });

        this.mostrarModalEditar = false;
        notificaciones.success("Tu información ha sido actualizada.", {
          title: "Perfil actualizado"
        });
      } catch (error) {
        console.error('Error al actualizar perfil:', error);
        let mensaje = "No pudimos actualizar tu información.";
        if (error.response?.data?.message) {
          mensaje = error.response.data.message;
        }
        this.errorEditar = mensaje;
      } finally {
        this.guardandoEditar = false;
      }
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