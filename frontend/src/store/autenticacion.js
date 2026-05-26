import { reactive } from 'vue';
import { obtenerMiUsuario } from '../services/user_service';

// Estado reactivo global de la sesion del usuario.
// Cualquier componente puede importarlo y leer "usuario" o "cargando"
// y Vue se encarga de actualizar la UI cuando cambien.
//
// cargando arranca en true solo si ya hay un token en localStorage, porque
// en ese caso vamos a pedir los datos del usuario al backend y conviene que
// la UI muestre un estado de espera hasta que termine la peticion.
export const estadoAutenticacion = reactive({

    usuario: null,
    cargando: !!localStorage.getItem("token"),

    // Guarda en el estado los datos del usuario y deja el token persistente
    // en localStorage para que sobreviva a recargas de pagina.
    iniciarSesion(datosRecibidos, token) {
        this.usuario = datosRecibidos;
        localStorage.setItem("token", token);
    },

    // Se llama al cargar la app. Si hay token guardado intenta restaurar la
    // sesion pidiendo los datos del usuario actual al backend. Si el token
    // esta caducado o invalido cerramos sesion para limpiar el estado.
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

    // Limpia el estado de usuario y borra el token guardado.
    cerrarSesion() {
        this.usuario = null;
        localStorage.removeItem("token");
    },

    // Actualiza campos sueltos del usuario sin perder los demas datos.
    // Se usa, por ejemplo, despues de editar el perfil para que el menu
    // del header refleje el nuevo nombre o nickname al instante.
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
