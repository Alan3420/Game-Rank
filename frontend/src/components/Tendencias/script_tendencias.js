import { obtenerTendencias } from '../../services/tendencias';
import { listarEstadosDeJuego } from '../../services/user_game_status.js';
import { STATUS_META } from '../../utils/statusMeta.js';
import { claseMetacritic } from '../../utils/metacritic.js';

// Orden del selector; el slug es lo que va en la URL (?board=)
const SECCIONES = [
  {
    key: 'mas_coleccion',
    slug: 'collected',
    titulo: 'Most collected',
    icono: 'pi-bookmark',
    descripcion: 'The games most players have added to their album.',
    nota: 'Players with the game in their album, any status.'
  },
  {
    key: 'mejor_valorados',
    slug: 'rated',
    titulo: 'Top rated',
    icono: 'pi-star',
    descripcion: 'The highest average score in player reviews.',
    nota: 'Average review score out of 5, games with at least 3 reviews.'
  },
  {
    key: 'mas_comentados',
    slug: 'reviewed',
    titulo: 'Most reviewed',
    icono: 'pi-comments',
    descripcion: 'The games players have written the most about.',
    nota: 'Number of written reviews.'
  },
  {
    key: 'mas_favoritos',
    slug: 'favorited',
    titulo: 'Most favorited',
    icono: 'pi-heart',
    descripcion: 'The games players have saved as favorites most often.',
    nota: 'Number of players with the game in favorites.'
  }
];

export default {

  data() {
    return {
      secciones: SECCIONES,
      STATUS_META: STATUS_META,
      tendencias: null,
      estados: {},
      activa: 'mas_coleccion',
      loading: true,
      error: null
    };
  },

  computed: {

    seccionActiva() {
      for (var i = 0; i < this.secciones.length; i++) {
        if (this.secciones[i].key === this.activa) {
          return this.secciones[i];
        }
      }
      return this.secciones[0];
    },

    juegos() {
      if (!this.tendencias || !this.tendencias[this.activa]) {
        return [];
      }
      return this.tendencias[this.activa];
    },

    campeon() {
      return this.juegos[0];
    },

    resto() {
      return this.juegos.slice(1);
    },

    // Puestos con empates (1, 2, 2, 4...): mismo valor, mismo puesto
    puestos() {
      var lista = [];
      for (var i = 0; i < this.juegos.length; i++) {
        if (i > 0 && this.valorDe(this.juegos[i]) === this.valorDe(this.juegos[i - 1])) {
          lista.push(lista[i - 1]);
        } else {
          lista.push(i + 1);
        }
      }
      return lista;
    },

    // Distancia del numero 1 sobre el siguiente
    ventaja() {
      if (this.juegos.length < 2) {
        return 'Only entry';
      }
      var a = Number(this.juegos[0].stat_value) || 0;
      var b = Number(this.juegos[1].stat_value) || 0;
      if (this.puestos[1] === 1) {
        return 'Tied for first';
      }
      var diferencia = this.activa === 'mejor_valorados' ? (a - b).toFixed(1) : Math.round(a - b);
      return '+' + diferencia + ' over No. 2';
    },

    // Maximo del ranking activo para escalar las barras
    maximo() {
      if (this.activa === 'mejor_valorados') {
        return 5;
      }
      var max = 0;
      for (var i = 0; i < this.juegos.length; i++) {
        var v = Number(this.juegos[i].stat_value) || 0;
        if (v > max) {
          max = v;
        }
      }
      return max;
    }
  },

  watch: {
    '$route.query.board': {
      immediate: true,
      handler(slug) {
        for (var i = 0; i < this.secciones.length; i++) {
          if (this.secciones[i].slug === slug) {
            this.activa = this.secciones[i].key;
            return;
          }
        }
        this.activa = this.secciones[0].key;
      }
    }
  },

  async mounted() {
    try {
      var resultados = await Promise.all([
        obtenerTendencias(),
        this.cargarEstados()
      ]);
      this.tendencias = resultados[0];
    } catch (error) {
      console.error('Error cargando tendencias:', error);
      this.error = "Trends didn't load. Reload the page to try again.";
    } finally {
      this.loading = false;
    }
  },

  methods: {

    claseMetacritic(score) {
      return claseMetacritic(score);
    },

    // Estados del jugador: solo para marcar lo que ya tiene
    async cargarEstados() {
      try {
        var data = await listarEstadosDeJuego();
        var mapa = {};
        var lista = (data && data.statuses) ? data.statuses : [];
        for (var i = 0; i < lista.length; i++) {
          mapa[lista[i].id_game_api] = lista[i].status;
        }
        this.estados = mapa;
      } catch (error) {
        this.estados = {};
      }
    },

    resenas(n) {
      return n + (n === 1 ? ' review' : ' reviews');
    },

    estadoDe(id) {
      return this.estados[id] || null;
    },

    elegir(key) {
      var slug = this.secciones[0].slug;
      for (var i = 0; i < this.secciones.length; i++) {
        if (this.secciones[i].key === key) {
          slug = this.secciones[i].slug;
        }
      }
      var query = Object.assign({}, this.$route.query);
      if (slug === this.secciones[0].slug) {
        delete query.board;
      } else {
        query.board = slug;
      }
      this.$router.replace({ query: query });
    },

    // Flechas, Inicio y Fin cambian de ranking y mueven el foco
    moverPestana(e) {
      var claves = this.secciones.map(function (s) { return s.key; });
      var actual = claves.indexOf(this.activa);
      var siguiente = -1;
      if (e.key === 'ArrowRight') {
        siguiente = (actual + 1) % claves.length;
      } else if (e.key === 'ArrowLeft') {
        siguiente = (actual - 1 + claves.length) % claves.length;
      } else if (e.key === 'Home') {
        siguiente = 0;
      } else if (e.key === 'End') {
        siguiente = claves.length - 1;
      }
      if (siguiente === -1) {
        return;
      }
      e.preventDefault();
      this.elegir(claves[siguiente]);
      var slug = this.secciones[siguiente].slug;
      this.$nextTick(function () {
        var tab = document.getElementById('tr-tab-' + slug);
        if (tab) {
          tab.focus();
        }
      });
    },

    valorDe(juego) {
      if (juego.stat_value === null || juego.stat_value === undefined) {
        return '—';
      }
      if (this.activa === 'mejor_valorados') {
        return Number(juego.stat_value).toFixed(1);
      }
      return Math.round(Number(juego.stat_value));
    },

    unidadDe(juego) {
      var n = Math.round(Number(juego.stat_value));
      if (this.activa === 'mejor_valorados') {
        return '/ 5';
      }
      if (this.activa === 'mas_coleccion') {
        return n === 1 ? 'player' : 'players';
      }
      if (this.activa === 'mas_comentados') {
        return n === 1 ? 'review' : 'reviews';
      }
      return n === 1 ? 'favorite' : 'favorites';
    },

    proporcion(juego) {
      if (!this.maximo) {
        return 0;
      }
      var v = Number(juego.stat_value) || 0;
      return Math.max(4, Math.round((v / this.maximo) * 100));
    },

    anioDe(juego) {
      if (!juego.release_date) {
        return '';
      }
      return String(juego.release_date).slice(0, 4);
    }
  }
};
