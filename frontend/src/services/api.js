import axios from 'axios';
import { estadoAutenticacion } from '../store/autenticacion';

var urlBase = 'http://localhost:5000';
if (import.meta.env.VITE_API_URL) {
    urlBase = import.meta.env.VITE_API_URL;
}

const api = axios.create({
    baseURL: urlBase
});


api.interceptors.request.use(function (config) {
    var token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = 'Bearer ' + token;
    }
    return config;
});


// Flag para no disparar el cierre de sesion varias veces si hay multiples
// peticiones en paralelo que reciben 401 a la vez
var sesionExpirada = false;


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

            // Login y register tambien tiran 401 si las credenciales son malas,
            // en esos casos no forzamos la redireccion al login porque ya
            // estamos ahi y la pantalla pinta el error por su cuenta
            var esRutaAuth = false;
            if (url.indexOf('/login') !== -1 || url.indexOf('/register') !== -1) {
                esRutaAuth = true;
            }

            var teniaSesion = !!localStorage.getItem('token');

            if (!esRutaAuth && teniaSesion && !sesionExpirada) {
                sesionExpirada = true;

                estadoAutenticacion.cerrarSesion();

                // Dejamos un aviso en localStorage para que la pantalla
                // de login lo lea al cargar y avise al usuario
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
