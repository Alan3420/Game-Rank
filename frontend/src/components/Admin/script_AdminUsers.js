import { getListUsers, changeUserRole, deleteUser } from '../../services/user_service';
import { notificaciones } from '../../store/notificaciones';
import { useRouter } from 'vue-router';
import { watchEffect } from 'vue';
import { useRoute } from 'vue-router';
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

      const busqueda = this.filtro.toLowerCase();

      return this.usuarios.filter(u =>
        u.name?.toLowerCase().includes(busqueda) ||
        u.last_name?.toLowerCase().includes(busqueda) ||
        u.email?.toLowerCase().includes(busqueda)
      );
    }
  },

  mounted() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    this.router = useRouter();
    const route = useRoute();

    // Reactivo al estado de sesión: muestra 404 si no es admin (sin revelar que la ruta existe)
    let parar = null;
    parar = watchEffect(() => {
      if (estadoAutenticacion.cargando) return;

      if (!estadoAutenticacion.usuario || estadoAutenticacion.usuario.role !== 'admin') {
        parar?.();
        this.router.replace({
          name: 'not-found',
          params: { pathMatch: route.path.substring(1).split('/') }
        });
        return;
      }

      parar?.();
      this.cargarUsuarios();
    });
  },

  methods: {
    async cargarUsuarios() {

      try {

        this.loading = true;
        const data = await getListUsers();
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

    async promoverAdmin(usuario) {
      try {

        await changeUserRole(usuario.id_user, 'admin');

        usuario.role = 'admin';
        notificaciones.success(`${usuario.name} has been promoted to administrator.`, {
          title: "User promoted"
        });

      } catch (error) {

        console.error('Error al promover usuario:', error);
        notificaciones.error("We couldn't promote the user.", {
          title: "Error"
        });

      }

    },

    async degradarAdmin(usuario) {

      try {

        await changeUserRole(usuario.id_user, 'user');
        usuario.role = 'user';
        notificaciones.success(`${usuario.name} has been demoted to user.`, {
          title: "User demoted"
        });

      } catch (error) {

        console.error('Error al degradar usuario:', error);
        notificaciones.error("We couldn't demote the user.", {
          title: "Error"
        });

      }
    },

    async eliminarUsuario(usuario) {

      const confirmar = confirm(`Are you sure you want to delete ${usuario.name}?`);
      if (!confirmar) return;

      try {

        await deleteUser(usuario.id_user);
        this.usuarios = this.usuarios.filter(u => u.id_user !== usuario.id_user);
        notificaciones.success(`${usuario.name} has been deleted.`, {
          title: "User deleted"
        });

      } catch (error) {

        console.error('Error al eliminar usuario:', error);
        notificaciones.error("We couldn't delete the user.", {
          title: "Error"
        });

      }
    },

    goBack() {
      this.router.push('/profile');
    },
    
    formatDate(date) {
      if (!date) return 'Not available';
      const d = new Date(date);
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
    }
  }
};