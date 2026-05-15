import api from './api';

export async function getGameDetail(gameId) {
    try {
        const response = await api.get(`/content/overview/${gameId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching game detail:', error);
        throw error;
    }
}

export async function obtenerAdiccionesJuego(gameId) {
    try {
        const response = await api.get(`/content/overview/${gameId}/adicciones`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener adicciones:', error);
        return [];
    }
}

export async function obtenerSagaDelJuego(gameId) {
    try {
        const response = await api.get(`/content/overview/${gameId}/saga`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener saga del juego:', error);
        return [];
    }
}

export async function obtenerLogrosJuego(gameId) {
    try {
        const response = await api.get(`/content/overview/${gameId}/logros`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener logros del juego:', error);
        return [];
    }
}
