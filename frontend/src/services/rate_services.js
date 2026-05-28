import api from './api';

export const crearCalificacion = async (idJuego, calificacion, estado) => {
    if (estado === undefined) {
        estado = null;
    }

    const respuesta = await api.post('/rate/create', {
        id_game: idJuego,
        rating: calificacion,
        status: estado
    });
    return respuesta.data;
};

export const actualizarCalificacion = async (idJuego, calificacion, estado) => {
    if (estado === undefined) {
        estado = null;
    }

    const respuesta = await api.put('/rate/update', {
        id_game: idJuego,
        rating: calificacion,
        status: estado
    });
    return respuesta.data;
};

export const eliminarCalificacion = async (idJuego) => {
    try {
        const respuesta = await api.delete('/rate/delete', {
            data: { id_game: idJuego }
        });
        return respuesta.data;
    } catch (error) {
        // Si el backend devuelve 404 es que no habia nada que borrar,
        // devolvemos null para que la UI no muestre un error feo
        if (error.response && error.response.status === 404) {
            return null;
        }
        throw error;
    }
};

// Intentamos crear y si el backend dice 409 (ya existia) llamamos al update.
// Asi el componente no tiene que saber si era el primer voto o no
export const guardarCalificacion = async (idJuego, calificacion) => {
    try {
        const respuesta = await crearCalificacion(idJuego, calificacion);
        return respuesta;
    } catch (error) {
        if (error.response && error.response.status === 409) {
            const respuestaActualizada = await actualizarCalificacion(idJuego, calificacion);
            return respuestaActualizada;
        }
        throw error;
    }
};

export const obtenerPromedioDeCalificacion = async (idJuego) => {
    try {
        const respuesta = await api.get(`/rate/avg/${idJuego}`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener la media:', error);
        return null;
    }
};
