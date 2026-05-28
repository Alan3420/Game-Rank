import { reactive } from 'vue';
import { obtenerMiUsuario } from '../services/user_service';


export const estadoAutenticacion = reactive({

    usuario: null,
    // Si hay token vamos a pedir el usuario al backend, asi que arrancamos
    // en estado de carga para que la UI muestre spinner mientras tanto
    cargando: !!localStorage.getItem("token"),

    iniciarSesion(datosRecibidos, token) {
        this.usuario = datosRecibidos;
        localStorage.setItem("token", token);
    },

    async restaurarSesion() {
        const token = localStorage.getItem("token");

        if (!token) {
            this.cargando = false;
            return;
        }

        try {
            const data = await obtenerMiUsuario();
            this.usuario = data.user;
        } catch (error) {
            console.error('No se pudo restaurar la sesion:', error);
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
        if (!this.usuario) {
            return;
        }

        for (var clave in datosNuevos) {
            if (Object.prototype.hasOwnProperty.call(datosNuevos, clave)) {
                this.usuario[clave] = datosNuevos[clave];
            }
        }
    }
});
