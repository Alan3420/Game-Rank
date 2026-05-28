import {
  obtenerTodosLosComentarios,
  eliminarComentario as eliminarComentarioEnBackend
} from '../../services/comment_services';
import { notificaciones } from '../../store/notificaciones';
import { useRouter, useRoute } from 'vue-router';
import { watchEffect } from 'vue';
import { estadoAutenticacion } from '../../store/autenticacion';


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

    // Misma proteccion que AdminUsers: si no es admin, 404 sin delatar
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

    async eliminarComentario(comentario) {

      var confirmar = confirm('Delete comment by ' + comentario.username + '?');
      if (!confirmar) {
        return;
      }

      try {
        await eliminarComentarioEnBackend(comentario.id_comment);

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

    formatearFecha(valor) {

      if (!valor) {
        return '—';
      }

      var meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var d = new Date(valor);

      return d.getDate() + ' ' + meses[d.getMonth()] + ' ' + d.getFullYear();
    },

    volver() {
      this.router.push('/profile');
    }
  }
};
