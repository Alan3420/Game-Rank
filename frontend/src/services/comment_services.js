import api from './api';

export async function createComments(id_game, description) {
    try {
        const tokenUser = localStorage.getItem("token")
        const response = await api.post(`/comment/create`, {
            id_game: id_game,
            description: description
        },
        );

        return response.data;
    } catch (error) {
        console.error('Error al crear el comentario::', error);
        throw error;
    }
}

export async function getCommentsByGame(game_id, limit = 10, offset = 0) {
    try {
        const response = await api.get(`/comment/game/${game_id}`, {
            params: { limit, offset }
        });
        return response.data;
    } catch (error) {
        console.error('Error al obtener comentarios:', error);
        throw error;
    }
}

export async function getAllComments() {
    try {
        const response = await api.get('/comment/all');
        return response.data;
    } catch (error) {
        console.error('Error al obtener todos los comentarios:', error);
        throw error;
    }
}

export async function deleteComment(comment_id) {
    try {
        const tokenUser = localStorage.getItem("token")
        const response = await api.delete(`/comment/delete/${comment_id}`);

        return response.data;
    } catch (error) {
        console.error('Error al eliminar el comentario:', error);
        throw error;
    }
}

export async function updateComment(comment_id, description) {
    try {

        const tokenUser = localStorage.getItem("token")
        const response = await api.put(`/comment/update/${comment_id}`, {
            description: description
        });
        
        return response.data;
    } catch (error) {
        console.error('Error al actualizar el comentario:', error);
        throw error;
    }
}