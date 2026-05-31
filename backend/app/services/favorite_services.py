from app.repositories import favorite_repo
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import formatear_resumen_juego


ESTADOS_VALIDOS = {"pendiente", "pausado", "jugando", "completado"}


def agregar_favorito(id_usuario, id_juego, status=None) -> object | str:
    if favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego):
        return "El juego ya está en favoritos"

    if status is not None and status not in ESTADOS_VALIDOS:
        return f"El status debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"

    return favorite_repo.crear_favorito(id_usuario=id_usuario, id_juego=id_juego, status=status)


def eliminar_favorito(id_usuario, id_juego) -> bool | str:
    if not favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego):
        return "El juego no está en favoritos"

    return favorite_repo.eliminar_favorito(id_usuario=id_usuario, id_juego=id_juego)


def actualizar_status(id_usuario, id_juego, nuevo_status) -> object | str:
    if nuevo_status not in ESTADOS_VALIDOS:
        return f"El status debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"

    resultado = favorite_repo.actualizar_status(
        id_usuario=id_usuario,
        id_juego=id_juego,
        nuevo_status=nuevo_status
    )

    if not resultado:
        return "El juego no está en favoritos"

    return resultado


def obtener_estado_del_juego(id_usuario, id_juego) -> object | None:
    return favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)


def quitar_status(id_usuario, id_juego) -> bool | str:
    favorito = favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if not favorito:
        return "El juego no está en favoritos"

    favorito.status = None
    from app.database.db import db
    db.session.commit()
    return True


def obtener_favoritos_del_usuario(id_usuario) -> list:
    favoritos = favorite_repo.obtener_favoritos_por_usuario(id_usuario=id_usuario)

    resultado = []
    for favorito in favoritos:
        juego = get_game_by_id_api(favorito.id_game_api)
        if juego:
            datos = formatear_resumen_juego(juego)
            datos["status"] = favorito.status
            resultado.append(datos)

    return resultado


def listar_favoritos_con_status(id_usuario) -> list:
    favoritos = favorite_repo.obtener_favoritos_por_usuario(id_usuario=id_usuario)
    resultado = []
    for f in favoritos:
        if f.status:
            resultado.append(f.to_dict())
    return resultado


def listar_favoritos_completos(id_usuario) -> list:
    favoritos = favorite_repo.obtener_favoritos_por_usuario(id_usuario=id_usuario)

    resultado = []
    for favorito in favoritos:
        if not favorito.status:
            continue
        try:
            datos_rawg = get_game_by_id_api(game_id=favorito.id_game_api)
            if not datos_rawg:
                continue
            juego_resumen = formatear_resumen_juego(datos_rawg)
            resultado.append({
                "status": favorito.status,
                "game": juego_resumen
            })
        except Exception:
            continue

    return resultado


def es_favorito(id_usuario, id_juego) -> bool:
    return favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego) is not None
