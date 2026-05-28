import { estadoAutenticacion } from '../store/autenticacion';
import { notificaciones } from '../store/notificaciones';
import { eliminarMiCuenta } from '../services/user_service';


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

    esAdministrador() {
      if (!estadoAutenticacion.usuario) {
        return false;
      }
      if (estadoAutenticacion.usuario.role === 'admin') {
        return true;
      }
      return false;
    },

    estadoAutenticacion() {
      return estadoAutenticacion;
    }
  },

  methods: {

    cambiarTema() {
      if (this.tema === 'light') {
        this.tema = 'dark';
      } else {
        this.tema = 'light';
      }

      document.documentElement.setAttribute('data-theme', this.tema);
      localStorage.setItem('tema', this.tema);
    },

    enviarBusquedaCabecera() {

      var termino = this.headerSearch.trim();
      var consulta = {};

      if (termino) {
        consulta.q = termino;
      }

      this.$router.push({
        path: '/content/overview',
        query: consulta
      });
    },

    manejarCierreSesion() {
      this.menuAbierto = false;
      estadoAutenticacion.cerrarSesion();
      this.$router.push("/login");
      notificaciones.success("You've signed out successfully.", { title: "Goodbye" });
    },

    irAModeracion() {
      this.menuAbierto = false;
      this.$router.push('/admin/comments');
    },

    abrirConfirmEliminar() {
      this.menuAbierto = false;
      this.confirmTexto = '';
      this.confirmEliminarAbierto = true;
    },

    cerrarConfirmEliminar() {
      if (this.eliminandoCuenta) {
        return;
      }
      this.confirmEliminarAbierto = false;
      this.confirmTexto = '';
    },

    async confirmarEliminarCuenta() {

      if (this.confirmTexto !== 'DELETE' || this.eliminandoCuenta) {
        return;
      }

      this.eliminandoCuenta = true;

      try {

        await eliminarMiCuenta();

        this.confirmEliminarAbierto = false;
        estadoAutenticacion.cerrarSesion();
        this.$router.push("/login");

        notificaciones.success("Your account has been permanently deleted.", {
          title: "Account deleted"
        });

      } catch (error) {

        console.error('Error al eliminar la cuenta:', error);

        var mensaje = "We couldn't delete your account. Please try again.";
        if (error.response && error.response.data && error.response.data.message) {
          mensaje = error.response.data.message;
        }

        notificaciones.error(mensaje, { title: "Error" });

      } finally {
        this.eliminandoCuenta = false;
      }
    },

    manejarClicFuera(e) {
      if (this.$refs.userMenuRef && !this.$refs.userMenuRef.contains(e.target)) {
        this.menuAbierto = false;
      }
    }
  },

  watch: {

    '$route.query.q'(valor) {
      if (valor) {
        this.headerSearch = valor;
      } else {
        this.headerSearch = '';
      }
    }
  },

  mounted() {

    // Aplicamos el tema enseguida para no tener un flashazo de tema claro
    // si el usuario tenia el oscuro guardado
    document.documentElement.setAttribute('data-theme', this.tema);

    document.addEventListener('mousedown', this.manejarClicFuera);

    estadoAutenticacion.restaurarSesion();

    // Si en una peticion anterior guardamos un aviso flash (por ejemplo
    // "sesion expirada" tras un 401) lo recogemos y lo mostramos ahora
    var flash = localStorage.getItem('flashNotificacion');
    if (flash) {
      localStorage.removeItem('flashNotificacion');

      try {
        var datos = JSON.parse(flash);
        var fn = null;
        if (datos.type === 'success') {
          fn = notificaciones.success;
        } else {
          fn = notificaciones.error;
        }
        fn(datos.message, { title: datos.title });
      } catch (error) {
      }
    }
  },

  unmounted() {
    document.removeEventListener('mousedown', this.manejarClicFuera);
  }
};
