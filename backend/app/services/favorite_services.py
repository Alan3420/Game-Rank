from app.repositories import favorite_repo
from app.client.clientRAWG import get_game_by_id_api
from app.services.adapter import formatear_resumen_juego


def agregar_favorito(id_usuario, id_juego) -> object | str:
    existe = favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if existe:
        return "El juego ya está en favoritos"

    nuevo_favorito = favorite_repo.crear_favorito(id_usuario=id_usuario, id_juego=id_juego)
    return nuevo_favorito


def eliminar_favorito(id_usuario, id_juego) -> bool | str:
    existe = favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if not existe:
        return "El juego no está en favoritos"

    resultado = favorite_repo.eliminar_favorito(id_usuario=id_usuario, id_juego=id_juego)
    return resultado


def obtener_favoritos_del_usuario(id_usuario) -> list:
    # En BD solo guardamos el id del juego asi que para cada favorito hay
    # que pedir el resto de datos a RAWG
    favoritos = favorite_repo.obtener_favoritos_por_usuario(id_usuario=id_usuario)

    resultado = []
    for favorito in favoritos:
        juego = get_game_by_id_api(favorito.id_game_api)
        if juego:
            resultado.append(formatear_resumen_juego(juego))

    return resultado


def es_favorito(id_usuario, id_juego) -> bool:
    favorito = favorite_repo.obtener_favorito(id_usuario=id_usuario, id_juego=id_juego)

    if favorito:
        return True
    return False
