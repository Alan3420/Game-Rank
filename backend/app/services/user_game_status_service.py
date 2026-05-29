from app.repositories import user_game_status_repo
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import formatear_resumen_juego


ESTADOS_VALIDOS = {"pendiente", "pausado", "jugando", "completado"}


def establecer_estado(id_usuario, id_juego, estado) -> object | str:
    if estado not in ESTADOS_VALIDOS:
        return f"El status debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"

    registro_existente = user_game_status_repo.obtener_estado(id_usuario=id_usuario, id_juego=id_juego)
    if registro_existente:
        return user_game_status_repo.actualizar_estado(
            id_usuario=id_usuario,
            id_juego=id_juego,
            nuevo_estado=estado
        )

    return user_game_status_repo.crear_estado(
        id_usuario=id_usuario,
        id_juego=id_juego,
        estado=estado
    )


def obtener_estado_del_juego(id_usuario, id_juego) -> object | None:
    return user_game_status_repo.obtener_estado(id_usuario=id_usuario, id_juego=id_juego)


def listar_estados_del_usuario(id_usuario) -> list:
    registros = user_game_status_repo.listar_estados_por_usuario(id_usuario=id_usuario)

    resultado = []
    for r in registros:
        resultado.append(r.to_dict())
    return resultado


def listar_estados_con_juegos(id_usuario) -> list:
    registros = user_game_status_repo.listar_estados_por_usuario(id_usuario=id_usuario)

    resultado = []
    for registro in registros:
        # Si RAWG falla con un juego concreto saltamos a por el siguiente,
        # es preferible mostrar 9 de 10 antes que romper toda la respuesta
        try:
            datos_rawg = get_game_by_id_api(game_id=registro.id_game_api)
            if not datos_rawg:
                continue
            juego_resumen = formatear_resumen_juego(datos_rawg)
            resultado.append({
                "status": registro.status,
                "game": juego_resumen
            })
        except Exception:
            continue

    return resultado


def quitar_estado(id_usuario, id_juego) -> bool | str:
    resultado = user_game_status_repo.eliminar_estado(id_usuario=id_usuario, id_juego=id_juego)

    if not resultado:
        return "Status no encontrado"

    return resultado
