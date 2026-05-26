import { estadoAutenticacion } from '../../store/autenticacion';
import { obtenerListaDeFavoritos, quitarDeFavoritos, agregarAFavoritos } from "../../services/favorites_area";
import { listarEstadosDeJuego, listarEstadosDeJuegoCompletos } from "../../services/user_game_status";
import { cambiarContrasena, actualizarUsuario, obtenerEstadisticasUsuario } from "../../services/user_service";
import { notificaciones } from '../../store/notificaciones';
import { useRouter } from 'vue-router';
import { STATUS_META, STATUS_LIST } from '../../utils/statusMeta.js';

// Componente de la pantalla de perfil. Reune todo lo "personal" del usuario:
// banner con sus datos, estadisticas, lista de coleccion por estado, lista
// de favoritos paginada, y los modales para editar perfil / cambiar
// contrasena. Tambien expone los accesos al panel de admin si corresponde.
//
// Nota: las claves "formularioCambiarContraseña" y sus relacionadas se
// mantienen con la "ñ" porque coinciden con los v-model del template.
export default {
  name: "perfil",

  data() {
    return {
      estadoAutenticacion: estadoAutenticacion,
      STATUS_META: STATUS_META,
      STATUS_LIST: STATUS_LIST,

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

    // Marca al usuario actual como admin para mostrar/ocultar opciones.
    isAdmin() {
      if (!estadoAutenticacion.usuario) {
        return false;
      }
      if (estadoAutenticacion.usuario.role === 'admin') {
        return true;
      }
      return false;
    },

    // Devuelve la coleccion filtrada por el tab elegido en la UI.
    // Si el tab es "todos" devolvemos la lista completa.
    coleccionFiltrada() {

      if (this.filtroColeccion === 'todos') {
        return this.coleccion;
      }

      var resultado = [];
      for (var i = 0; i < this.coleccion.length; i++) {
        if (this.coleccion[i].status === this.filtroColeccion) {
          resultado.push(this.coleccion[i]);
        }
      }
      return resultado;
    },

    // Devuelve un objeto agrupado: para cada estado, la lista de items.
    // Lo dejamos preparado por si en el futuro hace falta otra vista.
    coleccionPorEstado() {
      var resultado = {};
      for (var i = 0; i < STATUS_LIST.length; i++) {
        var clave = STATUS_LIST[i];
        resultado[clave] = [];
      }
      for (var j = 0; j < this.coleccion.length; j++) {
        var item = this.coleccion[j];
        if (resultado[item.status]) {
          resultado[item.status].push(item);
        }
      }
      return resultado;
    },

    // Set con los id de juego que ya estan en favoritos. Usar Set
    // permite preguntar ".has(id)" en O(1) desde el template.
    favoritosIds() {
      var ids = new Set();
      for (var i = 0; i < this.favoritos.length; i++) {
        ids.add(this.favoritos[i].id);
      }
      return ids;
    },

    // Numero total de paginas de la lista de favoritos.
    totalPaginasFavoritos() {
      var calculado = Math.ceil(this.favoritos.length / this.FAVS_POR_PAGINA);
      if (calculado < 1) {
        return 1;
      }
      return calculado;
    },

    // Devuelve solo los favoritos visibles en la pagina actual.
    favoritosPaginados() {
      var inicio = (this.paginaFavoritos - 1) * this.FAVS_POR_PAGINA;
      var fin = inicio + this.FAVS_POR_PAGINA;
      return this.favoritos.slice(inicio, fin);
    }
  },

  async mounted() {
    this.router = useRouter();

    await Promise.all([
      this.cargarFavoritos(),
      this.cargarEstadosDeColeccion(),
      this.cargarColeccion(),
      this.cargarEstadisticas()
    ]);

    document.addEventListener('mousedown', this.manejarClicFueraDelMenu);
  },

  beforeUnmount() {
    document.removeEventListener('mousedown', this.manejarClicFueraDelMenu);
  },

  methods: {

    // Pide al backend las estadisticas del usuario (favoritos totales,
    // juegos completados, media de rating, etc.) para pintarlas arriba.
    async cargarEstadisticas() {
      this.statsLoading = true;
      try {
        this.stats = await obtenerEstadisticasUsuario();
      } catch (error) {
        this.stats = null;
      } finally {
        this.statsLoading = false;
      }
    },

    // Abre el modal de edicion de perfil. Antes de abrirlo precargamos el
    // formulario con los datos actuales del usuario para que vea los
    // valores que esta a punto de cambiar.
    abrirModalEditar() {
      this.mostrarMenuEditar = false;

      var usuario = estadoAutenticacion.usuario;
      var datosIniciales = {
        name: '',
        last_name: '',
        nickname: ''
      };
      if (usuario) {
        if (usuario.name) {
          datosIniciales.name = usuario.name;
        }
        if (usuario.last_name) {
          datosIniciales.last_name = usuario.last_name;
        }
        if (usuario.nickname) {
          datosIniciales.nickname = usuario.nickname;
        }
      }
      this.formularioEditar = datosIniciales;

      this.errorEditar = '';
      this.mostrarModalEditar = true;
    },

    cerrarModalEditar() {
      if (this.guardandoEditar) {
        return;
      }
      this.mostrarModalEditar = false;
      this.errorEditar = '';
    },

    // Valida los datos del formulario y, si todo va bien, manda la
    // actualizacion al backend y refresca el estado local del usuario.
    async guardarCambiosPerfil() {

      var name = this.formularioEditar.name;
      if (name) {
        name = name.trim();
      } else {
        name = '';
      }

      var last_name = this.formularioEditar.last_name;
      if (last_name) {
        last_name = last_name.trim();
      } else {
        last_name = '';
      }

      var nickname = this.formularioEditar.nickname;
      if (nickname) {
        nickname = nickname.trim();
      } else {
        nickname = '';
      }

      if (!name || !last_name) {
        this.errorEditar = 'First name and last name are required.';
        return;
      }

      if (name.length > 50 || last_name.length > 50) {
        this.errorEditar = 'Each field must have a maximum of 50 characters.';
        return;
      }

      if (nickname && !/^[a-zA-Z0-9_]{3,30}$/.test(nickname)) {
        this.errorEditar = 'Nickname can only contain letters, numbers and _ (min. 3, max. 30 characters).';
        return;
      }

      var usuarioActual = estadoAutenticacion.usuario;
      var nicknameActual = '';
      if (usuarioActual && usuarioActual.nickname) {
        nicknameActual = usuarioActual.nickname;
      }

      var sinCambios = false;
      if (usuarioActual &&
          name === usuarioActual.name &&
          last_name === usuarioActual.last_name &&
          nickname === nicknameActual) {
        sinCambios = true;
      }
      if (sinCambios) {
        this.errorEditar = 'No changes were made.';
        return;
      }

      this.guardandoEditar = true;
      this.errorEditar = '';

      try {
        var id_user = estadoAutenticacion.usuario.id_user;
        var nicknameFinal = null;
        if (nickname) {
          nicknameFinal = nickname;
        }

        await actualizarUsuario(id_user, {
          name: name,
          last_name: last_name,
          nickname: nicknameFinal
        });

        estadoAutenticacion.actualizarUsuario({
          name: name,
          last_name: last_name,
          nickname: nicknameFinal
        });

        this.mostrarModalEditar = false;
        notificaciones.success("Your information has been updated.", {
          title: "Profile updated"
        });

      } catch (error) {
        console.error('Error al actualizar perfil:', error);

        var mensaje = "We couldn't update your information.";
        if (error.response && error.response.data && error.response.data.message) {
          mensaje = error.response.data.message;
        }
        this.errorEditar = mensaje;

      } finally {
        this.guardandoEditar = false;
      }
    },

    // Pide los estados (id_juego + estado) para pintar el badge en las
    // cards de los favoritos del perfil.
    async cargarEstadosDeColeccion() {
      try {
        var data = await listarEstadosDeJuego();
        var mapa = new Map();
        for (var i = 0; i < data.statuses.length; i++) {
          mapa.set(data.statuses[i].id_game_api, data.statuses[i].status);
        }
        this.statuses = mapa;
      } catch (error) {
        // Fallo silencioso, no es critico para la pantalla.
      }
    },

    // Llamado cuando una card emite que su estado cambio. Actualiza el
    // mapa de estados y tambien la lista de coleccion para que la pestana
    // correspondiente refleje el cambio sin recargar la pagina.
    manejarActualizacionEstado(datos) {
      var gameId = datos.gameId;
      var status = datos.status;

      var mapa = new Map(this.statuses);
      if (status) {
        mapa.set(gameId, status);
      } else {
        mapa.delete(gameId);
      }
      this.statuses = mapa;

      if (status) {
        // Si el juego ya estaba en coleccion lo actualizamos in-place.
        for (var i = 0; i < this.coleccion.length; i++) {
          if (this.coleccion[i].game.id === gameId) {
            var copia = {};
            for (var k in this.coleccion[i]) {
              if (Object.prototype.hasOwnProperty.call(this.coleccion[i], k)) {
                copia[k] = this.coleccion[i][k];
              }
            }
            copia.status = status;
            this.coleccion[i] = copia;
            break;
          }
        }
      } else {
        // Si nos quitan el estado, lo sacamos de la coleccion entera.
        var nueva = [];
        for (var j = 0; j < this.coleccion.length; j++) {
          if (this.coleccion[j].game.id !== gameId) {
            nueva.push(this.coleccion[j]);
          }
        }
        this.coleccion = nueva;
      }
    },

    // Pide al backend la coleccion completa (con datos del juego para
    // pintar la imagen y el nombre en la lista).
    async cargarColeccion() {
      this.coleccionLoading = true;
      try {
        var data = await listarEstadosDeJuegoCompletos();
        this.coleccion = data.statuses;
      } catch (error) {
        this.coleccion = [];
      } finally {
        this.coleccionLoading = false;
      }
    },

    // Pide al backend la lista de favoritos del usuario.
    async cargarFavoritos() {
      this.favoritosLoading = true;
      try {
        var data = await obtenerListaDeFavoritos();
        if (data && data.favorites) {
          this.favoritos = data.favorites;
        } else {
          this.favoritos = [];
        }
      } catch (error) {
        console.error('Error al cargar favoritos:', error);
        this.favoritos = [];
      } finally {
        this.favoritosLoading = false;
      }
    },

    // Toggle de favorito desde la lista de la coleccion (cada item de la
    // coleccion tiene su propio botoncito de corazon).
    async alternarFavoritoColeccion(gameId) {

      if (this.favLoadingId === gameId) {
        return;
      }
      this.favLoadingId = gameId;

      try {
        if (this.favoritosIds.has(gameId)) {
          await quitarDeFavoritos(gameId);

          var nuevaLista = [];
          for (var i = 0; i < this.favoritos.length; i++) {
            if (this.favoritos[i].id !== gameId) {
              nuevaLista.push(this.favoritos[i]);
            }
          }
          this.favoritos = nuevaLista;

          if (this.paginaFavoritos > this.totalPaginasFavoritos) {
            this.paginaFavoritos = this.totalPaginasFavoritos;
          }

          notificaciones.success("Game removed from your favorites.", { title: "Favorite removed" });

        } else {
          await agregarAFavoritos(gameId);

          // Recuperamos los datos del juego desde la coleccion para
          // pintarlo en favoritos sin pedir otra vez al backend.
          var datosJuego = null;
          for (var j = 0; j < this.coleccion.length; j++) {
            if (this.coleccion[j].game.id === gameId) {
              datosJuego = this.coleccion[j].game;
              break;
            }
          }
          if (datosJuego) {
            this.favoritos.push(datosJuego);
          }

          notificaciones.success("Game added to your favorites.", { title: "Favorite added" });
        }
      } catch (error) {
        console.error('Error al alternar favorito:', error);
        notificaciones.error("We couldn't update favorites.", { title: "Error" });
      } finally {
        this.favLoadingId = null;
      }
    },

    // Quita un favorito desde la card de la seccion "My Favorites".
    async quitarFavorito(idGame) {
      this.remover = idGame;
      try {
        await quitarDeFavoritos(idGame);

        var nuevaLista = [];
        for (var i = 0; i < this.favoritos.length; i++) {
          if (this.favoritos[i].id !== idGame) {
            nuevaLista.push(this.favoritos[i]);
          }
        }
        this.favoritos = nuevaLista;

        if (this.paginaFavoritos > this.totalPaginasFavoritos) {
          this.paginaFavoritos = this.totalPaginasFavoritos;
        }

        notificaciones.success("Game removed from your favorites.", { title: "Favorite removed" });

      } catch (error) {
        console.error("Error al quitar favorito:", error);
        notificaciones.error("We couldn't remove the game from favorites.", {
          title: "Favorites error"
        });
      } finally {
        this.remover = null;
      }
    },

    irADetalle(gameId) {
      this.router.push('/game/' + gameId);
    },

    irAPanelAdmin() {
      this.router.push('/admin/users');
    },

    irAModeracion() {
      this.router.push('/admin/comments');
    },

    // Abre el modal de cambio de contrasena. Resetea el formulario para
    // que no queden datos de aperturas anteriores.
    abrirModalCambiarContraseña() {
      this.mostrarMenuEditar = false;
      this.mostrarModalCambiarContraseña = true;
      this.errorCambiarContraseña = '';
      this.formularioCambiarContraseña = {
        actual: '',
        nueva: '',
        confirmar: ''
      };
    },

    cerrarModalCambiarContraseña() {
      this.mostrarModalCambiarContraseña = false;
      this.formularioCambiarContraseña = {
        actual: '',
        nueva: '',
        confirmar: ''
      };
      this.errorCambiarContraseña = '';
    },

    // Si se hace click fuera del menu desplegable de edicion, lo cerramos.
    manejarClicFueraDelMenu(e) {
      var menuRef = this.$refs.menuEditarRef;
      if (menuRef && !menuRef.contains(e.target)) {
        this.mostrarMenuEditar = false;
      }
    },

    // Valida el formulario de cambio de contrasena y, si todo va bien,
    // manda la nueva al backend.
    async guardarCambioContraseña() {

      var actual = this.formularioCambiarContraseña.actual;
      var nueva = this.formularioCambiarContraseña.nueva;
      var confirmar = this.formularioCambiarContraseña.confirmar;

      if (!actual || !nueva || !confirmar) {
        this.errorCambiarContraseña = 'All fields are required.';
        return;
      }

      if (nueva.length < 8) {
        this.errorCambiarContraseña = 'New password must be at least 8 characters.';
        return;
      }

      if (nueva !== confirmar) {
        this.errorCambiarContraseña = 'Passwords do not match.';
        return;
      }

      this.cambiandoContraseña = true;
      this.errorCambiarContraseña = '';

      try {
        await cambiarContrasena(actual, nueva);
        this.cerrarModalCambiarContraseña();
        notificaciones.success("Your password has been updated successfully.", {
          title: "Password changed"
        });

      } catch (error) {
        console.error('Error al cambiar contrasena:', error);

        var mensaje = "We couldn't change your password.";
        if (error.response && error.response.data && error.response.data.message) {
          mensaje = error.response.data.message;
        }
        this.errorCambiarContraseña = mensaje;

      } finally {
        this.cambiandoContraseña = false;
      }
    }
  }
};
