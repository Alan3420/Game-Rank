import { obtenerTendencias } from '../../services/tendencias';

// Componente de la pagina Tendencias. Pide al backend cuatro listas de
// juegos (mas favoritos, mejor valorados, mas comentados, mas coleccionados)
// y las pinta en secciones separadas con scroll horizontal entre cards.
export default {

  data() {
    return {
      tendencias: null,
      loading: true,
      error: null
    };
  },

  computed: {

    // Devuelve la lista de secciones de la pagina. Cada seccion tiene
    // una "key" que coincide con la propiedad del objeto que devuelve el
    // backend, y un titulo / subtitulo / icono que se muestran en el header
    // de cada bloque.
    //
    // Las claves estan en espanol porque asi llegan del backend; los
    // textos visibles estan en ingles porque la UI esta en ingles.
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

    // Lleva la pagina hasta la seccion indicada con scroll suave.
    // Lo usan los botones del menu superior que sirven de "tabs".
    desplazarASeccion(key) {
      var el = document.getElementById(key);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },

    // Devuelve la clase CSS que pintara el badge de metacritic segun la nota.
    // Verde = 80 o mas, amarillo = 50-79, rojo = menos de 50.
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

    // Construye la etiqueta de cada card en ingles a partir del valor
    // numerico que devuelve el backend. Asi no dependemos del texto
    // ya traducido que manda el servidor (que viene en espanol).
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

    // Navega al detalle del juego al hacer click en una card.
    irAJuego(id) {
      this.$router.push('/game/' + id);
    }
  }
};
