from app.repositories.user_game_status_repo import (
    obtener_status, listar_statuses_por_usuario,
    crear_status, actualizar_status, eliminar_status
)
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import game_format_resume


STATUS_VALIDOS = {"pendiente", "pausado", "jugando", "completado"}


def establecer_status(id_user, id_game, status) -> object | str:
    try:
        if status not in STATUS_VALIDOS:
            return f"El status debe ser uno de: {', '.join(STATUS_VALIDOS)}"

        registro_existente = obtener_status(id_user=id_user, id_game=id_game)
        if registro_existente:
            return actualizar_status(id_user=id_user, id_game=id_game, nuevo_status=status)

        return crear_status(id_user=id_user, id_game=id_game, status=status)
    except Exception as e:
        raise Exception(f"Error al establecer el status: {str(e)}")


def obtener_status_juego(id_user, id_game) -> object | None:
    try:
        return obtener_status(id_user=id_user, id_game=id_game)
    except Exception as e:
        raise Exception(f"Error al obtener el status: {str(e)}")


def listar_statuses_usuario(id_user) -> list:
    try:
        registros = listar_statuses_por_usuario(id_user=id_user)
        return [r.to_dict() for r in registros]
    except Exception as e:
        raise Exception(f"Error al listar los statuses: {str(e)}")


def listar_statuses_con_juegos(id_user) -> list:
    try:
        registros = listar_statuses_por_usuario(id_user=id_user)
        resultado = []
        for registro in registros:
            try:
                datos_rawg = get_game_by_id_api(game_id=registro.id_game_api)
                if not datos_rawg:
                    continue
                juego_resumen = game_format_resume(datos_rawg)
                resultado.append({
                    "id_status": registro.id_status,
                    "status": registro.status,
                    "game": juego_resumen
                })
            except Exception:
                continue
        return resultado
    except Exception as e:
        raise Exception(f"Error al listar statuses con juegos: {str(e)}")


def quitar_status(id_user, id_game) -> bool | str:
    try:
        resultado = eliminar_status(id_user=id_user, id_game=id_game)
        if not resultado:
            return "Status no encontrado"
        return resultado
    except Exception as e:
        raise Exception(f"Error al eliminar el status: {str(e)}")