import api from './api';

export async function getCatalogGames(page = 1, perPage = 20) {
    const response = await api.get('/content/catalog', {
        params: { page, per_page: perPage }
    });
    return response.data;
}


export async function getHeroVideo() {
    try {
        const response = await api.get('/content/hero-video');
        return response.data;
    } catch (error) {
        if (error.response?.status === 404) {
            return null;
        }
        console.error('Error obteniendo video del hero:', error);
        throw error;
    }
}