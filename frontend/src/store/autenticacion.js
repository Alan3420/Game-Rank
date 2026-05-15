import { reactive } from 'vue';
import { getMe } from '../services/user_service';

export const estadoAutenticacion = reactive({

    usuario: null,
    cargando: !!localStorage.getItem("token"),

    iniciarSesion(datosRecibidos, token) {
        this.usuario = datosRecibidos;
        localStorage.setItem("token", token);
    },

    async restaurarSesion() {
        const token = localStorage.getItem("token");
        if (!token) return;
        try {
            const data = await getMe();
            this.usuario = data.user;
        } catch {
            this.cerrarSesion();
        } finally {
            this.cargando = false;
        }
    },

    cerrarSesion() {
        this.usuario = null;
        localStorage.removeItem("token");
    },

    actualizarUsuario(datosNuevos) {
        this.usuario = { ...this.usuario, ...datosNuevos };
    }
});