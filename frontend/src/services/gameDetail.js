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
