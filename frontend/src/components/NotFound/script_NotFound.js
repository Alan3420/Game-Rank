import { useRouter, useRoute } from 'vue-router';

// Logica de la pantalla 404. Solo necesita guardar una referencia al router
// para poder llevar al usuario a otra pagina, y la ruta que pidio (para
// mostrarla en pantalla y que entienda que esa URL no existe).
export default {
  name: 'NotFound',

  data() {
    return {
      router: null,
      ruta: ''
    };
  },

  mounted() {
    this.router = useRouter();
    this.ruta = useRoute().path;
  },

  methods: {

    // Boton "Go home": lleva al inicio sin importar desde donde se vino.
    irAlInicio() {
      this.router.push('/');
    },

    // Boton "Go back": intenta volver atras en el historial del navegador.
    // Si la pestana se abrio directamente en la URL 404 no hay historial
    // al que volver, asi que en ese caso lo llevamos al inicio igualmente.
    volver() {
      if (window.history.length > 1) {
        this.router.go(-1);
      } else {
        this.router.push('/');
      }
    }
  }
};
