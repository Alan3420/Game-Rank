import api from "./api";

export const setGameStatus = async (gameId, status) => {
    const response = await api.post("/status/set", { id_game: gameId, status });
    return response.data;
};

export const getGameStatus = async (gameId) => {
    const response = await api.get(`/status/${gameId}`);
    return response.data;
};

export const removeGameStatus = async (gameId) => {
    const response = await api.delete(`/status/${gameId}`);
    return response.data;
};

export const listGameStatuses = async () => {
    const response = await api.get("/status/list");
    return response.data;
};

export const listGameStatusesFull = async () => {
    const response = await api.get("/status/list/full");
    return response.data;
};
