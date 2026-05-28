import api from "./api";

export const agregarAFavoritos = async (idJuego) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const respuesta = await api.post('/favorite/add', {
            id_game: idJuego
        });

        return respuesta.data;
    } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
            console.error(error.response.data.message);
        } else {
            console.error(error);
        }
    }
}

export const quitarDeFavoritos = async (idJuego) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const respuesta = await api.delete('/favorite/remove', {
            data: { id_game: idJuego }
        });

        return respuesta.data;
    } catch (error) {
        var mensaje = "";
        if (error.response && error.response.data && error.response.data.message) {
            mensaje = error.response.data.message;
        } else {
            mensaje = error.message;
        }
        console.error("Error al eliminar favorito:", mensaje);
        throw error;
    }
}

export const consultarSiEsFavorito = async (idJuego) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const respuesta = await api.get(`/favorite/check/${idJuego}`);
        return respuesta.data;
    } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
            console.error(error.response.data.message);
        } else {
            console.error(error);
        }
    }
}

export const obtenerListaDeFavoritos = async () => {
    try {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No se encontró el token de autenticación.");
            return;
        }

        const respuesta = await api.get('/favorite/listFav');
        return respuesta.data;
    } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
            console.error(error.response.data.message);
        } else {
            console.error(error);
        }
    }
}
