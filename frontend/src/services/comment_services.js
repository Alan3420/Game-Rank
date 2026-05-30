import api from './api';

export async function crearComentario(idJuego, descripcion, rating) {
    try {
        const respuesta = await api.post('/comment/create', {
            id_game: idJuego,
            description: descripcion,
            rating: rating
        });
        return respuesta.data;
    } catch (error) {
        console.error('Error al crear el comentario:', error);
        throw error;
    }
}

export async function obtenerComentariosDelJuego(idJuego, limite, desplazamiento) {
    if (!limite) {
        limite = 10;
    }
    if (!desplazamiento) {
        desplazamiento = 0;
    }

    try {
        const respuesta = await api.get(`/comment/game/${idJuego}`, {
            params: {
                limit: limite,
                offset: desplazamiento
            }
        });
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener comentarios:', error);
        throw error;
    }
}

export async function obtenerTodosLosComentarios() {
    try {
        const respuesta = await api.get('/comment/all');
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener todos los comentarios:', error);
        throw error;
    }
}

export async function eliminarComentario(idComentario) {
    try {
        const respuesta = await api.delete(`/comment/delete/${idComentario}`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al eliminar el comentario:', error);
        throw error;
    }
}

export async function actualizarComentario(idComentario, descripcion, rating) {
    try {
        const respuesta = await api.put(`/comment/update/${idComentario}`, {
            description: descripcion,
            rating: rating
        });
        return respuesta.data;
    } catch (error) {
        console.error('Error al actualizar el comentario:', error);
        throw error;
    }
}

export async function obtenerPromedioDeCalificacion(idJuego) {
    try {
        const respuesta = await api.get(`/comment/avg/${idJuego}`);
        return respuesta.data;
    } catch (error) {
        console.error('Error al obtener la media:', error);
        return null;
    }
}
