import api from './api';

export async function obtenerJuegosDelCatalogo(pagina, porPagina) {
    if (!pagina) {
        pagina = 1;
    }
    if (!porPagina) {
        porPagina = 20;
    }

    const respuesta = await api.get('/content/catalog', {
        params: {
            page: pagina,
            per_page: porPagina
        }
    });
    return respuesta.data;
}


export async function obtenerVideoDestacado() {
    try {
        const respuesta = await api.get('/content/hero-video');
        return respuesta.data;
    } catch (error) {
        // 404 significa que aun no hay video disponible, devolvemos null
        // para que el componente del Home oculte la seccion
        if (error.response && error.response.status === 404) {
            return null;
        }
        console.error('Error obteniendo video del hero:', error);
        throw error;
    }
}
