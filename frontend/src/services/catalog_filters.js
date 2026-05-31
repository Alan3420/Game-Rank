import api from './api';

export async function obtenerJuegosFiltrados(pagina, porPagina, filtros) {
    if (!pagina) {
        pagina = 1;
    }
    if (!porPagina) {
        porPagina = 20;
    }
    if (!filtros) {
        filtros = {};
    }

    const parametros = {
        page: pagina,
        per_page: porPagina
    };

    if (filtros.ordering) {
        parametros.ordering = filtros.ordering;
    }

    if (filtros.genres && filtros.genres.length > 0) {
        parametros.genres = filtros.genres.join(',');
    }

    if (filtros.platforms && filtros.platforms.length > 0) {
        parametros.platforms = filtros.platforms.join(',');
    }

    if (filtros.search) {
        parametros.search = filtros.search;
    }

    // El backend quiere el rango como "AAAA-MM-DD,AAAA-MM-DD", asi que si
    // el usuario solo marca un extremo del rango rellenamos el otro con
    // 1980 (minimo) o el 31 de diciembre del anio actual (maximo)
    if (filtros.dateFrom || filtros.dateTo) {
        var anioActual = new Date().getFullYear();
        var fechaInicio = '';
        var fechaFin = '';

        if (filtros.dateFrom) {
            fechaInicio = filtros.dateFrom + '-01-01';
        } else {
            fechaInicio = '1980-01-01';
        }

        if (filtros.dateTo) {
            fechaFin = filtros.dateTo + '-12-31';
        } else {
            fechaFin = anioActual + '-12-31';
        }

        parametros.dates = fechaInicio + ',' + fechaFin;
    }

    const respuesta = await api.get('/content/filtered', { params: parametros });
    return respuesta.data;
}
