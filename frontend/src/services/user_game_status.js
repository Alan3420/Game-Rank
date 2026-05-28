import api from "./api";

export const establecerEstadoDeJuego = async (idJuego, estado) => {
    const respuesta = await api.post("/status/set", {
        id_game: idJuego,
        status: estado
    });
    return respuesta.data;
};

export const obtenerEstadoDeJuego = async (idJuego) => {
    const respuesta = await api.get(`/status/${idJuego}`);
    return respuesta.data;
};

export const eliminarEstadoDeJuego = async (idJuego) => {
    const respuesta = await api.delete(`/status/${idJuego}`);
    return respuesta.data;
};

// Version ligera, solo (id_juego, estado) para los badges del catalogo
export const listarEstadosDeJuego = async () => {
    const respuesta = await api.get("/status/list");
    return respuesta.data;
};

// Version completa con datos del juego, para la pantalla de perfil
export const listarEstadosDeJuegoCompletos = async () => {
    const respuesta = await api.get("/status/list/full");
    return respuesta.data;
};
