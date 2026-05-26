import { estadoAutenticacion } from '../store/autenticacion';
import { notificaciones } from '../store/notificaciones';
import { eliminarMiCuenta } from '../services/user_service';

// Logica del componente raiz App.vue. Se encarga del header (busqueda,
// boton de tema, menu de usuario), del footer y del modal de confirmacion
// para borrar la cuenta. Al montarse, intenta restaurar la sesion del
// usuario a partir del token guardado en localStorage.
export default {

  data() {
    return {
      headerSearch: '',
      menuAbierto: false,
      // Tema guardado en localStorage. Si no hay nada guardado arrancamos
      // en modo claro porque es lo mas comun.
      tema: localStorage.getItem('tema') || 'light',
      confirmEliminarAbierto: false,
      confirmTexto: '',
      eliminandoCuenta: false
    };
  },

  computed: {

    // Devuelve true si el usuario logueado tiene rol admin. Se usa para
    // mostrar/ocultar opciones del menu como "Manage Users" y "Moderation".
    esAdministrador() {
      if (!estadoAutenticacion.usuario) {
        return false;
      }
      if (estadoAutenticacion.usuario.role === 'admin') {
        return true;
      }
      return false;
    },

    // Lo exponemos como computed para poder usar "estadoAutenticacion.x"
    // dentro del template del App.vue.
    estadoAutenticacion() {
      return estadoAutenticacion;
    }
  },

  methods: {

    // Alterna entre tema claro y oscuro, lo persiste en localStorage y
    // aplica el atributo data-theme al elemento raiz del HTML para que
    // las variables CSS cambien.
    cambiarTema() {
      if (this.tema === 'light') {
        this.tema = 'dark';
      } else {
        this.tema = 'light';
      }

      document.documentElement.setAttribute('data-theme', this.tema);
      localStorage.setItem('tema', this.tema);
    },

    // Se dispara con Enter en el input del header. Si hay texto navega al
    // catalogo con la query "q", si no, navega al catalogo sin filtros.
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

    // Cierra sesion, redirige al login y muestra notificacion de despedida.
    manejarCierreSesion() {
      this.menuAbierto = false;
      estadoAutenticacion.cerrarSesion();
      this.$router.push("/login");
      notificaciones.success("You've signed out successfully.", { title: "Goodbye" });
    },

    // Acceso directo a la pagina de moderacion desde el dropdown del menu.
    irAModeracion() {
      this.menuAbierto = false;
      this.$router.push('/admin/comments');
    },

    // Abre el modal que pide confirmar la eliminacion definitiva de la cuenta.
    abrirConfirmEliminar() {
      this.menuAbierto = false;
      this.confirmTexto = '';
      this.confirmEliminarAbierto = true;
    },

    // Cierra el modal. Si estamos en mitad de la peticion lo bloqueamos
    // para evitar que el usuario lo cierre por error.
    cerrarConfirmEliminar() {
      if (this.eliminandoCuenta) {
        return;
      }
      this.confirmEliminarAbierto = false;
      this.confirmTexto = '';
    },

    // Llama al backend para borrar la cuenta. Solo se ejecuta si el usuario
    // ha escrito exactamente "DELETE" en el input de confirmacion.
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

    // Cierra el menu desplegable del usuario cuando se hace click fuera de el.
    // Lo registramos como listener global del documento en mounted().
    manejarClicFuera(e) {
      if (this.$refs.userMenuRef && !this.$refs.userMenuRef.contains(e.target)) {
        this.menuAbierto = false;
      }
    }
  },

  watch: {

    // Cuando el usuario navega al catalogo desde otra parte y la URL tiene
    // ?q=algo, sincronizamos el input del header con ese valor para que
    // refleje la busqueda activa.
    '$route.query.q'(valor) {
      if (valor) {
        this.headerSearch = valor;
      } else {
        this.headerSearch = '';
      }
    }
  },

  mounted() {

    // Aplicamos el tema inmediatamente para evitar el "flash" de tema
    // claro al cargar la pagina cuando el usuario tenia tema oscuro.
    document.documentElement.setAttribute('data-theme', this.tema);

    document.addEventListener('mousedown', this.manejarClicFuera);

    // Intentamos restaurar la sesion del usuario a partir del token.
    estadoAutenticacion.restaurarSesion();

    // Si en la peticion anterior dejamos un aviso "flash" (por ejemplo,
    // "sesion expirada" tras un 401), lo recogemos aqui y lo mostramos
    // como notificacion en la primera carga.
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
        // Si el JSON estaba corrupto, lo ignoramos.
      }
    }
  },

  unmounted() {
    document.removeEventListener('mousedown', this.manejarClicFuera);
  }
};
