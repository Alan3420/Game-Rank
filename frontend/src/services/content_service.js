import api from './api';

export const getContentOverview = async () => {
    try {
        const response = await api.get('/content/overview');
        return response.data;
    } catch (error) {
        console.error('Error fetching content overview:', error);
        throw error;
    }
};