import api from "./api";

export const addTOFavorite = async (gameID) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }
        const response = await api.post(`/favorite/add`, { id_game: gameID })

        return response.data;
    }
    catch (error) {
        console.error(error.response.data.message);
    }
}

export const removeTOFavorite = async (gameID) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const response = await api.delete('/favorite/remove',
            {
                data: { id_game: gameID }
            }
        );

        return response.data;
    } catch (error) {
        console.error("Error al eliminar favorito:", error.response?.data?.message || error.message);
        throw error;
    }
}

export const checkFavorite = async (gameID) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const response = await api.get(`/favorite/check/${gameID}`);
        return response.data;
    }
    catch (error) {
        console.error(error.response.data.message);
    }
}

export const list_favorites = async () => {

    try {
        const token = localStorage.getItem("token");
        
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const response = await api.get(`/favorite/listFav`);
        return response.data;
    }
    catch (error) {
        console.error(error.response.data.message);
    }
}