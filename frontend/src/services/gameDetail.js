import api from './api';

// Trae todos los datos detallados del juego: descripcion, imagenes,
// generos, plataformas, etc. Se usa en la pantalla de detalle.
export async function obtenerDetalleDeJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}`);
        return respuesta.data;
    } catch (error) {
        console.error('Error fetching game detail:', error);
        throw error;
    }
}

// Devuelve la lista de DLC y expansiones del juego.
// Si falla devolvemos array vacio para que la UI siga funcionando.
export async function obtenerAdiccionesJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}/adicciones`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener adicciones:', error);
        return [];
    }
}

// Devuelve los demas juegos que forman parte de la misma saga.
export async function obtenerSagaDelJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}/saga`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener saga del juego:', error);
        return [];
    }
}

// Devuelve la lista de logros del juego.
export async function obtenerLogrosJuego(idJuego) {
    try {
        const respuesta = await api.get(`/content/overview/${idJuego}/logros`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener logros del juego:', error);
        return [];
    }
}
