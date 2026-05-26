import api from "./api";

// Marca el juego indicado como favorito del usuario actual.
// Si no hay token en localStorage abortamos sin pegarle al backend.
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

// Quita el juego de la lista de favoritos del usuario.
// Relanzamos el error para que la pantalla pueda revertir el icono si falla.
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

// Pregunta al backend si el juego ya esta marcado como favorito por el usuario.
// El componente usa este dato para pintar el corazon lleno o vacio.
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

// Devuelve la lista completa de favoritos del usuario para pintarlos
// en la pantalla de perfil.
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
