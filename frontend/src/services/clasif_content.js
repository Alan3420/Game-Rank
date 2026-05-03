import api from './api';

export async function getFutureReleases(page = 1, per_page = 10) {
    try {
        const response = await api.get('/content/release', {
            params: { page, per_page }
        })
        return response.data
    } catch (error) {
        console.error(error)
        throw error
    }
}
