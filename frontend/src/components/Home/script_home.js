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
import { obtenerListaDeFavoritos, agregarAFavoritos } from '../../services/favorites_area.js';
import { notificaciones } from '../../store/notificaciones.js';

const POR_PAGINA_PROXIMOS = 5;
const CARTAS_DESCUBRIR = 7;

// Pestanas de Descubrir: orden de RAWG con el que se pide cada lista
const PESTANAS_DESCUBRIR = [
  { key: 'popular', label: 'Popular', ordering: '-added' },
  { key: 'aclamados', label: 'Acclaimed', ordering: '-metacritic' }
];

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
      PESTANAS_DESCUBRIR,

      // Invitado: trailer del hero
      heroVideo: null,
      heroVideoCargado: false,
      videoPausado: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      // Invitado: estado elegido en la prueba (ninguno al principio)
      estadoDemo: null,

      // Album del jugador (resumen)
      coleccion: [],
      coleccionLoading: true,
      stats: null,
      favoritosIds: [],
      propiosCargados: false,

      // Descubrir: juegos que el jugador aun no tiene
      descubrir: [],
      descubrirLoading: true,
      tabDescubrir: 'popular',
      paginaDescubrir: 1,
      anadiendoId: null,
      // los que anade aqui se quedan visibles (con el corazon lleno)
      anadidosAqui: [],

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
    this.cargarPropiosYDescubrir();
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

    // ids que el jugador ya tiene (coleccion o favoritos)
    idsPropios() {
      var ids = new Set(this.favoritosIds);
      for (var i = 0; i < this.coleccion.length; i++) {
        if (this.coleccion[i].game) {
          ids.add(this.coleccion[i].game.id);
        }
      }
      return ids;
    },

    destacado() {
      return this.descubrir.length ? this.descubrir[0] : null;
    },

    restoDescubrir() {
      return this.descubrir.slice(1, CARTAS_DESCUBRIR);
    },

    // Resumen del album: lo que esta jugando y, si no hay, lo pendiente
    siguienteDelAlbum() {
      var orden = [['jugando', 'Continue playing'], ['pendiente', 'Up next'], ['pausado', 'Paused for now']];
      for (var i = 0; i < orden.length; i++) {
        var lista = [];
        for (var j = 0; j < this.coleccion.length; j++) {
          if (this.coleccion[j].status === orden[i][0]) {
            lista.push(this.coleccion[j]);
          }
        }
        if (lista.length) {
          return { titulo: orden[i][1], items: lista.slice(0, 3) };
        }
      }
      return { titulo: 'Continue playing', items: [] };
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
          release_date: this.heroVideo.release_date || null
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

    // "Oct 6", con el año solo si no es el actual
    fechaLanzamiento(valor) {
      if (!valor) {
        return 'TBA';
      }
      var dia = Number(valor.split('-')[2]);
      var texto = this.mesCorto(valor) + ' ' + dia;
      if (this.anioDe(valor) !== this.anioActual) {
        texto += ', ' + this.anioDe(valor);
      }
      return texto;
    },

    // Cuenta atras hasta la salida: Today, Tomorrow, In n days
    cuentaAtras(valor) {
      if (!valor) {
        return '';
      }
      var hoy = new Date();
      hoy.setHours(0, 0, 0, 0);
      var salida = new Date(valor + 'T00:00:00');
      var dias = Math.round((salida - hoy) / 86400000);
      if (dias < 0) {
        return '';
      }
      if (dias === 0) {
        return 'Today';
      }
      if (dias === 1) {
        return 'Tomorrow';
      }
      return 'In ' + dias + ' days';
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
      } catch (error) {
        console.error('Error cargando la coleccion:', error);
        this.coleccion = [];
      } finally {
        this.coleccionLoading = false;
      }
    },

    async cargarFavoritos() {
      try {
        var data = await obtenerListaDeFavoritos();
        var ids = [];
        var lista = (data && data.favorites) ? data.favorites : [];
        for (var i = 0; i < lista.length; i++) {
          ids.push(lista[i].id);
        }
        this.favoritosIds = ids;
      } catch (error) {
        this.favoritosIds = [];
      }
    },

    // Descubrir necesita saber antes que tiene el jugador para excluirlo
    async cargarPropiosYDescubrir() {
      await Promise.all([this.cargarColeccion(), this.cargarFavoritos()]);
      this.propiosCargados = true;
      this.cargarDescubrir(1);
    },

    async cargarDescubrir(pagina) {
      this.descubrirLoading = true;
      this.paginaDescubrir = pagina;
      var pestana = PESTANAS_DESCUBRIR[0];
      for (var i = 0; i < PESTANAS_DESCUBRIR.length; i++) {
        if (PESTANAS_DESCUBRIR[i].key === this.tabDescubrir) {
          pestana = PESTANAS_DESCUBRIR[i];
        }
      }
      try {
        var datos = await obtenerJuegosFiltrados(pagina, 20, { ordering: pestana.ordering });
        var juegos = (datos && datos.games) ? datos.games : [];
        var propios = this.idsPropios;
        var anadidos = this.anadidosAqui;
        // fuera lo que ya tiene (salvo lo que acaba de anadir aqui) y lo
        // que no tiene imagen
        this.descubrir = juegos.filter(function (j) {
          return j.imge_url && (!propios.has(j.id) || anadidos.indexOf(j.id) !== -1);
        }).slice(0, CARTAS_DESCUBRIR);
      } catch (error) {
        console.error('Error cargando descubrir:', error);
        this.descubrir = [];
      } finally {
        this.descubrirLoading = false;
      }
    },

    elegirDescubrir(key) {
      if (this.tabDescubrir === key) {
        return;
      }
      this.tabDescubrir = key;
      this.anadidosAqui = [];
      this.cargarDescubrir(1);
    },

    masDescubrir() {
      this.anadidosAqui = [];
      this.cargarDescubrir(this.paginaDescubrir + 1);
    },

    esFavorito(id) {
      return this.favoritosIds.indexOf(id) !== -1;
    },

    async anadirAFavoritos(id) {
      if (this.esFavorito(id) || this.anadiendoId) {
        return;
      }
      this.anadiendoId = id;
      var resultado = await agregarAFavoritos(id);
      this.anadiendoId = null;
      if (!resultado) {
        notificaciones.error("Game wasn't added. Check your connection and try again.", { title: 'Favorites error' });
        return;
      }
      this.favoritosIds = this.favoritosIds.concat([id]);
      this.anadidosAqui = this.anadidosAqui.concat([id]);
      notificaciones.success('Added to your favorites. Set its status from the game page.', { title: 'Favorite added' });
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
