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


# Servicio que actua de fachada para todo lo relacionado con juegos:
# detalles, catalogo, proximos lanzamientos, busqueda filtrada, saga,
# DLC, logros y video aleatorio del hero.
#
# Mucha de la informacion se obtiene de la API de RAWG. Lo que guardamos
# en nuestra BD es solo el "esqueleto" del juego (id + nombre + fecha)
# para poder enlazar comentarios/calificaciones/favoritos con FK.


# Pool de hilos que se usa para guardar juegos en segundo plano cuando se
# pinta el catalogo, sin bloquear la respuesta al usuario.
pool_guardado_segundo_plano = ThreadPoolExecutor(
    max_workers=5,
    thread_name_prefix="guardar_juego"
)


def obtener_detalle_del_videojuego(id_juego) -> dict:
    # Pide a RAWG todos los datos del juego, los completa con capturas,
    # videos, tiendas y equipo de desarrollo (cada cosa va a un endpoint
    # distinto), y si es la primera vez que vemos este juego lo guardamos
    # en la BD local con un resumen de plataformas/devs.
    detalle_juego = get_game_by_id_api(game_id=id_juego)

    juego_existe = vGame_repo.obtener_juego_por_id_bd(id_juego=id_juego)

    detalle_juego["short_screenshots"] = get_game_screenshots(game_id=id_juego)
    # Limitamos a 2 trailers para no inflar la respuesta.
    detalle_juego["movies"] = get_game_movies(game_id=id_juego)[:2]

    # Para las tiendas pedimos el catalogo completo de RAWG una sola vez y
    # lo cruzamos con las tiendas del juego. Asi obtenemos nombre + slug
    # de cada tienda con un solo round-trip.
    tiendas = get_game_stores(game_id=id_juego)
    catalogo_tiendas = get_stores_catalog()

    for item in tiendas:
        id_tienda = item.get("store_id")
        if id_tienda and id_tienda in catalogo_tiendas:
            item["store"] = catalogo_tiendas[id_tienda]

    detalle_juego["stores"] = tiendas
    detalle_juego["team"] = obtener_equipo_desarrollo(game_id=id_juego)

    if not juego_existe:
        # Construimos los strings "PC, PS5, Xbox" y "Rockstar, Naughty Dog"
        # para guardarlos planos en la BD local (la columna es VARCHAR).
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
    # Pedimos a RAWG juegos cuya fecha de lanzamiento este entre HOY y el
    # 31 de diciembre del anio actual. Solo los que aun no han salido.
    ahora = datetime.now()
    fecha_inicio = ahora.strftime("%Y-%m-%d")
    fecha_fin = datetime(ahora.year, 12, 31).strftime("%Y-%m-%d")

    resultado = get_future_releases(
        init_date=fecha_inicio,
        final_date=fecha_fin,
        page=pagina,
        per_page=por_pagina
    )

    # Mismo contrato que el catalogo: games + metadatos de paginacion.
    # El frontend lo usa para pintar los botones de pagina.
    return {
        "games": formatear_resumen_juego(resultado.get("results", [])),
        "next": resultado.get("next"),
        "previous": resultado.get("previous"),
        "count": resultado.get("count", 0)
    }


def _guardar_juego_si_no_existe(id_juego, app):
    # Funcion auxiliar para el pool de hilos. Necesita app_context propio
    # porque vive en otro hilo distinto al de la request.
    with app.app_context():
        try:
            if vGame_repo.obtener_juego_por_id_bd(id_juego):
                return
            obtener_detalle_del_videojuego(id_juego=id_juego)
        except Exception as error:
            print(f"Error al guardar el juego con id {id_juego}: {str(error)}")


def guardar_juegos(juegos: list[dict] | None, app):
    # Encola cada juego del listado para guardarse en segundo plano.
    # La respuesta al usuario sale de inmediato; el guardado en BD se hace
    # cuando los hilos lo procesan.
    if not juegos:
        return
    for juego in juegos:
        pool_guardado_segundo_plano.submit(_guardar_juego_si_no_existe, juego["id"], app)


def obtener_video_aleatorio() -> dict | None:
    # Recorre varias listas ordenadas (mas anadidos, mejor valorados, etc.)
    # y por cada lista mira los juegos en orden aleatorio buscando uno que
    # tenga al menos un trailer. Devuelve la URL del primer trailer encontrado.
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
                # Si falla con un juego concreto, seguimos con el siguiente
                # en vez de abortar el endpoint entero.
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
    # Pasamos los filtros tal cual a RAWG. Esta funcion es solo el wrapper
    # para que el route no tenga que tocar el client directamente.
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
