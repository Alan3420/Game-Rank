import {
  obtenerTodosLosComentarios,
  eliminarComentario as eliminarComentarioEnBackend
} from '../../services/comment_services';
import { notificaciones } from '../../store/notificaciones';
import { useRouter, useRoute } from 'vue-router';
import { watchEffect } from 'vue';
import { estadoAutenticacion } from '../../store/autenticacion';

// Panel de moderacion donde el admin ve TODOS los comentarios del sistema
// y puede borrarlos. La proteccion de acceso funciona igual que en
// AdminUsers: si entras y no eres admin, 404 sin revelar la ruta.
export default {
  name: 'AdminComments',

  data() {
    return {
      comentarios: [],
      filtro: '',
      loading: true,
      router: null
    };
  },

  computed: {

    // Filtra la lista por nombre de usuario, apellido o descripcion del
    // comentario. La busqueda es case-insensitive.
    comentariosFiltrados() {

      if (!this.filtro.trim()) {
        return this.comentarios;
      }

      var busqueda = this.filtro.toLowerCase();
      var resultado = [];

      for (var i = 0; i < this.comentarios.length; i++) {

        var c = this.comentarios[i];
        var nombre = '';
        var apellido = '';
        var descripcion = '';

        if (c.username) {
          nombre = c.username.toLowerCase();
        }
        if (c.user_last_name) {
          apellido = c.user_last_name.toLowerCase();
        }
        if (c.description) {
          descripcion = c.description.toLowerCase();
        }

        if (nombre.indexOf(busqueda) !== -1 ||
            apellido.indexOf(busqueda) !== -1 ||
            descripcion.indexOf(busqueda) !== -1) {
          resultado.push(c);
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
      self.cargarComentarios();
    });
  },

  methods: {

    // Pide al backend todos los comentarios del sistema.
    async cargarComentarios() {

      try {
        this.loading = true;
        var data = await obtenerTodosLosComentarios();
        this.comentarios = data.comments;
      } catch (error) {
        console.error('Error al cargar comentarios:', error);
        notificaciones.error("We couldn't load the comments.", { title: "Loading error" });
      } finally {
        this.loading = false;
      }
    },

    // Confirma con el admin y borra el comentario seleccionado.
    async eliminarComentario(comentario) {

      var confirmar = confirm('Delete comment by ' + comentario.username + '?');
      if (!confirmar) {
        return;
      }

      try {
        await eliminarComentarioEnBackend(comentario.id_comment);

        // Quitamos el comentario de la lista local sin recargar todo.
        var nuevaLista = [];
        for (var i = 0; i < this.comentarios.length; i++) {
          if (this.comentarios[i].id_comment !== comentario.id_comment) {
            nuevaLista.push(this.comentarios[i]);
          }
        }
        this.comentarios = nuevaLista;

        notificaciones.success("Comment deleted.", { title: "Comment deleted" });

      } catch (error) {
        console.error('Error al eliminar comentario:', error);
        notificaciones.error("We couldn't delete the comment.", { title: "Error" });
      }
    },

    // Formatea una fecha ISO al formato "12 Mar 2026" para mostrarla en
    // la tabla. Las abreviaciones de mes en ingles porque la UI esta en ingles.
    formatearFecha(valor) {

      if (!valor) {
        return '—';
      }

      var meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var d = new Date(valor);

      return d.getDate() + ' ' + meses[d.getMonth()] + ' ' + d.getFullYear();
    },

    // Boton "Back": vuelve al perfil.
    volver() {
      this.router.push('/profile');
    }
  }
};
