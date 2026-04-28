from app.repositories.vGame_repo import create_video_game, get_game_by_id_bd
from app.client.clientRAWG import get_game_by_id_api, get_game_by_name, get_all_video_games, get_game_screenshots
from app.services.adapter import game_format_details, game_format_resume


def get_video_game_details(game_id) -> dict:
    try:
        game_details = get_game_by_id_api(game_id=game_id)

        game_exists = get_game_by_id_bd(game_id=game_id)

        screenshots = get_game_screenshots(game_id=game_id)
        game_details["short_screenshots"] = screenshots


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


def get_video_game_by_name_details(game_name) -> dict | None:
    name_game_details = get_game_by_name(game_name=game_name)

    id_game_details = name_game_details["results"][0]["id"]

    game_details = get_game_by_id_api(game_id=id_game_details)

    if not name_game_details["results"]:
        return None
    return game_format_details(game_details)


def get_video_games_pagination(page: int, per_page: int):

    try:
        games = get_all_video_games(page=page, per_page=per_page)

        return {
            "games": game_format_resume(games.get("results", [])),
            "next": games.get("next"),
            "previous": games.get("previous")
        }

    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def save_games(games: list, app):
    with app.app_context():
        try:
            listaJuegos = game_format_details(games)

            if type(listaJuegos) == list:

                for game_resum in listaJuegos:

                    game_api = get_game_by_id_api(game_id=game_resum["id"])
                    id_bd = get_game_by_id_bd(game_api["id"])

                    if not id_bd:
                        get_video_game_details(game_id=game_api["id"])

        except Exception as e:
            print(f"Error al guardar el juego {game_api['name']}: {str(e)}")


def filter_games_by_platform_or_genres(plataforma=None, genero=None) -> list[dict] | None:

    try:
        if plataforma:

            games = get_all_video_games()

            games_by_platforms = []

            for game in games["results"]["parent_platforms"]:

                if game["platform"]["name"] == plataforma:
                    games_by_platforms.append(game)

            return game_format_resume(games_by_platforms)

        if genero:
            games = get_all_video_games()
            games_by_genres = []

            for game in games["results"]["genres"]:
                if game["name"] == genero:
                    games_by_genres.append(game)

            return game_format_resume(games_by_genres)

    except Exception as e:
        raise Exception(
            f"Error al obtener los juegos por plataforma/género: {str(e)}")
