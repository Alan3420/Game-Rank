import { reactive } from 'vue';

export const estadoAutenticacion = reactive({

    //iniciar sesion y guardar datos en localStorage
    iniciarSesion(datosRecibidos, token) {
        this.usuario = datosRecibidos;
        localStorage.setItem("datos_usuario", JSON.stringify(datosRecibidos));
        localStorage.setItem("token", token);
    },

    usuario: JSON.parse(localStorage.getItem("datos_usuario")) || null,


    // Funcion para limpiar todo al salir
    cerrarSesion() {
        this.usuario = null;
        localStorage.removeItem("datos_usuario");
        localStorage.removeItem("token");
    }
});