from app.repositories.rate_repo import create_rate, update_rate, delete_rate, get_all_rates, get_rate_by_id
from app.models  import Rate

def crear_valoracion(id_user, id_video_game, rate) -> Rate:

    calificacion = create_rate(id_user=id_user, id_video_game=id_video_game, rating=rate)

    return calificacion


def actualizar_valoracion(rate_id, rate):

    calificacion = update_rate(rate_id=rate_id, rating=rate)

    return calificacion

def eliminar_valoracion(rate_id) -> bool:

    resultado = delete_rate(rate_id=rate_id)

    return resultado

def get_media_game(id_video_game = None, id_user = None) -> float | int:

    id_game_id_user = 0

    if id_user:
        id_game_id_user = id_user
    else:
        id_game_id_user = id_video_game


    if id_video_game:
        rates = get_all_rates()
        media = 0
        contador = 0

        for rate in rates:
            if rate.id_game_api== id_game_id_user:
                media += rate.rating
                contador += 1

        return media/contador
    
def get_status_game(id_video_game) -> str:

    reseña = get_rate_by_id(rate_id=id_video_game)

    return reseña.status

  
