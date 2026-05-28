import api from './api';

export async function crearComentario(idJuego, descripcion) {
    try {
        const respuesta = await api.post('/comment/create', {
            id_game: idJuego,
            description: descripcion
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

export async function actualizarComentario(idComentario, descripcion) {
    try {
        const respuesta = await api.put(`/comment/update/${idComentario}`, {
            description: descripcion
        });
        return respuesta.data;
    } catch (error) {
        console.error('Error al actualizar el comentario:', error);
        throw error;
    }
}
