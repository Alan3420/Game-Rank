import { getListUsers, changeUserRole, deleteUser } from '../../services/user_service';
import { notificaciones } from '../../store/notificaciones';
import { useRouter } from 'vue-router';

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

  async mounted() {
    this.router = useRouter();
    await this.cargarUsuarios();
  },

  methods: {
    async cargarUsuarios() {

      try {

        this.loading = true;
        const data = await getListUsers();
        this.usuarios = data.users;

      } catch (error) {
        
        console.error('Error al cargar usuarios:', error);
        notificaciones.error("No pudimos cargar la lista de usuarios.", {
          title: "Error al cargar"
        });

      } finally {
        this.loading = false;
      }

    },

    async promoverAdmin(usuario) {
      try {

        await changeUserRole(usuario.id_user, 'admin');

        usuario.role = 'admin';
        notificaciones.success(`${usuario.name} ha sido promovido a administrador.`, {
          title: "Usuario promovido"
        });

      } catch (error) {

        console.error('Error al promover usuario:', error);
        notificaciones.error("No pudimos promover al usuario.", {
          title: "Error"
        });

      }

    },

    async degradarAdmin(usuario) {

      try {

        await changeUserRole(usuario.id_user, 'user');
        usuario.role = 'user';
        notificaciones.success(`${usuario.name} ha sido degradado a usuario.`, {
          title: "Usuario degradado"
        });

      } catch (error) {

        console.error('Error al degradar usuario:', error);
        notificaciones.error("No pudimos degradar al usuario.", {
          title: "Error"
        });

      }
    },

    async eliminarUsuario(usuario) {

      const confirmar = confirm(`¿Estás seguro de que deseas eliminar a ${usuario.name}?`);
      if (!confirmar) return;

      try {

        await deleteUser(usuario.id_user);
        this.usuarios = this.usuarios.filter(u => u.id_user !== usuario.id_user);
        notificaciones.success(`${usuario.name} ha sido eliminado.`, {
          title: "Usuario eliminado"
        });

      } catch (error) {

        console.error('Error al eliminar usuario:', error);
        notificaciones.error("No pudimos eliminar al usuario.", {
          title: "Error"
        });

      }
    },

    goBack() {
      this.router.push('/profile');
    },
    
    formatDate(date) {
      if (!date) return 'No disponible';
      const d = new Date(date);
      const meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
      return `${d.getDate()} ${meses[d.getMonth()]} ${d.getFullYear()}`;
    }
  }
};