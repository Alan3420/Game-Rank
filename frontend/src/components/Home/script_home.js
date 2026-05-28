import { obtenerJuegosDelCatalogo, obtenerVideoDestacado } from '../../services/resume_cards.js';
import { obtenerProximosLanzamientos } from '../../services/clasif_content.js';
import { estadoAutenticacion } from '../../store/autenticacion.js';
import { consultarSiEsFavorito, agregarAFavoritos, quitarDeFavoritos } from '../../services/favorites_area.js';
import { listarEstadosDeJuego } from '../../services/user_game_status.js';
import { notificaciones } from '../../store/notificaciones.js';

const POR_PAGINA_PROXIMOS = 10;


export default {
  name: "home",

  data() {
    return {
      topGames: [],
      futureReleases: [],
      favorites: new Set(),
      statuses: new Map(),
      isLoading: true,
      isFutureLoading: true,
      heroVideo: null,
      currentPageProximos: 1,
      totalCountProximos: 0
    };
  },

  async mounted() {

    var token = localStorage.getItem("token");
    var tareas = [];

    tareas.push(this.cargarVideoDestacado());

    // Sin sesion no tiene sentido pedir favoritos ni estados de coleccion
    if (token) {
      tareas.push(this.cargarMejoresJuegos());
      tareas.push(this.cargarProximosLanzamientos());
      tareas.push(this.cargarEstadosDeColeccion());
    }

    await Promise.all(tareas);
  },

  methods: {

    async cargarVideoDestacado() {
      try {
        var video = await obtenerVideoDestacado();
        if (video) {
          this.heroVideo = video;
        } else {
          this.heroVideo = null;
        }
      } catch (error) {
        console.error('Error al cargar video del hero:', error);
        this.heroVideo = null;
      }
    },

    async cargarMejoresJuegos() {

      this.isLoading = true;

      try {
        var respuesta = await obtenerJuegosDelCatalogo(1);

        var juegos = [];
        if (respuesta && respuesta.games && Array.isArray(respuesta.games)) {
          juegos = respuesta.games;
        } else if (Array.isArray(respuesta)) {
          juegos = respuesta;
        }

        var juegosConNota = [];
        for (var i = 0; i < juegos.length; i++) {
          if (juegos[i].metacritic && juegos[i].metacritic > 0) {
            juegosConNota.push(juegos[i]);
          }
        }

        juegosConNota.sort(function (a, b) {
          return b.metacritic - a.metacritic;
        });
        this.topGames = juegosConNota.slice(0, 3);
        this.isLoading = false;

        if (estadoAutenticacion.usuario) {
          var tareas = [];
          for (var j = 0; j < this.topGames.length; j++) {
            tareas.push(this.comprobarFavoritoInicial(this.topGames[j].id));
          }
          await Promise.all(tareas);
        }

      } catch (error) {
        console.error('Error cargando mejores juegos:', error);
        this.isLoading = false;
      }
    },

    async cargarProximosLanzamientos() {
      await this.cargarPaginaProximos(1);
    },

    async cargarPaginaProximos(pagina) {

      this.isFutureLoading = true;
      this.currentPageProximos = pagina;

      try {
        var respuesta = await obtenerProximosLanzamientos(pagina, POR_PAGINA_PROXIMOS);

        if (respuesta && respuesta.games) {
          this.futureReleases = respuesta.games;
        } else {
          this.futureReleases = [];
        }

        if (respuesta && respuesta.count) {
          this.totalCountProximos = respuesta.count;
        } else {
          this.totalCountProximos = 0;
        }

        // Si pedimos una pagina mas alla del total volvemos a la ultima
        // valida para no dejar la lista en blanco
        if (this.totalPaginasProximos > 0 && pagina > this.totalPaginasProximos) {
          await this.cargarPaginaProximos(this.totalPaginasProximos);
          return;
        }

        this.isFutureLoading = false;

        if (pagina > 1) {
          var elemento = document.getElementById('proximos-section');
          if (elemento) {
            elemento.scrollIntoView({ behavior: 'smooth' });
          }
        }

        if (estadoAutenticacion.usuario) {
          var tareas = [];
          for (var i = 0; i < this.futureReleases.length; i++) {
            tareas.push(this.comprobarFavoritoInicial(this.futureReleases[i].id));
          }
          await Promise.all(tareas);
        }

      } catch (error) {
        console.error('Error cargando proximos lanzamientos:', error);
        this.futureReleases = [];
        this.isFutureLoading = false;
      }
    },

    async cargarEstadosDeColeccion() {
      try {
        var data = await listarEstadosDeJuego();
        var mapa = new Map();
        for (var i = 0; i < data.statuses.length; i++) {
          mapa.set(data.statuses[i].id_game_api, data.statuses[i].status);
        }
        this.statuses = mapa;
      } catch (error) {
      }
    },

    manejarActualizacionEstado(datos) {
      var gameId = datos.gameId;
      var status = datos.status;

      // Reemplazamos el Map entero para que Vue se entere del cambio
      var mapa = new Map(this.statuses);
      if (status) {
        mapa.set(gameId, status);
      } else {
        mapa.delete(gameId);
      }
      this.statuses = mapa;
    },

    async comprobarFavoritoInicial(gameId) {
      try {
        var data = await consultarSiEsFavorito(gameId);
        if (data.is_favorite) {
          this.favorites.add(gameId);
        }
      } catch (error) {
        console.error('Error verificando favorito ' + gameId + ':', error);
      }
    },

    async alternarFavorito(gameId) {

      var eraFavorito = this.favorites.has(gameId);

      try {
        if (eraFavorito) {
          await quitarDeFavoritos(gameId);
          this.favorites.delete(gameId);
          notificaciones.success("Game removed from your favorites.", { title: "Favorite removed" });
        } else {
          await agregarAFavoritos(gameId);
          this.favorites.add(gameId);
          notificaciones.success("Game added to your favorites.", { title: "Favorite added" });
        }
      } catch (error) {
        console.error('Error al cambiar favorito:', error);

        var mensaje = "We couldn't add the game to favorites.";
        if (eraFavorito) {
          mensaje = "We couldn't remove the game from favorites.";
        }
        notificaciones.error(mensaje, { title: "Favorites error" });
      }
    },

    irADetalle(gameId) {
      this.$router.push('/game/' + gameId);
    },

    claseColorMetacritic(score) {
      if (!score) {
        return 'rank-score--none';
      }
      if (score >= 75) {
        return 'rank-score--green';
      }
      if (score >= 50) {
        return 'rank-score--yellow';
      }
      return 'rank-score--red';
    },

    irALogin() {
      var token = localStorage.getItem("token");
      if (token) {
        this.$router.push('/content/overview');
      } else {
        this.$router.push('/login');
      }
    },

    irARegistro() {
      this.$router.push("/register");
    },

    irAExplorar() {
      this.$router.push('/content/overview');
    },

    desplazarALanzamientos() {
      var elemento = document.getElementById('proximos-section');
      if (elemento) {
        elemento.scrollIntoView({ behavior: 'smooth' });
      }
    }
  },

  computed: {
    estadoAutenticacion() {
      return estadoAutenticacion;
    },

    // Tope de 500 paginas porque RAWG corta a partir de ahi aunque el
    // count diga mas
    totalPaginasProximos() {
      if (!this.totalCountProximos) {
        return 0;
      }
      var calculado = Math.ceil(this.totalCountProximos / POR_PAGINA_PROXIMOS);
      if (calculado > 500) {
        return 500;
      }
      return calculado;
    }
  }
};
