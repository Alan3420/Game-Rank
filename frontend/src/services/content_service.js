import api from './api';

export async function getContentOverview (contentOverview, user_id) {
    try {
        const response = await api.get('/content/overview',{
            contentOverview: contentOverview,
            user_id: user_id
        });

        return response.data;
    } catch (error) {
        console.error('Error al cargar el resumen del contenido:', error);
        throw error;
    }
};