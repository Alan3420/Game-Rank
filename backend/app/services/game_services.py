from app.repositories.vGame_repo import create_video_game, get_game_by_id_bd
from app.client.clientRAWG import get_game_by_id_api, get_all_games, get_game_screenshots, get_game_movies, get_future_releases, get_games_by_ordering, get_games_filtered, get_game_stores, get_stores_catalog, obtener_saga_del_juego, obtener_equipo_desarrollo, obtener_adicciones_juego, obtener_logros_juego
from app.services.adapter import game_format_details, game_format_resume, logros_format
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor



pool_guardado_segundo_plano = ThreadPoolExecutor(
    max_workers=5, thread_name_prefix="save_game")


def get_video_game_details(game_id) -> dict:
    try:
        game_details = get_game_by_id_api(game_id=game_id)

        game_exists = get_game_by_id_bd(game_id=game_id)

        screenshots = get_game_screenshots(game_id=game_id)
        game_details["short_screenshots"] = screenshots
        game_details["movies"] = get_game_movies(game_id=game_id)[:2]

        stores = get_game_stores(game_id=game_id)
        catalog = get_stores_catalog()

        for item in stores:
            sid = item.get("store_id")
            if sid and sid in catalog:
                item["store"] = catalog[sid]
                
        game_details["stores"] = stores
        game_details["team"] = obtener_equipo_desarrollo(game_id=game_id)

        if not game_exists:
            listaPlataformas = ""
            listaDevs_Company = ""
            for plataforma in game_details["platforms"]:
                listaPlataformas += plataforma["platform"]["name"]
                if plataforma != game_details["platforms"][-1]:
                    listaPlataformas += ", "

            for dev_company in game_details["developers"]:
                listaDevs_Company += dev_company["name"]
                if dev_company != game_details["developers"][-1]:
                    listaDevs_Company += ", "

            create_video_game(id_game_api=game_details["id"],
                              name=game_details["name"],
                              date_release=game_details["released"],
                              platforms=listaPlataformas,
                              development_company=listaDevs_Company)

        resultado = game_format_details(game_details)

        return resultado
    except Exception as e:

        raise Exception(f"Error al obtener los detalles del juego: {str(e)}")



def get_upcoming_launch_games(page, per_page):
    try:
        init_date = None
        final_date = None

        time = datetime.now()

        init_date = time.strftime("%Y-%m-%d")
        final_date = datetime(time.year, 12, 31).strftime("%Y-%m-%d")

        return game_format_resume(get_future_releases(init_date=init_date, final_date=final_date, page=page, per_page=per_page))

    except Exception as e:
        raise Exception(f"Error:{str(e)}")



def _guardar_juego_si_no_existe(id_juego, app):
    with app.app_context():
        try:
            if get_game_by_id_bd(id_juego):
                return
            get_video_game_details(game_id=id_juego)
        except Exception as error:
            print(f"Error al guardar el juego con id {id_juego}: {str(error)}")


def save_games(games: list[dict] | None, app):
    if not games:
        return
    for juego in games:
        pool_guardado_segundo_plano.submit(_guardar_juego_si_no_existe, juego["id"], app)


def get_random_game_video() -> dict | None:
    try:
        import random

        orderings = ["-added", "-rating",
                     "-metacritic", "-released", "-relevance"]

        for ordering in orderings:
            games = get_games_by_ordering(ordering=ordering, per_page=40)

            if not games:
                continue

            random.shuffle(games)

            for game in games:
                try:
                    game_id = game.get("id")
                    if not game_id:
                        continue

                    videos = get_game_movies(game_id=game_id)

                    if not videos:
                        continue

                    for v in videos:
                        data = v.get("data") or {}
                        video_url = data.get("max") or data.get("480")
                        if video_url:
                            return {"video_url": video_url}
                except Exception:
                    continue

        return None
    except Exception as e:
        raise Exception(f"Error al obtener video aleatorio: {str(e)}")


def get_catalog_games(page: int, per_page: int):
    try:
        result = get_all_games(page=page, per_page=per_page)
        return {
            "games": game_format_resume(result.get("results", [])),
            "next": result.get("next"),
            "previous": result.get("previous"),
            "count": result.get("count", 0)
        }
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def get_video_games_filtered(page, per_page, ordering=None, genres=None, platforms=None, dates=None, search=None):
    try:
        result = get_games_filtered(
            page=page,
            per_page=per_page,
            ordering=ordering,
            genres=genres,
            platforms=platforms,
            dates=dates,
            search=search
        )
        return {
            "games": game_format_resume(result.get("results", [])),
            "next": result.get("next"),
            "previous": result.get("previous"),
            "count": result.get("count", 0)
        }
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def obtener_adicciones_servicio(game_id) -> list:
    try:
        adicciones = obtener_adicciones_juego(game_id=game_id)
        return game_format_resume(adicciones)
    except Exception as e:
        raise Exception(f"Error al obtener adicciones del juego: {str(e)}")


def obtener_saga_servicio(game_id) -> list:
    try:
        juegos = obtener_saga_del_juego(game_id=game_id)
        return game_format_resume(juegos)
    except Exception as e:
        raise Exception(f"Error al obtener saga del juego: {str(e)}")


def obtener_logros_servicio(game_id) -> list:
    try:
        logros = obtener_logros_juego(game_id=game_id)
        return logros_format(logros)
    except Exception as e:
        raise Exception(f"Error al obtener logros del juego: {str(e)}")


