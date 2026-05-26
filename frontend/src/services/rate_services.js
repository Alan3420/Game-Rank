import api from './api';

// Crea una nueva calificacion para el juego indicado.
// El "status" es opcional porque a veces calificamos sin cambiar el estado.
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

// Actualiza una calificacion existente del usuario para ese juego.
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

// Elimina la calificacion. Si el backend responde 404 quiere decir que
// no habia calificacion guardada, asi que devolvemos null en vez de tirar error.
export const eliminarCalificacion = async (idJuego) => {
    try {
        const respuesta = await api.delete('/rate/delete', {
            data: { id_game: idJuego }
        });
        return respuesta.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            return null;
        }
        throw error;
    }
};

// Crea o actualiza segun corresponda. Primero intentamos crear; si el backend
// responde 409 es que ya existia, asi que llamamos al update.
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

// Devuelve la nota media del juego segun las calificaciones de todos los usuarios.
// Si algo falla devolvemos null para que la UI muestre "—" sin reventar.
export const obtenerPromedioDeCalificacion = async (idJuego) => {
    try {
        const respuesta = await api.get(`/rate/avg/${idJuego}`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener la media:', error);
        return null;
    }
};
