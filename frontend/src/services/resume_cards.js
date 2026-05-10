import api from './api';

export async function getContentOverview(page = 1, game_name = null) {
    try {
        const response = await api.get('/content/overview', {
            params: {
                page: page,
                per_page: 10,
                name: game_name
            }
        });

        return response.data;

    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function getHeroVideo() {
    try {
        const response = await api.get('/content/hero-video');
        return response.data;
    } catch (error) {
        console.error('Error obteniendo video del hero:', error);
        throw error;
    }
}