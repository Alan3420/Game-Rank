import api from './api';

// Pide al backend la pagina del catalogo general de juegos.
// Se usa para llenar las cards del listado principal.
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


// Pide al backend el video destacado que se muestra en el hero del Home.
// Si el backend responde 404 (todavia no hay video) devolvemos null
// para que el componente sepa que debe ocultar la seccion.
export async function obtenerVideoDestacado() {
    try {
        const respuesta = await api.get('/content/hero-video');
        return respuesta.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            return null;
        }
        console.error('Error obteniendo video del hero:', error);
        throw error;
    }
}
