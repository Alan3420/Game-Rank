import api from "./api";

// Guarda en que estado tiene el usuario un juego (por ejemplo "playing",
// "completed", "dropped"). Si ya existia, el backend lo reemplaza.
export const establecerEstadoDeJuego = async (idJuego, estado) => {
    const respuesta = await api.post("/status/set", {
        id_game: idJuego,
        status: estado
    });
    return respuesta.data;
};

// Pide el estado guardado por el usuario para un juego concreto.
export const obtenerEstadoDeJuego = async (idJuego) => {
    const respuesta = await api.get(`/status/${idJuego}`);
    return respuesta.data;
};

// Borra el estado que el usuario tenia asignado a un juego.
export const eliminarEstadoDeJuego = async (idJuego) => {
    const respuesta = await api.delete(`/status/${idJuego}`);
    return respuesta.data;
};

// Trae solo los id de juego y el estado, para pintar etiquetas rapidas
// en las cards del listado sin cargar mas datos.
export const listarEstadosDeJuego = async () => {
    const respuesta = await api.get("/status/list");
    return respuesta.data;
};

// Trae la lista completa con datos del juego (nombre, imagen, etc.),
// que necesita la pantalla de perfil para mostrar el listado por estado.
export const listarEstadosDeJuegoCompletos = async () => {
    const respuesta = await api.get("/status/list/full");
    return respuesta.data;
};
