import { obtenerJuegosDelCatalogo, obtenerVideoDestacado } from '../../services/resume_cards.js';
import { obtenerProximosLanzamientos } from '../../services/clasif_content.js';
import { estadoAutenticacion } from '../../store/autenticacion.js';
import { consultarSiEsFavorito, agregarAFavoritos, quitarDeFavoritos } from '../../services/favorites_area.js';
import { listarEstadosDeJuego } from '../../services/user_game_status.js';
import { notificaciones } from '../../store/notificaciones.js';

// Numero de juegos por pagina en la seccion de proximos lanzamientos.
// Se usa 10 por pagina (a diferencia del catalogo que usa 20) para que
// la seccion no domine la altura del Home.
const POR_PAGINA_PROXIMOS = 10;

// Componente de la pagina principal (Home). Tiene dos modos: cuando no hay
// sesion muestra solo el hero + CTA de registro; cuando hay sesion muestra
// ademas los 3 juegos mejor valorados y la lista de proximos lanzamientos.
export default {
  name: "home",

  data() {
    return {
      topGames: [],
      futureReleases: [],
      // Set para acceso rapido O(1) cuando preguntamos si un juego es favorito.
      favorites: new Set(),
      // Map id_juego -> estado, para pintar el badge de la card.
      statuses: new Map(),
      isLoading: true,
      isFutureLoading: true,
      heroVideo: null,
      // Estado de paginacion de "Upcoming Releases". RAWG no devuelve
      // un total fiable cuando hay muchos resultados, pero usamos count
      // para calcular totalPaginasProximos.
      currentPageProximos: 1,
      totalCountProximos: 0
    };
  },

  async mounted() {

    var token = localStorage.getItem("token");
    var tareas = [];

    // El video del hero se carga siempre, este logueado o no.
    tareas.push(this.cargarVideoDestacado());

    // El resto solo tiene sentido si hay sesion: si no, no podemos
    // pedir favoritos ni estados de coleccion.
    if (token) {
      tareas.push(this.cargarMejoresJuegos());
      tareas.push(this.cargarProximosLanzamientos());
      tareas.push(this.cargarEstadosDeColeccion());
    }

    await Promise.all(tareas);
  },

  methods: {

    // Pide el video destacado al backend. Si no hay video (404) o falla,
    // dejamos heroVideo en null y el template oculta el bloque del video.
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

    // Pide la primera pagina del catalogo, filtra los que tienen nota de
    // Metacritic y se queda con los 3 mejores para mostrarlos como
    // "Top Rated" en la pagina principal.
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

        // Nos quedamos solo con los que tienen nota de Metacritic > 0.
        var juegosConNota = [];
        for (var i = 0; i < juegos.length; i++) {
          if (juegos[i].metacritic && juegos[i].metacritic > 0) {
            juegosConNota.push(juegos[i]);
          }
        }

        // Ordenamos de mayor a menor nota y cogemos los 3 primeros.
        juegosConNota.sort(function (a, b) {
          return b.metacritic - a.metacritic;
        });
        this.topGames = juegosConNota.slice(0, 3);
        this.isLoading = false;

        // Si hay sesion comprobamos cuales son favoritos para pintar
        // el corazon en su estado correcto.
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

    // Pide la primera pagina de proximos lanzamientos al cargar el Home.
    async cargarProximosLanzamientos() {
      await this.cargarPaginaProximos(1);
    },

    // Carga la pagina indicada de la seccion "Upcoming Releases".
    // Replica el patron del catalogo: usa games + count para paginar.
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

        // Si pedimos una pagina mas alla del total, volvemos a la ultima
        // pagina valida para no mostrar lista vacia.
        if (this.totalPaginasProximos > 0 && pagina > this.totalPaginasProximos) {
          await this.cargarPaginaProximos(this.totalPaginasProximos);
          return;
        }

        this.isFutureLoading = false;

        // Hacemos scroll a la seccion para que el usuario vea el cambio
        // de pagina (salvo en la carga inicial, donde estamos en la 1).
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

    // Pide al backend la lista corta de estados (id_juego + status) y los
    // mete en un Map para acceso rapido. Lo usamos solo para pintar el
    // badge de estado en las cards.
    async cargarEstadosDeColeccion() {
      try {
        var data = await listarEstadosDeJuego();
        var mapa = new Map();
        for (var i = 0; i < data.statuses.length; i++) {
          mapa.set(data.statuses[i].id_game_api, data.statuses[i].status);
        }
        this.statuses = mapa;
      } catch (error) {
        // Fallo silencioso: no es critico. Si falla, las cards no muestran
        // el badge de estado pero todo lo demas funciona igual.
      }
    },

    // Se dispara cuando una card cambia de estado (via emit @update:status).
    // Reemplazamos el Map entero para que Vue detecte el cambio y repinte.
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
    },

    // Al cargar la lista de juegos pregunta uno a uno si ya son favoritos
    // del usuario actual. Si lo es, lo metemos en el Set para que la card
    // muestre el corazon lleno.
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

    // Alterna el estado favorito de un juego. Optimista: cambia el Set
    // antes de saber si el backend acepto el cambio, y muestra notificacion.
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

    // Navega a la pagina de detalle del juego.
    irADetalle(gameId) {
      this.$router.push('/game/' + gameId);
    },

    // Devuelve la clase CSS de color para la nota de Metacritic.
    // Verde = 75+, amarillo = 50-74, rojo = menor, gris = sin nota.
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

    // Boton del hero para usuarios no logueados: si por algun motivo ya
    // tienen token guardado los llevamos al catalogo; si no, al login.
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

    // Boton "Upcoming releases" del hero: hace scroll a la seccion
    // correspondiente sin recargar la pagina.
    desplazarALanzamientos() {
      var elemento = document.getElementById('proximos-section');
      if (elemento) {
        elemento.scrollIntoView({ behavior: 'smooth' });
      }
    }
  },

  computed: {
    // Lo exponemos como computed para usarlo dentro del template.
    estadoAutenticacion() {
      return estadoAutenticacion;
    },

    // Total de paginas de proximos lanzamientos a partir del count.
    // Tope de 500 igual que el catalogo porque RAWG corta en esa pagina.
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
