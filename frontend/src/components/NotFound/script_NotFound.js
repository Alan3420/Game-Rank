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
    volver() {
      if (window.history.length > 1) {
        this.router.go(-1);
      } else {
        this.router.push('/');
      }
    }
  }
};
