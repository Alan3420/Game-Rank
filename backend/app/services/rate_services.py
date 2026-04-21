from app.repositories.rate_repo import get_rate_by_id, get_rate_by_user_and_game,get_rates_by_game, get_rates_by_user,create_rate, update_rate, delete_rate

def crear_valoracion(id_user, id_game, rating, status) -> object | str:
    try:
        existe = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
        if existe:
            return "Ya has valorado este juego"
        rate = create_rate(id_user=id_user, id_game=id_game, rating=rating, status=status)
        return rate
    except Exception as e:
        raise Exception(f"Error al crear la valoración: {str(e)}")
    
def actualizar_valoracion(id_user, id_game, rating=None, status=None) -> object | str:
    try:
        rate = update_rate(id_user=id_user, id_game=id_game, rating=rating, status=status)
        if not rate:
            return "Valoración no encontrada"
        return rate
    except Exception as e:
        raise Exception(f"Error al actualizar la valoración: {str(e)}")

def eliminar_valoracion(id_user, id_game) -> bool | str:
    try:
        resultado = delete_rate(id_user=id_user, id_game=id_game)
        if not resultado:
            return "Valoración no encontrada"
        return resultado
    except Exception as e:
        raise Exception(f"Error al eliminar la valoración: {str(e)}")

def get_media_juego(id_game) -> float:
    try:
        rates = get_rates_by_game(id_game=id_game)
        if not rates:
            return 0
        total = 0
        for rate in rates:
            total += rate.rating

        return round(total / len(rates), 2)
    
    except Exception as e:
        raise Exception(f"Error al calcular la media: {str(e)}")

def get_valoraciones_juego(id_game) -> list:
    try:
        rates = get_rates_by_game(id_game=id_game)
        resultado = []

        for rate in rates:
            resultado.append(rate.to_dict())
        return resultado
    except Exception as e:
        raise Exception(f"Error al obtener valoraciones: {str(e)}")
    
def get_valoraciones_usuario(id_user) -> list:
    try:
        rates = get_rates_by_user(id_user=id_user)
        resultado = []
        for rate in rates:
            resultado.append(rate.to_dict())
        return resultado
    except Exception as e:
        raise Exception(f"Error al obtener valoraciones: {str(e)}")

def get_estado_juego(id_user, id_game) -> str | None:
    try:
        rate = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
        if not rate:
            return None
        return rate.status
    except Exception as e:
        raise Exception(f"Error al obtener el estado: {str(e)}")