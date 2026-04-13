from app.repositories.vGame_repo import create_video_game, get_all_video_games, get_game_by_id_api, get_game_by_id_bd, get_game_by_name
from app.services.adapter import game_format_details, game_format_resume

def get_video_game_details(game_id) -> dict:
    try:
        game_details = get_game_by_id_api(game_id=game_id)

        game_exists = get_game_by_id_bd(game_id=game_id)

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
                            development_company=listaDevs_Company,
                            id_comment=None)


        return game_format_details(game_details)
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
        games = get_all_video_games()

        start = (page - 1) * per_page
        end = start + per_page

        paginated_games = games["results"][start:end]

        return game_format_resume(paginated_games)

    except Exception as e:
        raise Exception(f"Error al obtener los juegos con paginación: {str(e)}")


            
                
            
            
    
        
        
        
        
        