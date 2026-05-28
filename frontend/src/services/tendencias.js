import api from './api';

export async function obtenerTendencias() {
    try {
        const respuesta = await api.get('/tendencias/');
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener tendencias:', error);
        throw error;
    }
}
