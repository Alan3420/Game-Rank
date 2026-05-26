import api from './api';

// Trae desde el backend la lista paginada de juegos cuyo lanzamiento todavia
// no ha ocurrido, para mostrarlos en la seccion de proximos lanzamientos.
export async function obtenerProximosLanzamientos(pagina, porPagina) {
    if (!pagina) {
        pagina = 1;
    }
    if (!porPagina) {
        porPagina = 10;
    }

    try {
        const respuesta = await api.get('/content/release', {
            params: {
                page: pagina,
                per_page: porPagina
            }
        });
        return respuesta.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}
