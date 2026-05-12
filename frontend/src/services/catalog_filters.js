import api from './api';

export async function getFilteredGames(page = 1, perPage = 20, filters = {}) {
    const params = { page, per_page: perPage };

    if (filters.ordering) params.ordering = filters.ordering;
    if (filters.genres && filters.genres.length > 0) params.genres = filters.genres.join(',');
    if (filters.platforms && filters.platforms.length > 0) params.platforms = filters.platforms.join(',');
    if (filters.search) params.search = filters.search;

    if (filters.dateFrom || filters.dateTo) {
        const from = filters.dateFrom ? `${filters.dateFrom}-01-01` : '1980-01-01';
        const to = filters.dateTo ? `${filters.dateTo}-12-31` : `${new Date().getFullYear()}-12-31`;
        params.dates = `${from},${to}`;
    }

    const response = await api.get('/content/filtered', { params });
    return response.data;
}
