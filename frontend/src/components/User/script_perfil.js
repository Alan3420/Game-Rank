import { estadoAutenticacion } from '../../store/autenticacion';
import { list_favorites, removeTOFavorite, addTOFavorite } from "../../services/favorites_area";
import { listGameStatuses, listGameStatusesFull } from "../../services/user_game_status";
import { changePassword, updateUser, getEstadisticasUsuario } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted, ref } from 'vue';
import { STATUS_META, STATUS_LIST } from '../../utils/statusMeta.js';

export default {
  name: "perfil",
  data() {
    return {
      estadoAutenticacion,
      STATUS_META,
      STATUS_LIST,
      favoritos: [],
      favoritosLoading: true,
      remover: null,
      paginaFavoritos: 1,
      FAVS_POR_PAGINA: 8,
      statuses: new Map(),
      coleccion: [],
      coleccionLoading: true,
      filtroColeccion: 'todos',
      favLoadingId: null,
      stats: null,
      statsLoading: true,
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
        last_name: '',
        nickname: ''
      },
      errorEditar: '',
      guardandoEditar: false,
      router: null
    };
  },
  computed: {
    isAdmin() {
      return estadoAutenticacion.usuario?.role === 'admin';
    },
    coleccionFiltrada() {
      if (this.filtroColeccion === 'todos') return this.coleccion;
      return this.coleccion.filter(item => item.status === this.filtroColeccion);
    },
    coleccionPorEstado() {
      const result = {};
      for (const key of STATUS_LIST) {
        result[key] = this.coleccion.filter(item => item.status === key);
      }
      return result;
    },
    favoritosIds() {
      return new Set(this.favoritos.map(f => f.id));
    },
    totalPaginasFavoritos() {
      return Math.max(1, Math.ceil(this.favoritos.length / this.FAVS_POR_PAGINA));
    },
    favoritosPaginados() {
      const inicio = (this.paginaFavoritos - 1) * this.FAVS_POR_PAGINA;
      return this.favoritos.slice(inicio, inicio + this.FAVS_POR_PAGINA);
    }
  },
  async mounted() {
    this.router = useRouter();
    await Promise.all([
      this.cargarFavoritos(),
      this.loadStatuses(),
      this.cargarColeccion(),
      this.cargarEstadisticas()
    ]);
    document.addEventListener('mousedown', this.handleClickOutsideMenu);
  },
  beforeUnmount() {
    document.removeEventListener('mousedown', this.handleClickOutsideMenu);
  },
  methods: {
    async cargarEstadisticas() {
      this.statsLoading = true;
      try {
        this.stats = await getEstadisticasUsuario();
      } catch {
        this.stats = null;
      } finally {
        this.statsLoading = false;
      }
    },

    abrirModalEditar() {
      this.mostrarMenuEditar = false;
      this.formularioEditar = {
        name: estadoAutenticacion.usuario?.name || '',
        last_name: estadoAutenticacion.usuario?.last_name || '',
        nickname: estadoAutenticacion.usuario?.nickname || ''
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
      const nickname = this.formularioEditar.nickname?.trim();

      if (!name || !last_name) {
        this.errorEditar = 'El nombre y el apellido son obligatorios.';
        return;
      }

      if (name.length > 50 || last_name.length > 50) {
        this.errorEditar = 'Cada campo debe tener máximo 50 caracteres.';
        return;
      }

      if (nickname && !/^[a-zA-Z0-9_]{3,30}$/.test(nickname)) {
        this.errorEditar = 'El nickname solo puede contener letras, números y _ (mín. 3, máx. 30 caracteres).';
        return;
      }

      const sinCambios =
        name === estadoAutenticacion.usuario?.name &&
        last_name === estadoAutenticacion.usuario?.last_name &&
        nickname === (estadoAutenticacion.usuario?.nickname || '');

      if (sinCambios) {
        this.errorEditar = 'No has hecho ningún cambio.';
        return;
      }

      this.guardandoEditar = true;
      this.errorEditar = '';

      try {
        const id_user = estadoAutenticacion.usuario.id_user;
        await updateUser(id_user, { name, last_name, nickname: nickname || null });

        estadoAutenticacion.actualizarUsuario({ name, last_name, nickname: nickname || null });

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
    async loadStatuses() {
      try {
        const data = await listGameStatuses();
        const map = new Map();
        for (const s of data.statuses) {
          map.set(s.id_game_api, s.status);
        }
        this.statuses = map;
      } catch {
        // fallo silencioso
      }
    },

    handleStatusUpdate({ gameId, status }) {
      const map = new Map(this.statuses);
      if (status) {
        map.set(gameId, status);
      } else {
        map.delete(gameId);
      }
      this.statuses = map;
      // Refrescar la colección por estados también
      if (status) {
        const idx = this.coleccion.findIndex(c => c.game.id === gameId);
        if (idx !== -1) {
          this.coleccion[idx] = { ...this.coleccion[idx], status };
        }
      } else {
        this.coleccion = this.coleccion.filter(c => c.game.id !== gameId);
      }
    },

    async cargarColeccion() {
      this.coleccionLoading = true;
      try {
        const data = await listGameStatusesFull();
        this.coleccion = data.statuses;
      } catch {
        this.coleccion = [];
      } finally {
        this.coleccionLoading = false;
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
    async toggleFavoritoColeccion(gameId) {
      if (this.favLoadingId === gameId) return;
      this.favLoadingId = gameId;
      try {
        if (this.favoritosIds.has(gameId)) {
          await removeTOFavorite(gameId);
          this.favoritos = this.favoritos.filter(f => f.id !== gameId);
          if (this.paginaFavoritos > this.totalPaginasFavoritos) this.paginaFavoritos = this.totalPaginasFavoritos;
          notificaciones.success("Juego eliminado de tus favoritos.", { title: "Favorito eliminado" });
        } else {
          await addTOFavorite(gameId);
          const gameData = this.coleccion.find(c => c.game.id === gameId)?.game;
          if (gameData) this.favoritos.push(gameData);
          notificaciones.success("Juego añadido a tus favoritos.", { title: "Favorito añadido" });
        }
      } catch (error) {
        notificaciones.error("No pudimos actualizar favoritos.", { title: "Error" });
      } finally {
        this.favLoadingId = null;
      }
    },
    async quitarFavorito(idGame) {
      this.remover = idGame;
      try {
        await removeTOFavorite(idGame);
        this.favoritos = this.favoritos.filter(f => f.id !== idGame);
        if (this.paginaFavoritos > this.totalPaginasFavoritos) this.paginaFavoritos = this.totalPaginasFavoritos;
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
    irAModeracion() {
      this.router.push('/admin/comments');
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