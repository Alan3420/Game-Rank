import axios from 'axios';
import { estadoAutenticacion } from '../store/autenticacion';

// Instancia central de axios que usan todos los servicios para hablar con
// el backend. Se configura la URL base segun el entorno: en desarrollo
// apunta a localhost y en produccion la define VITE_API_URL.
var urlBase = 'http://localhost:5000';
if (import.meta.env.VITE_API_URL) {
    urlBase = import.meta.env.VITE_API_URL;
}

const api = axios.create({
    baseURL: urlBase
});


// Interceptor de peticiones: antes de mandar cualquier request, si el
// usuario tiene token guardado en localStorage lo adjuntamos al header
// Authorization para que el backend pueda identificarlo.
api.interceptors.request.use(function (config) {
    var token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = 'Bearer ' + token;
    }
    return config;
});


// Bandera para evitar que se dispare el cierre de sesion mas de una vez
// cuando llegan varias respuestas 401 a la vez (por ejemplo si la pantalla
// estaba haciendo varias peticiones en paralelo y el token caduco).
var sesionExpirada = false;


// Interceptor de respuestas: si el backend devuelve 401 quiere decir que
// el token ya no es valido. En ese caso cerramos sesion, guardamos un
// aviso para mostrarlo en la pantalla de login y redirigimos al usuario.
api.interceptors.response.use(
    function (response) {
        return response;
    },
    function (error) {

        var status = null;
        if (error.response && error.response.status) {
            status = error.response.status;
        }

        if (status === 401) {

            var url = '';
            if (error.config && error.config.url) {
                url = error.config.url;
            }

            // Los endpoints de login y register tambien devuelven 401 cuando
            // las credenciales son incorrectas; en esos casos NO queremos
            // forzar la redireccion al login, dejamos que la propia pantalla
            // muestre el error.
            var esRutaAuth = false;
            if (url.indexOf('/login') !== -1 || url.indexOf('/register') !== -1) {
                esRutaAuth = true;
            }

            var teniaSesion = !!localStorage.getItem('token');

            if (!esRutaAuth && teniaSesion && !sesionExpirada) {
                sesionExpirada = true;

                estadoAutenticacion.cerrarSesion();

                // Guardamos un aviso "flash" en localStorage para que la
                // pantalla de login lo lea al cargar y muestre la notificacion.
                var avisoFlash = {
                    type: 'error',
                    title: 'Sesión expirada',
                    message: 'Tu sesión ha expirado. Vuelve a iniciar sesión.'
                };
                localStorage.setItem('flashNotificacion', JSON.stringify(avisoFlash));

                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
            }
        }

        return Promise.reject(error);
    }
);


export default api;
