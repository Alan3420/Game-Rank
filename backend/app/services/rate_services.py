from app.repositories.rate_repo import get_rate_by_user_and_game, get_rates_by_game, get_rates_by_user, create_rate, update_rate, delete_rate


def crear_valoracion(id_user, id_game, rating, status) -> object | str:
    try:
        if not isinstance(rating, int) or rating < 0 or rating > 5:
            return "La valoración debe ser un número entero entre 0 y 5"

        if get_rate_by_user_and_game(id_user=id_user, id_game=id_game):
            return "Ya has valorado este juego"
        return create_rate(id_user=id_user, id_game=id_game, rating=rating, status=status)
    except Exception as e:
        raise Exception(f"Error al crear la valoración: {str(e)}")


def actualizar_valoracion(id_user, id_game, rating=None, status=None) -> object | str:
    try:
        if rating is not None:
            if not isinstance(rating, int) or rating < 0 or rating > 5:
                return "La valoración debe ser un número entero entre 0 y 5"

        rate = update_rate(id_user=id_user, id_game=id_game,
                           rating=rating, status=status)
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
            return 0.0
        return round(sum(r.rating for r in rates) / len(rates), 2)
    except Exception as e:
        raise Exception(f"Error al calcular la media: {str(e)}")


def get_valoraciones_juego(id_game) -> list:
    try:
        rates = get_rates_by_game(id_game=id_game)
        return [r.to_dict() for r in rates]
    except Exception as e:
        raise Exception(f"Error al obtener valoraciones: {str(e)}")


def get_valoraciones_usuario(id_user) -> list:
    try:
        rates = get_rates_by_user(id_user=id_user)
        return [r.to_dict() for r in rates]
    except Exception as e:
        raise Exception(f"Error al obtener valoraciones: {str(e)}")


def get_estado_juego(id_user, id_game) -> str | None:
    try:
        rate = get_rate_by_user_and_game(id_user=id_user, id_game=id_game)
        return rate.status if rate else None
    except Exception as e:
        raise Exception(f"Error al obtener el estado: {str(e)}")
