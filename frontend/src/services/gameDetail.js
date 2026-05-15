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

export async function obtenerSagaDelJuego(gameId) {
    try {
        const response = await api.get(`/content/overview/${gameId}/saga`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener saga del juego:', error);
        return [];
    }
}
