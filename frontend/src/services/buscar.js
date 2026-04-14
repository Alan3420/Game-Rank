import api from './api';

export async function getContentByName(game_name) {
    try {
        const response = await api.get('/content/search', {
            params: { name: game_name }
        })
        return response.data
    } catch (error) {
        console.error(error)
        throw error
    }
}