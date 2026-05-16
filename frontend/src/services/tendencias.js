import api from './api';

export async function getTendencias() {
    try {
        const response = await api.get('/tendencias/');
        return response.data;
    } catch (error) {
        console.error('Error al obtener tendencias:', error);
        throw error;
    }
}
