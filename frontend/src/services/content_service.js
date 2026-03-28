import api from './api';

export async function getContentOverview (game_id) {
    try {
        const response = await api.get('/content/overview',{
            params:{"game_id":game_id}
        });
        return response.data;
    } catch (error) {
        console.error('Error al cargar el resumen del contenido:', error);
        throw error;
    }
};