import { estadoAutenticacion } from '../store/autenticacion';
import { notificaciones } from '../store/notificaciones';
import { deleteOwnAccount } from '../services/user_service';

export default {

  data() {
    return {
      headerSearch: '',
      menuAbierto: false,
      tema: localStorage.getItem('tema') || 'light',
      confirmEliminarAbierto: false,
      confirmTexto: '',
      eliminandoCuenta: false
    };

  },

  computed: {

    isAdmin() {
      return estadoAutenticacion.usuario?.role === 'admin';
    },

    estadoAutenticacion() {
      return estadoAutenticacion;
    }
  },

  methods: {

    toggleTema() {
      this.tema = this.tema === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', this.tema);
      localStorage.setItem('tema', this.tema);
    },


    submitHeaderSearch() {
      const term = this.headerSearch.trim();
      this.$router.push({ path: '/content/overview', query: term ? { q: term } : {} });
    },


    manejarCierreSesion() {
      this.menuAbierto = false;
      estadoAutenticacion.cerrarSesion();
      this.$router.push("/login");
      notificaciones.success("Has cerrado sesión correctamente.", { title: "Hasta luego" });
    },


    irAConfigAdmin() {
      this.menuAbierto = false;
      notificaciones.info("Panel de configuración en desarrollo.", { title: "Próximamente" });
    },


    abrirConfirmEliminar() {
      this.menuAbierto = false;
      this.confirmTexto = '';
      this.confirmEliminarAbierto = true;
    },


    cerrarConfirmEliminar() {
      if (this.eliminandoCuenta) return;
      this.confirmEliminarAbierto = false;
      this.confirmTexto = '';
    },


    async confirmarEliminarCuenta() {

      if (this.confirmTexto !== 'ELIMINAR' || this.eliminandoCuenta) return;
      this.eliminandoCuenta = true;

      try {

        await deleteOwnAccount();

        this.confirmEliminarAbierto = false;
        estadoAutenticacion.cerrarSesion();

        this.$router.push("/login");
        notificaciones.success("Tu cuenta ha sido eliminada permanentemente.", { title: "Cuenta eliminada" });

      } catch (error) {

        console.error('Error al eliminar la cuenta:', error);
        notificaciones.error(
          error.response?.data?.message || "No pudimos eliminar tu cuenta. Inténtalo de nuevo.",
          { title: "Error" }
        );
      } finally {
        this.eliminandoCuenta = false;
      }
    },


    handleClickOutside(e) {
      if (this.$refs.userMenuRef && !this.$refs.userMenuRef.contains(e.target)) {
        this.menuAbierto = false;
      }
    }

  },


  watch: {
    '$route.query.q'(val) {
      this.headerSearch = val || '';
    }
  },

  mounted() {

    document.documentElement.setAttribute('data-theme', this.tema);
    document.addEventListener('mousedown', this.handleClickOutside);

    estadoAutenticacion.restaurarSesion();

    const flash = localStorage.getItem('flashNotificacion');

    if (flash) {
      localStorage.removeItem('flashNotificacion');

      try {
        const { type, title, message } = JSON.parse(flash);
        const fn = type === 'success' ? notificaciones.success : notificaciones.error;
        fn(message, { title });
      } catch { }
    }
  },
  
  unmounted() {
    document.removeEventListener('mousedown', this.handleClickOutside);
  }
};
