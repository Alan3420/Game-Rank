import api from './api';

// Pide al backend el resumen de tendencias de la comunidad:
// juegos mas marcados como favoritos, mejor valorados, mas comentados
// y mas anadidos a colecciones.
export async function obtenerTendencias() {
    try {
        const respuesta = await api.get('/tendencias/');
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener tendencias:', error);
        throw error;
    }
}
