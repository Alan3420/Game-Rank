from app.repositories.vGame_repo import get_game_by_id, get_all_video_games, get_game_by_name, create_video_game

def get_video_game_details(game_id):
    game_details = get_game_by_id(game_id=game_id)
    all_games = get_all_video_games()

    print(game_details)
    game_exists = False

    for game in all_games:
        if game.id_game_api ==game_details["id"]:
            print(game.id_game_api)
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

def get_video_game_by_name_details(game_name):
    game_details = get_game_by_name(game_name=game_name)
    if not game_details["results"]:
        raise Exception("No se encontró ningún juego con ese nombre")   
    return game_format(game_details["results"])

def game_format(data):
    if type(data) != list:
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "release_date": data.get("released"),
            "description": data.get("description"),
            "imge_url": data.get("background_image"),
            "rating": data.get("rating"),
             "platforms":    [p.get("platform", {}).get("name") for p in (data.get("platforms") or [])],
            "developers":   [d.get("name") for d in (data.get("developers") or [])],
        }
    else:
        return [
            {
                "id": game.get("id"),
                "name": game.get("name"),
                "release_date": game.get("released"),
                "description": game.get("description"),
                "imge_url": game.get("background_image"),
                "rating": game.get("rating"),
                "platforms":    [p.get("platform", {}).get("name") for p in (game.get("platforms") or [])],
                "developers":   [d.get("name") for d in (game.get("developers") or [])],
            }
            for game in data
        ]
        
        
        
        
        