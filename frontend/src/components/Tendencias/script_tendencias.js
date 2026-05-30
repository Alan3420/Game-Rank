import { obtenerTendencias } from '../../services/tendencias';

export default {

  data() {
    return {
      tendencias: null,
      loading: true,
      error: null
    };
  },

  computed: {

    secciones() {
      return [
        {
          key: 'mas_favoritos',
          titulo: 'Most Favorited',
          subtitulo: 'Games with the most likes from the community',
          icono: 'pi-heart-fill',
          label: 'Favorited'
        },
        {
          key: 'mejor_valorados',
          titulo: 'Top Rated',
          subtitulo: 'The highest rated titles by the community',
          icono: 'pi-star-fill',
          label: 'Rated'
        },
        {
          key: 'mas_comentados',
          titulo: 'Most Commented',
          subtitulo: 'Games with the most discussion and reviews',
          icono: 'pi-comments',
          label: 'Commented'
        },
        {
          key: 'mas_coleccion',
          titulo: 'Most Collected',
          subtitulo: 'Titles most added to user collections',
          icono: 'pi-bookmark-fill',
          label: 'Collection'
        }
      ];
    }
  },

  async mounted() {
    try {
      this.tendencias = await obtenerTendencias();
    } catch (error) {
      console.error('Error cargando tendencias:', error);
      this.error = "We couldn't load the trends. Please try again later.";
    } finally {
      this.loading = false;
    }
  },

  methods: {

    desplazarASeccion(key) {
      var el = document.getElementById(key);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },

    claseMetacritic(score) {
      if (!score) {
        return 'mc-na';
      }
      if (score >= 80) {
        return 'mc-green';
      }
      if (score >= 50) {
        return 'mc-yellow';
      }
      return 'mc-red';
    },

    formatearEtiquetaTendencia(seccionKey, valor) {

      if (valor === null || valor === undefined) {
        return '';
      }

      if (seccionKey === 'mejor_valorados') {
        var promedio = Number(valor).toFixed(1);
        return promedio + ' / 5 ★';
      }

      var total = Math.round(Number(valor));

      if (seccionKey === 'mas_favoritos') {
        if (total === 1) {
          return total + ' favorite';
        }
        return total + ' favorites';
      }

      if (seccionKey === 'mas_comentados') {
        if (total === 1) {
          return total + ' review';
        }
        return total + ' reviews';
      }

      if (seccionKey === 'mas_coleccion') {
        if (total === 1) {
          return total + ' user';
        }
        return total + ' users';
      }

      return '';
    },

    irAJuego(id) {
      this.$router.push('/game/' + id);
    }
  }
};
