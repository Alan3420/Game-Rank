import { getAllComments, deleteComment } from '../../services/comment_services';
import { notificaciones } from '../../store/notificaciones';
import { useRouter } from 'vue-router';
import { watchEffect } from 'vue';
import { useRoute } from 'vue-router';
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
      if (!this.filtro.trim()) return this.comentarios;
      const q = this.filtro.toLowerCase();
      return this.comentarios.filter(c =>
        c.username?.toLowerCase().includes(q) ||
        c.user_last_name?.toLowerCase().includes(q) ||
        c.description?.toLowerCase().includes(q)
      );
    }
  },
  mounted() {
    this.router = useRouter();
    const route = useRoute();

    const parar = watchEffect(() => {
      if (estadoAutenticacion.cargando) return;

      if (!estadoAutenticacion.usuario || estadoAutenticacion.usuario.role !== 'admin') {
        parar();
        this.router.replace({
          name: 'not-found',
          params: { pathMatch: route.path.substring(1).split('/') }
        });
        return;
      }

      parar();
      this.cargarComentarios();
    });
  },
  methods: {
    async cargarComentarios() {
      try {
        this.loading = true;
        const data = await getAllComments();
        this.comentarios = data.comments;
      } catch (error) {
        console.error('Error al cargar comentarios:', error);
        notificaciones.error("We couldn't load the comments.", { title: "Loading error" });
      } finally {
        this.loading = false;
      }
    },

    async eliminarComentario(comentario) {
      const confirmar = confirm(`Delete comment by ${comentario.username}?`);
      if (!confirmar) return;

      try {
        await deleteComment(comentario.id_comment);
        this.comentarios = this.comentarios.filter(c => c.id_comment !== comentario.id_comment);
        notificaciones.success("Comment deleted.", { title: "Comment deleted" });
      } catch (error) {
        console.error('Error al eliminar comentario:', error);
        notificaciones.error("We couldn't delete the comment.", { title: "Error" });
      }
    },

    formatDate(value) {
      if (!value) return '—';
      const d = new Date(value);
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
    },

    goBack() {
      this.router.push('/profile');
    }
  }
};
