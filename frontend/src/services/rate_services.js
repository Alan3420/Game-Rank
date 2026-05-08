import api from './api';

export const createRate = async (gameId, rating, status = null) => {
    const response = await api.post('/rate/create', {
        id_game: gameId,
        rating: rating,
        status: status
    });
    return response.data;
};

export const updateRate = async (gameId, rating, status = null) => {
    const response = await api.put('/rate/update', {
        id_game: gameId,
        rating: rating,
        status: status
    });
    return response.data;
};

export const deleteRate = async (gameId) => {
    try {
        const response = await api.delete('/rate/delete', {
            data: { id_game: gameId }
        });
        return response.data;
    } catch (error) {
        if (error.response?.status === 404) return null;
        throw error;
    }
};

export const saveRate = async (gameId, rating) => {
    try {
        return await createRate(gameId, rating);
    } catch (error) {
        if (error.response?.status === 409) {
            return await updateRate(gameId, rating);
        }
        throw error;
    }
};

export const getAvgRate = async (gameId) => {
    try {
        const response = await api.get(`/rate/avg/${gameId}`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener la media:', error);
        return null;
    }
};
