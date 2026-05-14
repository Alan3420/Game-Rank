import { reactive } from 'vue';
import { getMe } from '../services/user_service';

export const estadoAutenticacion = reactive({

    usuario: null,

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