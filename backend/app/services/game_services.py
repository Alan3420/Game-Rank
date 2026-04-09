from app.repositories.vGame_repo import get_game_by_id, get_all_video_games, get_game_by_name, create_video_game
from app.services.adapter import game_format

def get_video_game_details(game_id) -> dict:
    game_details = get_game_by_id(game_id=game_id)
    all_games = get_all_video_games()

    game_exists = False

    for game in all_games:
        if game.id_game_api ==game_details["id"]:
            game_exists = True
            break

    if not game_exists:
        create_video_game(id_game_api=int(game_details["id"]), 
                              name=str(game_details["name"]), 
                              date_release=game_details["released"], 
                              platforms=str(game_details["platforms"][0]["platform"]["name"]), 
                              development_company=str(game_details["developers"][0]["name"]), 
                              id_comment=None)

    return game_format(game_details)

def get_video_game_by_name_details(game_name) -> dict | list[dict]:
    name_game_details = get_game_by_name(game_name=game_name)

    id_game_details = name_game_details["results"][0]["id"]

    game_details = get_game_by_id(game_id=id_game_details)

    if not name_game_details["results"]:
        raise Exception("No se encontró ningún juego con ese nombre")   
    return game_format(game_details)


            
                
            
            
    
        
        
        
        
        