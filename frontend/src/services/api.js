import axios from 'axios';
import { estadoAutenticacion } from '../store/autenticacion';

const api = axios.create({
    // Para pruebas en mobil 192.168.1.XXX, pruebas generales localhost, para identificar la ip local CMD ipconfig
    baseURL: 'http://localhost:5000'
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

let sesionExpirada = false;

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            const url = error.config?.url || '';
            const esRutaAuth = url.includes('/login') || url.includes('/register');
            const teniaSesion = !!localStorage.getItem('token');

            if (!esRutaAuth && teniaSesion && !sesionExpirada) {
                sesionExpirada = true;
                estadoAutenticacion.cerrarSesion();
                localStorage.setItem('flashNotificacion', JSON.stringify({
                    type: 'error',
                    title: 'Sesión expirada',
                    message: 'Tu sesión ha expirado. Vuelve a iniciar sesión.'
                }));
                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;