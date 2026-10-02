import { obtenerVideoDestacado } from '../../services/resume_cards.js';
import { obtenerProximosLanzamientos } from '../../services/clasif_content.js';
import { obtenerJuegosFiltrados } from '../../services/catalog_filters.js';
import { obtenerTendencias } from '../../services/tendencias.js';
import { listarEstadosDeJuegoCompletos } from '../../services/user_game_status.js';
import { obtenerEstadisticasUsuario } from '../../services/user_service.js';
import { estadoAutenticacion } from '../../store/autenticacion.js';
import { STATUS_META, STATUS_LIST } from '../../utils/statusMeta.js';
import { claseMetacritic } from '../../utils/metacritic.js';
import { formatearFechaCorta } from '../../utils/formatoFecha.js';

const POR_PAGINA_PROXIMOS = 5;
const CARTAS_POR_PAGINA_ALBUM = 6;

// Secciones de tendencias en el orden en que se muestran las pestanas
const SECCIONES_TENDENCIAS = [
  { key: 'mas_coleccion', label: 'Most collected' },
  { key: 'mejor_valorados', label: 'Top rated' },
  { key: 'mas_comentados', label: 'Most reviewed' },
  { key: 'mas_favoritos', label: 'Most favorited' }
];

// Fecha local en formato AAAA-MM-DD (RAWG filtra por fechas, no por horas)
function fechaISO(fecha) {
  var mes = String(fecha.getMonth() + 1).padStart(2, '0');
  var dia = String(fecha.getDate()).padStart(2, '0');
  return fecha.getFullYear() + '-' + mes + '-' + dia;
}


