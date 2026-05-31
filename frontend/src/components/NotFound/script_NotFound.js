import { useRouter, useRoute } from 'vue-router';

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
