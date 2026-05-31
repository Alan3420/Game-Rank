import api from './api';

export async function obtenerDetalleDeJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}`);
        return respuesta.data;
    } catch (error) {
        console.error('Error fetching game detail:', error);
        throw error;
    }
}

export async function obtenerAdiccionesJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}/adicciones`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener adicciones:', error);
        return [];
    }
}

export async function obtenerSagaDelJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}/saga`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener saga del juego:', error);
        return [];
    }
}

export async function obtenerLogrosJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}/logros`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener logros del juego:', error);
        return [];
    }
}
