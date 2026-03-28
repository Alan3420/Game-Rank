import api from './api';

export async function getContentOverview (game_id, game_name) {
    try {

        if (!game_id && !game_name) {
            throw new Error('Debe proporcionar un ID de juego o un nombre de juego para obtener el resumen del contenido.');
        }



        const response = await api.get('/content/overview',{
            params:{"game_id":game_id, "game_name":game_name}
        });
        return response.data;
    } catch (error) {
        if(error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            throw new Error(`Error en la respuesta del servidor: ${error.response.data}`);
        }
    }
};