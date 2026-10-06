import {
  obtenerListaDeUsuarios,
  cambiarRolDeUsuario,
  eliminarUsuario as eliminarUsuarioEnBackend
} from '../../services/user_service';
import { notificaciones } from '../../store/notificaciones';
import { confirmacion } from '../../store/confirmacion';
import { formatearFechaCorta } from '../../utils/formatoFecha.js';
import { useRouter, useRoute } from 'vue-router';
import { watchEffect } from 'vue';
import { estadoAutenticacion } from '../../store/autenticacion';


export default {
  name: 'AdminUsers',

  data() {
    return {
      usuarios: [],
      filtro: '',
      loading: true,
      router: null
    };
  },

  computed: {

    usuariosFiltrados() {

      if (!this.filtro.trim()) {
        return this.usuarios;
      }

      var busqueda = this.filtro.toLowerCase();
      var resultado = [];

      for (var i = 0; i < this.usuarios.length; i++) {

        var u = this.usuarios[i];
        var nombre = '';
        var apellido = '';
        var email = '';

        if (u.name) {
          nombre = u.name.toLowerCase();
        }
        if (u.last_name) {
          apellido = u.last_name.toLowerCase();
        }
        if (u.email) {
          email = u.email.toLowerCase();
        }
        var apodo = u.nickname ? u.nickname.toLowerCase() : '';

        if (nombre.indexOf(busqueda) !== -1 ||
            apellido.indexOf(busqueda) !== -1 ||
            apodo.indexOf(busqueda) !== -1 ||
            email.indexOf(busqueda) !== -1) {
          resultado.push(u);
        }
      }

      return resultado;
    }
  },

  mounted() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    this.router = useRouter();
    var route = useRoute();
    var self = this;

    // Esperamos a que la sesion termine de cargar para validar el rol.
    // Si no es admin sacamos un 404 (sin delatar que la ruta existe) y
    // si lo es cargamos los usuarios. En cualquier caso cortamos el watcher
    var parar = null;
    parar = watchEffect(function () {

      if (estadoAutenticacion.cargando) {
        return;
      }

      var esAdmin = false;
      if (estadoAutenticacion.usuario && estadoAutenticacion.usuario.role === 'admin') {
        esAdmin = true;
      }

      if (!esAdmin) {
        if (parar) {
          parar();
        }
        self.router.replace({
          name: 'not-found',
          params: { pathMatch: route.path.substring(1).split('/') }
        });
        return;
      }

      if (parar) {
        parar();
      }
      self.cargarUsuarios();
    });
  },

  methods: {

    async cargarUsuarios() {

      try {
        this.loading = true;
        var data = await obtenerListaDeUsuarios();
        this.usuarios = data.users;
      } catch (error) {
        console.error('Error al cargar usuarios:', error);
        notificaciones.error("User list didn't load. Reload the page to try again.", {
          title: "Loading error"
        });
      } finally {
        this.loading = false;
      }
    },

    async promoverAdmin(usuario) {

      try {
        await cambiarRolDeUsuario(usuario.id_user, 'admin');
        usuario.role = 'admin';
        notificaciones.success(usuario.name + ' has been promoted to administrator.', {
          title: "User promoted"
        });
      } catch (error) {
        console.error('Error al promover usuario:', error);
        notificaciones.error("User wasn't promoted. Check your connection and try again.", {
          title: "Error"
        });
      }
    },

    async degradarAdmin(usuario) {

      try {
        await cambiarRolDeUsuario(usuario.id_user, 'user');
        usuario.role = 'user';
        notificaciones.success(usuario.name + ' has been demoted to user.', {
          title: "User demoted"
        });
      } catch (error) {
        console.error('Error al degradar usuario:', error);
        notificaciones.error("User wasn't demoted. Check your connection and try again.", {
          title: "Error"
        });
      }
    },

    async eliminarUsuario(usuario) {

      var confirmar = await confirmacion.pedir({
        title: 'Delete user?',
        message: usuario.name + ' ' + (usuario.last_name || '') + ' and all their comments, ratings and favorites will be removed permanently.',
        confirmLabel: 'Delete user'
      });
      if (!confirmar) {
        return;
      }

      try {
        await eliminarUsuarioEnBackend(usuario.id_user);

        var nuevaLista = [];
        for (var i = 0; i < this.usuarios.length; i++) {
          if (this.usuarios[i].id_user !== usuario.id_user) {
            nuevaLista.push(this.usuarios[i]);
          }
        }
        this.usuarios = nuevaLista;

        notificaciones.success(usuario.name + ' has been deleted.', {
          title: "User deleted"
        });

      } catch (error) {
        console.error('Error al eliminar usuario:', error);
        notificaciones.error("User wasn't deleted. Check your connection and try again.", {
          title: "Error"
        });
      }
    },

    volver() {
      this.router.push('/profile');
    },

    formatearFecha(fecha) {

      if (!fecha) {
        return 'Not available';
      }

      return formatearFechaCorta(fecha);
    }
  }
};