export default {

  data() {
    return {
      STATUS_META,
      STATUS_LIST,
      SECCIONES_TENDENCIAS,

      // Invitado: trailer del hero
      heroVideo: null,
      heroVideoCargado: false,
      videoPausado: window.matchMedia('(prefers-reduced-motion: reduce)').matches,

      // Album del jugador
      coleccion: [],
      coleccionLoading: true,
      stats: null,
      tabActiva: 'jugando',

      // Pagina derecha
      mejoresAnio: [],
      mejoresLoading: true,
      novedades: [],
      novedadesLoading: true,

      // Parte baja
      tendencias: null,
      tendenciasLoading: true,
      tabTendencia: 'mas_coleccion',
      proximos: [],
      proximosLoading: true,
      paginaProximos: 1,
      totalProximos: 0
    };
  },

  async mounted() {
    if (!estadoAutenticacion.usuario && !localStorage.getItem('token')) {
      this.cargarVideoDestacado();
      return;
    }

    // Todo en paralelo: cada zona tiene su propio skeleton
    this.cargarColeccion();
    this.cargarEstadisticas();
    this.cargarMejoresDelAnio();
    this.cargarNovedadesDelMes();
    this.cargarTendencias();
    this.cargarProximos(1);
  },

  computed: {
    estadoAutenticacion() {
      return estadoAutenticacion;
    },

    nombreJugador() {
      if (estadoAutenticacion.usuario && estadoAutenticacion.usuario.name) {
        return estadoAutenticacion.usuario.name;
      }
      return 'player';
    },

    anioActual() {
      return new Date().getFullYear();
    },

    // id de juego -> estado, para marcar con su color las cartas que el
    // jugador ya tiene en cualquier lista de la Home
    estadoPorJuego() {
      var mapa = {};
      for (var i = 0; i < this.coleccion.length; i++) {
        var item = this.coleccion[i];
        if (item.game && item.game.id) {
          mapa[item.game.id] = item.status;
        }
      }
      return mapa;
    },

    conteoPorEstado() {
      var conteo = { pendiente: 0, jugando: 0, pausado: 0, completado: 0 };
      for (var i = 0; i < this.coleccion.length; i++) {
        var estado = this.coleccion[i].status;
        if (conteo[estado] !== undefined) {
          conteo[estado] += 1;
        }
      }
      return conteo;
    },

    cartasDeLaPestana() {
      var resultado = [];
      for (var i = 0; i < this.coleccion.length; i++) {
        if (this.coleccion[i].status === this.tabActiva) {
          resultado.push(this.coleccion[i]);
        }
      }
      return resultado;
    },

    cartasVisibles() {
      return this.cartasDeLaPestana.slice(0, CARTAS_POR_PAGINA_ALBUM);
    },

    // Una pagina de archivador son 3x2 fundas: las que no tienen carta se
    // muestran vacias (solo en escritorio, en movil se ocultan por CSS) y
    // la ultima es un bolsillo que lleva al catalogo. La pagina completa
    // iguala la altura de la pagina enfrentada del album.
    hayBolsilloCatalogo() {
      return this.cartasVisibles.length < CARTAS_POR_PAGINA_ALBUM;
    },

    fundasVacias() {
      if (!this.hayBolsilloCatalogo) {
        return 0;
      }
      return CARTAS_POR_PAGINA_ALBUM - this.cartasVisibles.length - 1;
    },

    // Juego del trailer (el backend lo devuelve junto al video); sin el,
    // la demo usa una carta sin datos de ningun juego concreto
    juegoDemo() {
      if (this.heroVideo && this.heroVideo.id) {
        return {
          id: this.heroVideo.id,
          name: this.heroVideo.name,
          metacritic: this.heroVideo.metacritic,
          imge_url: this.heroVideo.imge_url,
          release_date: null
        };
      }
      return { id: null, name: 'Your next game', metacritic: null, imge_url: null, release_date: null };
    },

    juegosTendencia() {
      if (!this.tendencias || !this.tendencias[this.tabTendencia]) {
        return [];
      }
      return this.tendencias[this.tabTendencia].slice(0, 4);
    },

    totalPaginasProximos() {
      if (!this.totalProximos) {
        return 1;
      }
      // RAWG corta en la pagina 500 aunque el count diga mas
      return Math.min(Math.ceil(this.totalProximos / POR_PAGINA_PROXIMOS), 500);
    }
  },

  methods: {
    claseMetacritic,

    formatearFecha(valor) {
      return formatearFechaCorta(valor);
    },

    mesCorto(valor) {
      if (!valor) {
        return 'TBA';
      }
      return new Date(valor + 'T00:00:00').toLocaleString('en', { month: 'short' });
    },

    anioDe(valor) {
      return valor ? Number(valor.split('-')[0]) : null;
    },

    alternarVideo() {
      var video = this.$refs.heroVideoRef;
      this.videoPausado = !this.videoPausado;
      if (!video) {
        return;
      }
      if (this.videoPausado) {
        video.pause();
      } else {
        video.play();
      }
    },

    async cargarVideoDestacado() {
      try {
        this.heroVideo = await obtenerVideoDestacado();
      } catch (error) {
        this.heroVideo = null;
      } finally {
        this.heroVideoCargado = true;
      }
    },

    async cargarColeccion() {
      this.coleccionLoading = true;
      try {
        var data = await listarEstadosDeJuegoCompletos();
        this.coleccion = (data && data.statuses) ? data.statuses : [];

        // La pestana inicial es la primera que tenga cartas, empezando
        // por lo que el jugador esta jugando
        var orden = ['jugando', 'pendiente', 'pausado', 'completado'];
        for (var i = 0; i < orden.length; i++) {
          if (this.conteoPorEstado[orden[i]] > 0) {
            this.tabActiva = orden[i];
            break;
          }
        }
      } catch (error) {
        console.error('Error cargando la coleccion:', error);
        this.coleccion = [];
      } finally {
        this.coleccionLoading = false;
      }
    },

    async cargarEstadisticas() {
      try {
        this.stats = await obtenerEstadisticasUsuario();
      } catch (error) {
        this.stats = null;
      }
    },

    async cargarMejoresDelAnio() {
      this.mejoresLoading = true;
      try {
        var hoy = new Date();
        // RAWG casi no tiene notas de Metacritic de juegos recientes, asi
        // que el ranking del año usa la valoracion de sus jugadores (0-5)
        var datos = await obtenerJuegosFiltrados(1, 10, {
          ordering: '-rating',
          dates: this.anioActual + '-01-01,' + fechaISO(hoy)
        });
        var juegos = (datos && datos.games) ? datos.games : [];
        this.mejoresAnio = juegos.filter(function (j) { return j.rating > 0; }).slice(0, 5);
      } catch (error) {
        console.error('Error cargando lo mejor del año:', error);
        this.mejoresAnio = [];
      } finally {
        this.mejoresLoading = false;
      }
    },

    async cargarNovedadesDelMes() {
      this.novedadesLoading = true;
      try {
        var hoy = new Date();
        var inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
        var datos = await obtenerJuegosFiltrados(1, 5, {
          ordering: '-added',
          dates: fechaISO(inicioMes) + ',' + fechaISO(hoy)
        });
        this.novedades = (datos && datos.games) ? datos.games.slice(0, 5) : [];
      } catch (error) {
        console.error('Error cargando novedades del mes:', error);
        this.novedades = [];
      } finally {
        this.novedadesLoading = false;
      }
    },

    async cargarTendencias() {
      this.tendenciasLoading = true;
      try {
        this.tendencias = await obtenerTendencias();
        // Si la seccion por defecto viene vacia, saltamos a la primera con datos
        if (this.tendencias && (!this.tendencias[this.tabTendencia] || this.tendencias[this.tabTendencia].length === 0)) {
          for (var i = 0; i < SECCIONES_TENDENCIAS.length; i++) {
            var key = SECCIONES_TENDENCIAS[i].key;
            if (this.tendencias[key] && this.tendencias[key].length) {
              this.tabTendencia = key;
              break;
            }
          }
        }
      } catch (error) {
        this.tendencias = null;
      } finally {
        this.tendenciasLoading = false;
      }
    },

    async cargarProximos(pagina) {
      this.proximosLoading = true;
      this.paginaProximos = pagina;
      try {
        var datos = await obtenerProximosLanzamientos(pagina, POR_PAGINA_PROXIMOS);
        this.proximos = (datos && datos.games) ? datos.games : [];
        this.totalProximos = (datos && datos.count) ? datos.count : 0;
      } catch (error) {
        console.error('Error cargando proximos lanzamientos:', error);
        this.proximos = [];
      } finally {
        this.proximosLoading = false;
      }
    },

    // Etiqueta en ingles del dato de cada tendencia (el backend la
    // devuelve en espanol en stat_label, asi que la recomponemos)
    etiquetaTendencia(juego) {
      var valor = juego.stat_value;
      if (valor === null || valor === undefined) {
        return '';
      }
      if (this.tabTendencia === 'mejor_valorados') {
        return Number(valor).toFixed(1) + ' / 5 average';
      }
      var total = Math.round(Number(valor));
      var nombres = {
        mas_coleccion: ['collection', 'collections'],
        mas_comentados: ['review', 'reviews'],
        mas_favoritos: ['favorite', 'favorites']
      };
      var par = nombres[this.tabTendencia] || ['', ''];
      return total + ' ' + (total === 1 ? par[0] : par[1]);
    },

    // Navegacion de pestanas con flechas (patron WAI-ARIA de tabs)
    moverPestana(evento, lista, actual, asignar) {
      // currentTarget deja de existir al terminar el evento: lo guardamos
      var contenedor = evento.currentTarget;
      var indice = lista.indexOf(actual);
      var siguiente = indice;
      if (evento.key === 'ArrowRight') {
        siguiente = (indice + 1) % lista.length;
      } else if (evento.key === 'ArrowLeft') {
        siguiente = (indice - 1 + lista.length) % lista.length;
      } else if (evento.key === 'Home') {
        siguiente = 0;
      } else if (evento.key === 'End') {
        siguiente = lista.length - 1;
      } else {
        return;
      }
      evento.preventDefault();
      asignar(lista[siguiente]);
      this.$nextTick(function () {
        var activo = contenedor.querySelector('[aria-selected="true"]');
        if (activo) {
          activo.focus();
        }
      });
    },

    irARegistro() {
      this.$router.push('/register');
    },

    irALogin() {
      this.$router.push('/login');
    }
  }
};
