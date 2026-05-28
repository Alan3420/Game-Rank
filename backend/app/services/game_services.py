from app.repositories import vGame_repo
from app.client.clientRAWG import (
    get_game_by_id_api,
    get_all_games,
    get_game_screenshots,
    get_game_movies,
    get_future_releases,
    get_games_by_ordering,
    get_games_filtered,
    get_game_stores,
    get_stores_catalog,
    obtener_saga_del_juego,
    obtener_equipo_desarrollo,
    obtener_adicciones_juego,
    obtener_logros_juego
)
from app.services.adapter import formatear_detalle_juego, formatear_resumen_juego, formatear_logros
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import random


# Pool para ir guardando juegos en segundo plano mientras se pinta el
# catalogo, asi la respuesta sale al usuario antes de tocar la BD
pool_guardado_segundo_plano = ThreadPoolExecutor(
    max_workers=5,
    thread_name_prefix="guardar_juego"
)


def obtener_detalle_del_videojuego(id_juego) -> dict:
    detalle_juego = get_game_by_id_api(game_id=id_juego)

    juego_existe = vGame_repo.obtener_juego_por_id_bd(id_juego=id_juego)

    detalle_juego["short_screenshots"] = get_game_screenshots(game_id=id_juego)
    detalle_juego["movies"] = get_game_movies(game_id=id_juego)[:2]

    # Pedimos el catalogo entero de tiendas de RAWG una vez y lo cruzamos
    # con las tiendas del juego, asi nos ahorramos llamadas extra
    tiendas = get_game_stores(game_id=id_juego)
    catalogo_tiendas = get_stores_catalog()

    for item in tiendas:
        id_tienda = item.get("store_id")
        if id_tienda and id_tienda in catalogo_tiendas:
            item["store"] = catalogo_tiendas[id_tienda]

    detalle_juego["stores"] = tiendas
    detalle_juego["team"] = obtener_equipo_desarrollo(game_id=id_juego)

    if not juego_existe:
        lista_plataformas = ""
        lista_desarrolladoras = ""

        for plataforma in detalle_juego["platforms"]:
            lista_plataformas = lista_plataformas + plataforma["platform"]["name"]
            if plataforma != detalle_juego["platforms"][-1]:
                lista_plataformas = lista_plataformas + ", "

        for desarrolladora in detalle_juego["developers"]:
            lista_desarrolladoras = lista_desarrolladoras + desarrolladora["name"]
            if desarrolladora != detalle_juego["developers"][-1]:
                lista_desarrolladoras = lista_desarrolladoras + ", "

        vGame_repo.crear_videojuego(
            id_juego_api=detalle_juego["id"],
            nombre=detalle_juego["name"],
            fecha_lanzamiento=detalle_juego["released"],
            plataformas=lista_plataformas,
            compania_desarrollo=lista_desarrolladoras
        )

    return formatear_detalle_juego(detalle_juego)


def obtener_proximos_lanzamientos(pagina, por_pagina):
    ahora = datetime.now()
    fecha_inicio = ahora.strftime("%Y-%m-%d")
    fecha_fin = datetime(ahora.year, 12, 31).strftime("%Y-%m-%d")

    resultado = get_future_releases(
        init_date=fecha_inicio,
        final_date=fecha_fin,
        page=pagina,
        per_page=por_pagina
    )

    return {
        "games": formatear_resumen_juego(resultado.get("results", [])),
        "next": resultado.get("next"),
        "previous": resultado.get("previous"),
        "count": resultado.get("count", 0)
    }


def _guardar_juego_si_no_existe(id_juego, app):
    # Como esto corre en otro hilo necesita su propio app_context
    with app.app_context():
        try:
            if vGame_repo.obtener_juego_por_id_bd(id_juego):
                return
            obtener_detalle_del_videojuego(id_juego=id_juego)
        except Exception as error:
            print(f"Error al guardar el juego con id {id_juego}: {str(error)}")


def guardar_juegos(juegos: list[dict] | None, app):
    if not juegos:
        return
    for juego in juegos:
        pool_guardado_segundo_plano.submit(_guardar_juego_si_no_existe, juego["id"], app)


def obtener_video_aleatorio() -> dict | None:
    # Vamos probando varias listas ordenadas hasta encontrar un juego con
    # trailer, asi siempre tenemos algo que mostrar en el hero
    ordenes = ["-added", "-rating", "-metacritic", "-relevance"]

    for orden in ordenes:
        juegos = get_games_by_ordering(ordering=orden, per_page=40)

        if not juegos:
            continue

        random.shuffle(juegos)

        for juego in juegos:
            try:
                id_juego = juego.get("id")
                if not id_juego:
                    continue

                videos = get_game_movies(game_id=id_juego)
                if not videos:
                    continue

                for v in videos:
                    datos_video = v.get("data") or {}
                    url_video = datos_video.get("max") or datos_video.get("480")
                    if url_video:
                        return {"video_url": url_video}

            except Exception:
                continue

    return None


def obtener_juegos_del_catalogo(pagina: int, por_pagina: int):
    resultado = get_all_games(page=pagina, per_page=por_pagina)
    return {
        "games": formatear_resumen_juego(resultado.get("results", [])),
        "next": resultado.get("next"),
        "previous": resultado.get("previous"),
        "count": resultado.get("count", 0)
    }


def obtener_juegos_filtrados(pagina, por_pagina, ordering=None, genres=None,
                              platforms=None, dates=None, search=None):
    resultado = get_games_filtered(
        page=pagina,
        per_page=por_pagina,
        ordering=ordering,
        genres=genres,
        platforms=platforms,
        dates=dates,
        search=search
    )
    return {
        "games": formatear_resumen_juego(resultado.get("results", [])),
        "next": resultado.get("next"),
        "previous": resultado.get("previous"),
        "count": resultado.get("count", 0)
    }


def obtener_adicciones_del_juego(id_juego) -> list:
    adicciones = obtener_adicciones_juego(game_id=id_juego)
    return formatear_resumen_juego(adicciones)


def obtener_saga(id_juego) -> list:
    juegos = obtener_saga_del_juego(game_id=id_juego)
    return formatear_resumen_juego(juegos)


def obtener_logros_del_juego(id_juego) -> list:
    logros = obtener_logros_juego(game_id=id_juego)
    return formatear_logros(logros)
