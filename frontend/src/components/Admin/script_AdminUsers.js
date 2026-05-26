import {
  obtenerListaDeUsuarios,
  cambiarRolDeUsuario,
  eliminarUsuario as eliminarUsuarioEnBackend
} from '../../services/user_service';
import { notificaciones } from '../../store/notificaciones';
import { useRouter, useRoute } from 'vue-router';
import { watchEffect } from 'vue';
import { estadoAutenticacion } from '../../store/autenticacion';

// Panel de administracion para gestionar los usuarios registrados.
// Solo accesible para usuarios con rol "admin". Si el usuario no es admin
// devolvemos 404 conservando la URL para no revelar que la pagina existe.
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

    // Devuelve la lista filtrada por el texto que escribio el admin.
    // Sin texto devolvemos la lista completa. Con texto buscamos en nombre,
    // apellido y email (case-insensitive).
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

        if (nombre.indexOf(busqueda) !== -1 ||
            apellido.indexOf(busqueda) !== -1 ||
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

    // Usamos watchEffect para reaccionar al estado de la sesion. Cuando
    // termina de cargar comprobamos el rol: si no es admin, redirigimos a
    // 404 sin revelar la existencia de la ruta. Si es admin, cargamos
    // los usuarios. En cualquier caso cortamos el watcher despues para
    // que no vuelva a dispararse.
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

    // Pide al backend la lista completa de usuarios.
    async cargarUsuarios() {

      try {
        this.loading = true;
        var data = await obtenerListaDeUsuarios();
        this.usuarios = data.users;
      } catch (error) {
        console.error('Error al cargar usuarios:', error);
        notificaciones.error("We couldn't load the user list.", {
          title: "Loading error"
        });
      } finally {
        this.loading = false;
      }
    },

    // Sube al usuario indicado al rol de administrador.
    async promoverAdmin(usuario) {

      try {
        await cambiarRolDeUsuario(usuario.id_user, 'admin');
        usuario.role = 'admin';
        notificaciones.success(usuario.name + ' has been promoted to administrator.', {
          title: "User promoted"
        });
      } catch (error) {
        console.error('Error al promover usuario:', error);
        notificaciones.error("We couldn't promote the user.", {
          title: "Error"
        });
      }
    },

    // Baja al usuario del rol de administrador al rol normal.
    async degradarAdmin(usuario) {

      try {
        await cambiarRolDeUsuario(usuario.id_user, 'user');
        usuario.role = 'user';
        notificaciones.success(usuario.name + ' has been demoted to user.', {
          title: "User demoted"
        });
      } catch (error) {
        console.error('Error al degradar usuario:', error);
        notificaciones.error("We couldn't demote the user.", {
          title: "Error"
        });
      }
    },

    // Confirma con el admin y borra el usuario del sistema.
    async eliminarUsuario(usuario) {

      var confirmar = confirm('Are you sure you want to delete ' + usuario.name + '?');
      if (!confirmar) {
        return;
      }

      try {
        await eliminarUsuarioEnBackend(usuario.id_user);

        // Reconstruimos la lista local sin el usuario eliminado para
        // que la tabla se actualice sin recargar todo.
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
        notificaciones.error("We couldn't delete the user.", {
          title: "Error"
        });
      }
    },

    // Boton "Back": vuelve al perfil del propio admin.
    volver() {
      this.router.push('/profile');
    },

    // Formatea una fecha ISO al formato "12 Mar 2026" para mostrarla en
    // la tabla. Las abreviaciones de mes estan en ingles porque la UI
    // completa esta en ingles.
    formatearFecha(fecha) {

      if (!fecha) {
        return 'Not available';
      }

      var meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var d = new Date(fecha);

      return d.getDate() + ' ' + meses[d.getMonth()] + ' ' + d.getFullYear();
    }
  }
};
